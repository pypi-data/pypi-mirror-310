from __future__ import annotations

__version__ = "0.0.1"

from llmling.llm.registry import ProviderFactory, default_registry
from llmling_provider_llm.provider import LLMLibProvider


def register_provider() -> None:
    """Register this provider with LLMling."""
    default_registry.register("llm", ProviderFactory(LLMLibProvider))


__all__ = ["LLMLibProvider", "register_provider"]
