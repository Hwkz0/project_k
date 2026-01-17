"""AI provider integration endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.integrations.ai_providers import get_ai_provider, AIProviderType

router = APIRouter()


class ChatRequest(BaseModel):
    """Chat completion request."""
    
    provider: AIProviderType = AIProviderType.MOCK
    model: Optional[str] = None
    prompt: str
    max_tokens: int = 500


class ChatResponse(BaseModel):
    """Chat completion response."""
    
    provider: str
    model: str
    response: str
    usage: dict


@router.get("/providers")
def list_providers():
    """List available AI providers."""
    return {
        "providers": [
            {
                "id": "mock",
                "name": "Mock Provider",
                "description": "Mock AI provider for testing",
                "available": True,
            },
            {
                "id": "openai",
                "name": "OpenAI",
                "description": "OpenAI GPT models",
                "available": False,  # Set based on API key availability
            },
            {
                "id": "anthropic",
                "name": "Anthropic",
                "description": "Anthropic Claude models",
                "available": False,
            },
        ]
    }


@router.post("/chat", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Generate a chat completion using the specified AI provider."""
    try:
        provider = get_ai_provider(request.provider)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
    try:
        result = await provider.chat_completion(
            prompt=request.prompt,
            model=request.model,
            max_tokens=request.max_tokens,
        )
        
        return ChatResponse(
            provider=request.provider.value,
            model=result["model"],
            response=result["response"],
            usage=result["usage"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI provider error: {str(e)}",
        )


@router.get("/models/{provider}")
def list_provider_models(
    provider: AIProviderType,
):
    """List available models for a provider."""
    try:
        ai_provider = get_ai_provider(provider)
        return {"models": ai_provider.list_models()}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
