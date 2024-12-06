"""LLM library provider implementation."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Unpack
import uuid

from llmling.core import capabilities, exceptions
from llmling.core.log import get_logger
from llmling.llm.base import (
    CompletionResult,
    LLMConfig,
    LLMProvider,
    Message,
    MessageContent,
    ToolCall,
)

from llmling_provider_llm import client


if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from llmling.llm.clients.protocol import LiteLLMCompletionParams


logger = get_logger(__name__)


class LLMLibProvider(LLMProvider):
    """Provider implementation using the llm library."""

    def __init__(self, config: LLMConfig) -> None:
        """Initialize provider with configuration."""
        super().__init__(config)
        if not config.model:
            msg = "Model ID cannot be empty"
            raise ValueError(msg)
        self._capabilities = self._get_capabilities()
        msg = "Initialized LLMLib provider for model %s with capabilities: %s"
        logger.debug(msg, config.model, self._capabilities)

    def _get_capabilities(self) -> capabilities.Capabilities:
        """Get model capabilities."""
        return client.get_model_info(self.config.model)

    def _prepare_messages(self, messages: list[Message]) -> list[dict[str, Any]]:
        """Convert messages to llm library format."""
        prepared = []
        for msg in messages:
            # Basic message data
            message_data: dict[str, Any] = {"role": msg.role, "content": msg.content}
            # Add content items if present (for multi-modal)
            if msg.content_items:
                message_data["content_items"] = [
                    {"type": i.type, "content": i.content, "alt_text": i.alt_text}
                    for i in msg.content_items
                ]
            prepared.append(message_data)
        return prepared

    def _extract_tool_calls(
        self,
        response: dict[str, Any],
    ) -> list[ToolCall] | None:
        """Extract tool calls from response."""
        try:
            if "function_call" not in response:
                return None

            function_call = response["function_call"]
            return [
                ToolCall(
                    id=str(uuid.uuid4()),
                    name=function_call["name"],
                    parameters=json.loads(function_call["arguments"]),
                )
            ]
        except Exception:  # noqa: BLE001
            logger.warning("Failed to process tool calls", exc_info=True)
            return None

    async def complete(
        self,
        messages: list[Message],
        **kwargs: Unpack[LiteLLMCompletionParams],
    ) -> CompletionResult:
        """Generate a completion for the messages."""
        try:
            dct = self._prepare_messages(messages)
            response = await client.complete(self.config.model, dct, **kwargs)
            # Extract usage information
            usage = response.get("usage", {})
            return CompletionResult(
                content=response["choices"][0]["message"]["content"],
                model=response["model"],
                tool_calls=self._extract_tool_calls(response),
                metadata={"provider": "llm", "usage": usage},
                prompt_tokens=usage.get("prompt_tokens"),
                completion_tokens=usage.get("completion_tokens"),
                total_cost=0.0,  # llm library doesn't provide cost info
            )
        except Exception as exc:
            msg = f"LLMLib completion failed: {exc}"
            raise exceptions.LLMError(msg) from exc

    async def complete_stream(
        self,
        messages: list[Message],
        *,
        chunk_size: int | None = None,
        **kwargs: Unpack[LiteLLMCompletionParams],
    ) -> AsyncIterator[CompletionResult]:
        """Generate a streaming completion for the messages."""
        try:
            messages_dict = self._prepare_messages(messages)

            async for chunk in client.stream(
                self.config.model,
                messages_dict,
                **kwargs,
            ):
                if content := chunk["choices"][0]["delta"].get("content"):
                    yield CompletionResult(
                        content=content,
                        model=chunk["model"],
                        metadata={"chunk": True},
                    )

        except Exception as exc:
            msg = f"LLMLib streaming failed: {exc}"
            raise exceptions.LLMError(msg) from exc


if __name__ == "__main__":
    import asyncio

    import devtools

    async def test_provider():
        """Test the LLMLib provider."""
        # Create test config
        config = LLMConfig(model="gpt-3.5-turbo", temperature=0.7, max_tokens=1000)
        # Initialize provider
        provider = LLMLibProvider(config)
        print("\nProvider initialized with capabilities:")
        print(devtools.debug(provider._capabilities))
        # Test basic completion
        print("\nTesting basic completion:")
        msg_1 = Message(role="system", content="You are a helpful assistant.")
        msg_2 = Message(role="user", content="Write a haiku about coding.")
        result = await provider.complete([msg_1, msg_2])
        print(devtools.debug(result))
        # Test streaming
        print("\nTesting streaming:")
        messages = [Message(role="user", content="Count from 1 to 5.")]
        async for chunk in provider.complete_stream(messages):
            print(chunk.content, end="", flush=True)
        # Test vision if supported
        if not provider._capabilities.supports_vision:
            return
        print("\nTesting vision capabilities:")
        content = MessageContent(
            type="image_url",
            content="https://example.com/image.jpg",
            alt_text="An example image",
        )
        msg = Message(
            role="user", content="What's in this image?", content_items=[content]
        )
        vision_result = await provider.complete([msg])
        print(devtools.debug(vision_result))

    asyncio.run(test_provider())
