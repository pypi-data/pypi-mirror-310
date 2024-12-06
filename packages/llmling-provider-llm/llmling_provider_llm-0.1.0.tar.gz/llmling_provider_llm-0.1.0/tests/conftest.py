"""Pytest configuration and fixtures."""

from __future__ import annotations

import os

from llmling.llm.base import LLMConfig
import pytest

from llmling_provider_llm import provider


# Define test models based on environment
TEST_MODELS = (
    [pytest.param("smollm2:135m", id="smollm")]
    if os.getenv("CI")
    else [
        pytest.param("smollm2:135m", id="smollm"),
        pytest.param("gpt-3.5-turbo", id="gpt3"),
    ]
)


@pytest.fixture(params=TEST_MODELS)
def model_id(request: pytest.FixtureRequest) -> str:
    """Return a test model ID."""
    return request.param


@pytest.fixture
def test_config(model_id: str) -> LLMConfig:
    """Create a test LLM configuration."""
    return LLMConfig(
        model=model_id,
        temperature=0.7,
        max_tokens=1000,
    )


@pytest.fixture
def test_provider(test_config: LLMConfig) -> provider.LLMLibProvider:
    """Create a test provider instance."""
    return provider.LLMLibProvider(test_config)
