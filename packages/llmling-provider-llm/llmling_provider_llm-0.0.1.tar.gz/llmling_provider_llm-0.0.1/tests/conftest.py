"""Tests for the LLMling LLM provider."""

from __future__ import annotations

from llmling.llm.base import LLMConfig, Message, MessageContent
import pytest

from llmling_provider_llm import client, provider


# Define test models
TEST_MODELS = [
    pytest.param("smollm2:135m", id="smollm"),
    pytest.param("gpt-3.5-turbo", id="gpt3"),
]


@pytest.mark.parametrize("model_id", TEST_MODELS)
class TestLLMProvider:
    """Test suite for LLM provider."""

    @pytest.fixture
    def test_config(self, model_id: str) -> LLMConfig:
        """Create a test LLM configuration."""
        return LLMConfig(
            model=model_id,
            temperature=0.7,
            max_tokens=1000,
        )

    @pytest.fixture
    def test_provider(self, test_config: LLMConfig) -> provider.LLMLibProvider:
        """Create a test provider instance."""
        return provider.LLMLibProvider(test_config)

    @pytest.mark.asyncio
    async def test_model_capabilities(self, model_id: str) -> None:
        """Test retrieving model capabilities."""
        capabilities = client.get_model_info(model_id)
        assert capabilities.key == model_id
        assert capabilities.litellm_provider == "llm"
        assert capabilities.mode == "chat"

    @pytest.mark.asyncio
    async def test_basic_completion(
        self,
        test_provider: provider.LLMLibProvider,
    ) -> None:
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
    async def test_streaming_completion(
        self,
        test_provider: provider.LLMLibProvider,
    ) -> None:
        """Test streaming completion functionality."""
        messages = [
            Message(role="user", content="Count from 1 to 3."),
        ]

        chunks = []
        async for chunk in test_provider.complete_stream(messages):
            assert chunk.content is not None
            chunks.append(chunk.content)

        complete_response = "".join(chunks)
        assert len(complete_response) > 0

    @pytest.mark.asyncio
    async def test_vision_capability(
        self,
        test_provider: provider.LLMLibProvider,
    ) -> None:
        """Test vision capabilities if supported."""
        if not test_provider._capabilities.supports_vision:
            pytest.skip("Vision capabilities not supported by this model")

        content_item = MessageContent(
            type="image_url",
            content="https://example.com/test.jpg",
            alt_text="A test image",
        )

        message = Message(
            role="user",
            content="What's in this image?",
            content_items=[content_item],
        )

        result = await test_provider.complete([message])
        assert result.content is not None
        assert len(result.content) > 0

    def test_message_preparation(
        self,
        test_provider: provider.LLMLibProvider,
    ) -> None:
        """Test message preparation logic."""
        messages = [
            Message(
                role="user",
                content="Test message",
                content_items=[
                    MessageContent(
                        type="image_url",
                        content="https://example.com/test.jpg",
                        alt_text="Test image",
                    ),
                ],
            ),
        ]

        prepared = test_provider._prepare_messages(messages)

        assert len(prepared) == 1
        assert prepared[0]["role"] == "user"
        assert prepared[0]["content"] == "Test message"
        assert "content_items" in prepared[0]
        assert len(prepared[0]["content_items"]) == 1
        assert prepared[0]["content_items"][0]["type"] == "image_url"


if __name__ == "__main__":
    pytest.main(["-vv", __file__])
