"""Base AI Provider interface."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional


class AIProviderType(str, Enum):
    """Available AI provider types."""
    MOCK = "mock"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name."""
        pass
    
    @property
    @abstractmethod
    def provider_type(self) -> AIProviderType:
        """Provider type enum."""
        pass
    
    @abstractmethod
    def list_models(self) -> List[str]:
        """List available models for this provider."""
        pass
    
    @abstractmethod
    async def chat_completion(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Generate a chat completion.
        
        Args:
            prompt: The input prompt
            model: The model to use (provider-specific)
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Dict with 'response', 'model', and 'usage' keys
        """
        pass
    
    @abstractmethod
    async def generate_embedding(
        self,
        text: str,
        model: Optional[str] = None,
    ) -> List[float]:
        """
        Generate an embedding for the given text.
        
        Args:
            text: The input text
            model: The embedding model to use
        
        Returns:
            List of floats representing the embedding
        """
        pass
    
    def is_available(self) -> bool:
        """Check if this provider is available (has API key, etc)."""
        return True
