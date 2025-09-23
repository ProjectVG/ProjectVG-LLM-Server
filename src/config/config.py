"""
Configuration Management
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application Settings"""

    # Server Settings
    SERVER_HOST: str = Field(default="0.0.0.0", env="SERVER_HOST")
    SERVER_PORT: int = Field(default=8080, env="SERVER_PORT")
    DEBUG: bool = Field(default=True, env="DEBUG")

    # OpenAI API Settings
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    DEFAULT_MODEL: str = Field(default="gpt-4o-mini", env="DEFAULT_MODEL")
    DEFAULT_TEMPERATURE: float = Field(default=0.7, env="DEFAULT_TEMPERATURE")
    DEFAULT_MAX_TOKENS: int = Field(default=1000, env="DEFAULT_MAX_TOKENS")

    # Logging Settings
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="logs/app.log", env="LOG_FILE")

    # CORS Settings
    CORS_ORIGINS: list = Field(default=["*"], env="CORS_ORIGINS")
    CORS_CREDENTIALS: bool = Field(default=True, env="CORS_CREDENTIALS")
    CORS_METHODS: list = Field(default=["*"], env="CORS_METHODS")
    CORS_HEADERS: list = Field(default=["*"], env="CORS_HEADERS")

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get application settings"""
    return settings

# 하위 호환성을 위한 전역 변수들
SERVER_PORT: int = settings.SERVER_PORT
SERVER_HOST: str = settings.SERVER_HOST
OPENAI_API_KEY: str = settings.OPENAI_API_KEY
DEFAULT_MODEL: str = settings.DEFAULT_MODEL
DEFAULT_TEMPERATURE: float = settings.DEFAULT_TEMPERATURE
DEFAULT_MAX_TOKENS: int = settings.DEFAULT_MAX_TOKENS
LOG_LEVEL: str = settings.LOG_LEVEL
LOG_FILE: str = settings.LOG_FILE 