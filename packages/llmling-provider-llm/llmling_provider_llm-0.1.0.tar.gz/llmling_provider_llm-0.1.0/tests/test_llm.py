"""Tests for the LLMling LLM provider."""

from __future__ import annotations

import asyncio

from llmling.core import exceptions
from llmling.llm.base import LLMConfig, Message, MessageContent
import pytest

from llmling_provider_llm import client, provider
from tests.conftest import TEST_MODELS


@pytest.mark.asyncio
@pytest.mark.parametrize("model_id", TEST_MODELS)
async def test_model_capabilities(model_id: str) -> None:
    """Test retrieving model capabilities."""
    capabilities = client.get_model_info(model_id)
    assert capabilities.key == model_id
    assert capabilities.litellm_provider == "llm"
    assert capabilities.mode == "chat"


@pytest.mark.asyncio
async def test_basic_completion(test_provider: provider.LLMLibProvider) -> None:
    """Test basic completion functionality."""
    messages = [
        Message(role="system", content="You are a helpful assistant."),
        Message(role="user", content="Write a one-word greeting."),
    ]
    result = await test_provider.complete(messages)
    assert result.content is not None
    assert isinstance(result.content, str)
    assert len(result.content) > 0
    assert result.model == test_provider.config.model


@pytest.mark.asyncio
async def test_streaming_completion(test_provider: provider.LLMLibProvider) -> None:
    """Test streaming completion functionality."""
    messages = [
        Message(role="user", content="Count from 1 to 3."),
    ]

    chunks: list[str] = []
    async for chunk in test_provider.complete_stream(messages):
        assert chunk.content is not None
        chunks.append(chunk.content)

    complete_response = "".join(chunks)
    assert len(complete_response) > 0


@pytest.mark.asyncio
async def test_vision_capability(
    test_provider: provider.LLMLibProvider,
) -> None:
    """Test vision capabilities if supported."""
    if not test_provider._capabilities.supports_vision:
        pytest.skip("Vision capabilities not supported by this model")

    url = "https://example.com/test.jpg"
    content_item = MessageContent(type="image_url", content=url, alt_text="A test image")
    items = [content_item]
    message = Message(role="user", content="What's in this image?", content_items=items)
    result = await test_provider.complete([message])
    assert result.content is not None
    assert len(result.content) > 0


def test_message_preparation(test_provider: provider.LLMLibProvider) -> None:
    """Test message preparation logic."""
    url = "https://example.com/test.jpg"
    content = MessageContent(type="image_url", content=url, alt_text="Test image")
    messages = [Message(role="user", content="Test message", content_items=[content])]
    prepared = test_provider._prepare_messages(messages)

    assert len(prepared) == 1
    assert prepared[0]["role"] == "user"
    assert prepared[0]["content"] == "Test message"
    assert "content_items" in prepared[0]
    assert len(prepared[0]["content_items"]) == 1
    assert prepared[0]["content_items"][0]["type"] == "image_url"


@pytest.mark.asyncio
@pytest.mark.parametrize("model_id", TEST_MODELS)
async def test_long_conversation(model_id: str) -> None:
    """Test handling of multi-turn conversations."""
    config = LLMConfig(model=model_id)
    provider_instance = provider.LLMLibProvider(config)

    messages = [
        Message(role="system", content="You are a helpful assistant."),
        Message(role="user", content="What is 2+2?"),
        Message(role="assistant", content="4"),
        Message(role="user", content="Multiply that by 3"),
    ]

    result = await provider_instance.complete(messages)
    assert result.content is not None
    assert len(result.content) > 0


@pytest.mark.asyncio
@pytest.mark.parametrize("model_id", TEST_MODELS)
async def test_streaming_cancellation(model_id: str) -> None:
    """Test that streaming can be cancelled midway."""
    config = LLMConfig(model=model_id)
    provider_instance = provider.LLMLibProvider(config)

    msg = "Count from 1 to 1000 very slowly, number by number."
    messages = [Message(role="user", content=msg)]
    chunks_received = 0

    try:
        async for _chunk in provider_instance.complete_stream(messages):
            chunks_received += 1
            if chunks_received >= 5:  # noqa: PLR2004
                break
    finally:
        await asyncio.sleep(0.1)

    assert chunks_received >= 1


@pytest.mark.asyncio
@pytest.mark.parametrize("model_id", TEST_MODELS)
async def test_concurrent_requests(model_id: str) -> None:
    """Test handling multiple concurrent requests."""
    config = LLMConfig(model=model_id)
    provider_instance = provider.LLMLibProvider(config)

    messages = [Message(role="user", content="Say 'hello'")]
    num_requests = 3
    results = await asyncio.gather(*[
        provider_instance.complete(messages) for _ in range(num_requests)
    ])

    assert len(results) == num_requests
    assert all(r.content is not None for r in results)


@pytest.mark.parametrize(
    "invalid_model_id",
    [
        pytest.param("nonexistent-model", id="nonexistent"),
        pytest.param("", id="empty"),
        pytest.param("invalid:format:model", id="invalid_format"),
    ],
)
def test_invalid_model_initialization(invalid_model_id: str) -> None:
    """Test that provider properly handles invalid model initialization."""
    config = LLMConfig(model=invalid_model_id)

    with pytest.raises((exceptions.LLMError, ValueError)):
        provider.LLMLibProvider(config)


if __name__ == "__main__":
    pytest.main(["-vv", __file__])
