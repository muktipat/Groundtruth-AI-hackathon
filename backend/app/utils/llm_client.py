"""LLM client wrapper for OpenAI."""
import json
from typing import Optional, Dict, Any
from openai import OpenAI
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LLMClient:
    """OpenAI client wrapper."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def query(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> str:
        """
        Query OpenAI API.
        
        Args:
            prompt: User message
            system_prompt: System context
            temperature: Model temperature
            max_tokens: Max tokens in response
            json_mode: Return JSON response
            
        Returns:
            Model response
        """
        temperature = temperature or settings.TEMPERATURE
        max_tokens = max_tokens or settings.MAX_TOKENS
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=settings.GPT_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"} if json_mode else None
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    def extract_json(self, text: str) -> Dict[str, Any]:
        """Extract JSON from response."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response")
            return {}


# Singleton instance
llm_client = LLMClient()
