"""Configuration management for AuraCX backend."""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""
    
    # API Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Model Configuration
    GPT_MODEL: str = "gpt-4-turbo-preview"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2048
    
    # API Configuration
    API_TITLE: str = "AuraCX API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Hyper-Personalized Customer Experience Automation"
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]
    
    # Confidence Threshold
    CONFIDENCE_THRESHOLD: float = 0.7
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT == "production"


settings = Settings()
