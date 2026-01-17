"""AI Provider integrations."""

from app.integrations.ai_providers.base import AIProvider, AIProviderType
from app.integrations.ai_providers.mock_provider import MockAIProvider
from app.integrations.ai_providers.openai_provider import OpenAIProvider
from app.integrations.ai_providers.anthropic_provider import AnthropicProvider


def get_ai_provider(provider_type: AIProviderType) -> AIProvider:
    """Get an AI provider instance by type."""
    providers = {
        AIProviderType.MOCK: MockAIProvider,
        AIProviderType.OPENAI: OpenAIProvider,
        AIProviderType.ANTHROPIC: AnthropicProvider,
    }
    
    provider_class = providers.get(provider_type)
    if not provider_class:
        raise ValueError(f"Unknown provider type: {provider_type}")
    
    return provider_class()


__all__ = [
    "AIProvider",
    "AIProviderType",
    "get_ai_provider",
    "MockAIProvider",
    "OpenAIProvider",
    "AnthropicProvider",
]
