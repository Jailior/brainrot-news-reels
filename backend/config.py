"""
Configuration management for the backend application.

This module handles all environment variables, API keys, database connection strings,
and application settings. It provides a centralized configuration object that can be
imported throughout the application.

Interactions:
- Used by database.py for connection strings
- Used by all service classes for API keys (NewsAPI, Claude, ElevenLabs)
- Used by storage_service.py for S3 bucket configuration
- Used by main.py for application settings
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All sensitive values (API keys, database passwords) should be set via
    environment variables, not hardcoded in this file.
    """
    
    # Database Configuration
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/brainrot_news_reels"
    )
    
    # NewsAPI Configuration
    newsapi_key: Optional[str] = os.getenv("NEWSAPI_KEY")
    newsapi_base_url: str = os.getenv("NEWSAPI_BASE_URL", "https://newsapi.org/v2")
    
    # Claude API Configuration
    open_router_api_key: Optional[str] = os.getenv("LLM_API_KEY")
    openrouter_base_url: Optional[str] = os.getenv("OPENROUTER_URL")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-5.2")
    
    # ElevenLabs API Configuration
    elevenlabs_api_key: Optional[str] = os.getenv("ELEVENLABS_API_KEY")
    elevenlabs_base_url: str = os.getenv("ELEVENLABS_BASE_URL", "https://api.elevenlabs.io/v1")
    elevenlabs_voice_id: str = os.getenv("ELEVENLABS_VOICE_ID", "default")
    
    # AWS S3 Configuration
    aws_access_key_id: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    s3_bucket_name: str = os.getenv("S3_BUCKET_NAME", "brainrot-news-reels")
    s3_endpoint_url: Optional[str] = os.getenv("S3_ENDPOINT_URL")  # For Cloudflare R2 or other S3-compatible services
    
    # Application Settings
    app_name: str = "Brainrot News Reels API"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Temporary File Settings
    temp_dir: str = os.getenv("TEMP_DIR", "/tmp")
    
    # API Settings
    api_prefix: str = "/api"
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False
    
    # Global constants
    MAX_CHAR_TO_DISPLAY: int = 100

load_dotenv()

# Global settings instance
settings = Settings()

