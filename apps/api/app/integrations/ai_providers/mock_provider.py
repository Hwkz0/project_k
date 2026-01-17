"""Mock AI Provider for testing."""

import random
from typing import Any, Dict, List, Optional

from app.integrations.ai_providers.base import AIProvider, AIProviderType


class MockAIProvider(AIProvider):
    """Mock AI provider for testing and development."""
    
    @property
    def name(self) -> str:
        return "Mock AI Provider"
    
    @property
    def provider_type(self) -> AIProviderType:
        return AIProviderType.MOCK
    
    def list_models(self) -> List[str]:
        return [
            "mock-gpt-small",
            "mock-gpt-medium",
            "mock-gpt-large",
        ]
    
    async def chat_completion(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Generate a mock chat completion."""
        model = model or "mock-gpt-medium"
        
        # Generate a mock response based on the prompt
        responses = [
            f"This is a mock response to your prompt about: {prompt[:50]}...",
            "I'm a mock AI assistant. In a real implementation, this would be powered by an actual AI model.",
            f"Mock response generated for testing purposes. Your prompt was {len(prompt)} characters long.",
            "Here's a helpful mock response! In production, connect a real AI provider for actual intelligence.",
            f"Processing your request... [MOCK MODE] The model '{model}' would normally respond here.",
        ]
        
        response = random.choice(responses)
        
        # Simulate token usage
        prompt_tokens = len(prompt.split())
        completion_tokens = len(response.split())
        
        return {
            "response": response,
            "model": model,
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            },
        }
    
    async def generate_embedding(
        self,
        text: str,
        model: Optional[str] = None,
    ) -> List[float]:
        """Generate a mock embedding."""
        # Generate a mock embedding (1536 dimensions like OpenAI ada-002)
        random.seed(hash(text))
        return [random.uniform(-1, 1) for _ in range(1536)]
    
    def is_available(self) -> bool:
        return True  # Mock provider is always available
