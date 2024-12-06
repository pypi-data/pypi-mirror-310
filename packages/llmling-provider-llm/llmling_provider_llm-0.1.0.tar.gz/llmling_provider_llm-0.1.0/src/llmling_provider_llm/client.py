"""Client for the llm library."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any, Protocol

from llmling.core import capabilities, exceptions
from llmling.core.log import get_logger


if TYPE_CHECKING:
    import llm
    from llm.models import AsyncModel, Model, Response


logger = get_logger(__name__)

# Cache for model instances and capabilities
_model_cache: dict[str, AsyncModelProtocol] = {}
_capabilities_cache: dict[str, capabilities.Capabilities] = {}


class AsyncModelProtocol(Protocol):
    """Protocol defining the required async model interface."""

    model_id: str

    async def prompt(
        self,
        prompt: str,
        system: str | None = None,
        attachments: list[Any] | None = None,
        **kwargs: Any,
    ) -> Response | AsyncIterator[str]: ...


def _get_cached_model(model_id: str) -> AsyncModelProtocol:
    """Get or create cached model instance, falling back to sync if needed."""
    import llm

    if model_id not in _model_cache:
        try:
            # First try to get an async model
            _model_cache[model_id] = llm.get_async_model(model_id)
        except Exception as exc:  # noqa: BLE001
            # If async model isn't available, try sync model
            logger.debug("Falling back to sync model for %s: %s", model_id, exc)
            try:
                sync_model = llm.get_model(model_id)
                _model_cache[model_id] = SyncModelAdapter(sync_model)
            except llm.UnknownModelError as model_exc:
                msg = f"Model {model_id} not found"
                raise exceptions.LLMError(msg) from model_exc
    return _model_cache[model_id]


class SyncModelAdapter:
    """Adapter to make sync models behave like async models."""

    def __init__(self, model: Model) -> None:
        """Initialize the adapter with a sync model."""
        self.model = model
        self.model_id = model.model_id

    async def prompt(
        self,
        prompt: str,
        system: str | None = None,
        attachments: list[Any] | None = None,
        **kwargs: Any,
    ) -> DummyResponse:  # Note: Always return DummyResponse
        """Execute the prompt asynchronously by wrapping the sync model."""
        # Ignore streaming flag - sync models don't support true streaming
        kwargs.pop("stream", None)

        # Run the sync prompt in a thread
        response = await asyncio.to_thread(
            self.model.prompt,
            prompt,
            system=system,
            attachments=attachments,
            **kwargs,
        )

        # Handle both string and Response objects
        if isinstance(response, str):
            return DummyResponse(response)

        # If it's a Response object, get its text and wrap it
        content = response.text() if callable(response.text) else response.text
        return DummyResponse(content)


class DummyResponse:
    """Simple Response-like object for string outputs."""

    def __init__(self, content: str) -> None:
        """Initialize with content string."""
        self._content = content
        # Add basic token counting (optional)
        self.prompt_tokens = 0
        self.completion_tokens = len(content.split())
        self.total_tokens = self.completion_tokens
        self._iterator_used = False

    async def text(self) -> str:
        """Return the content string (as async method)."""
        return self._content

    def __aiter__(self) -> DummyResponse:
        """Make this class async iterable."""
        return self

    async def __anext__(self) -> str:
        """Yield the entire content as a single chunk."""
        if self._iterator_used:
            raise StopAsyncIteration
        self._iterator_used = True
        return self._content


def _detect_model_capabilities(model: AsyncModel) -> capabilities.Capabilities:
    """Detect model capabilities from instance."""
    try:
        # Get supported options
        valid_params = {
            "temperature",
            "max_tokens",
            "top_p",
            "frequency_penalty",
            "presence_penalty",
        }
        supported_params = [attr for attr in dir(model) if attr in valid_params]

        # Detect vision support from attachments
        supports_vision = hasattr(model, "handle_attachments")

        return capabilities.Capabilities(
            key=model.model_id,
            litellm_provider="llm",
            mode="chat",
            supports_system_messages=True,
            supports_vision=supports_vision,
            supported_openai_params=supported_params,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to detect capabilities: %s", exc)
        return capabilities.Capabilities(
            key=model.model_id,
            litellm_provider="llm",
            mode="chat",
        )


def get_model_info(model_id: str) -> capabilities.Capabilities:
    """Get model capabilities (cached)."""
    if model_id in _capabilities_cache:
        return _capabilities_cache[model_id]

    model = _get_cached_model(model_id)
    caps = _detect_model_capabilities(model)
    _capabilities_cache[model_id] = caps
    return caps


def _prepare_attachments(
    messages: list[dict[str, Any]],
) -> tuple[list[llm.Attachment], list[dict[str, Any]]]:
    """Extract attachments from messages."""
    import llm

    attachments = []
    clean_messages = []

    for msg in messages:
        if "content_items" in msg:
            msg_attachments = []
            text_content: list[Any] = []

            for item in msg["content_items"]:
                if item["type"] == "text":
                    text_content.append(item["content"])
                elif item["type"] == "image_url":
                    msg_attachments.append(llm.Attachment(url=item["content"]))
                elif item["type"] == "image_base64":
                    msg_attachments.append(
                        llm.Attachment(content=item["content"].encode())
                    )

            attachments.extend(msg_attachments)
            clean_messages.append({
                **msg,
                "content": "\n".join(text_content),
            })
        else:
            clean_messages.append(msg)

    return attachments, clean_messages


async def complete(
    model_id: str,
    messages: list[dict[str, Any]],
    **kwargs: Any,
) -> Any:
    """Execute completion."""
    try:
        model = _get_cached_model(model_id)

        # Extract system message if present
        system_prompt = None
        user_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            else:
                user_messages.append(msg)

        # Handle attachments
        attachments, clean_messages = _prepare_attachments(user_messages)

        # Build prompt from remaining messages
        prompt = "\n".join(
            f"{msg['role'].title()}: {msg['content']}" for msg in clean_messages
        )

        # Execute completion
        response = await model.prompt(
            prompt,
            system=system_prompt,
            attachments=attachments or None,
            **kwargs,
        )

        # Handle different response types
        if isinstance(response, AsyncIterator):
            # Collect all chunks for non-streaming response
            content = ""
            async for chunk in response:
                content += chunk
        else:
            # Regular response object
            content = await response.text()

        return {
            "choices": [{"message": {"content": content}}],
            "model": model_id,
            "usage": {
                "prompt_tokens": getattr(response, "prompt_tokens", 0),
                "completion_tokens": getattr(response, "completion_tokens", 0),
                "total_tokens": getattr(response, "total_tokens", 0),
            },
        }

    except Exception as exc:
        exc_msg = f"Completion failed: {exc}"
        raise exceptions.LLMError(exc_msg) from exc


async def stream(
    model_id: str,
    messages: list[dict[str, Any]],
    **kwargs: Any,
) -> AsyncIterator[Any]:
    """Stream completions, falling back to single response for sync models."""
    try:
        model = _get_cached_model(model_id)

        # Extract system message if present
        system_prompt = None
        user_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            else:
                user_messages.append(msg)

        # Handle attachments
        attachments, clean_messages = _prepare_attachments(user_messages)

        # Build prompt
        prompt = "\n".join(
            f"{msg['role'].title()}: {msg['content']}" for msg in clean_messages
        )

        response = await model.prompt(
            prompt,
            system=system_prompt,
            attachments=attachments or None,
            stream=True,
            **kwargs,
        )

        # Handle any kind of response as an async iterator
        async for chunk in response:
            yield {
                "choices": [{"delta": {"content": chunk}}],
                "model": model_id,
            }

    except Exception as exc:
        error_msg = f"Streaming failed: {exc}"
        raise exceptions.LLMError(error_msg) from exc


if __name__ == "__main__":
    import asyncio

    import devtools

    async def test_client():
        # List available models
        print("\nAvailable models:")
        # Test with Claude
        model_id = "gpt-3.5-turbo"
        print(f"\nTesting with {model_id}:")

        # Get capabilities
        info = get_model_info(model_id)
        print("\nCapabilities:")
        print(devtools.debug(info))

        # Test completion
        print("\nTesting completion:")
        response = await complete(
            model_id,
            [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": "Write a haiku about Python.",
                },
            ],
            temperature=0.7,
        )
        print(devtools.debug(response))

        # Test streaming
        print("\nTesting streaming:")
        async for chunk in stream(
            model_id,
            [{"role": "user", "content": "Count from 1 to 5 slowly."}],
            temperature=0.7,
        ):
            print(chunk["choices"][0]["delta"]["content"], end="", flush=True)
        # Test vision (if supported)
        if info.supports_vision:
            print("\nTesting vision:")
            response = await complete(
                model_id,
                [
                    {
                        "role": "user",
                        "content": "What's in this image?",
                        "content_items": [
                            {
                                "type": "image_url",
                                "content": "https://example.com/image.jpg",
                            }
                        ],
                    }
                ],
            )
            print(devtools.debug(response))

    asyncio.run(test_client())
