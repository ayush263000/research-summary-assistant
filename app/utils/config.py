"""
Configuration management using Pydantic settings
"""

from pydantic import BaseSettings, Field
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # Google Gemini Configuration
    GOOGLE_API_KEY: str = Field(..., env="GOOGLE_API_KEY")
    GEMINI_MODEL: str = Field(default="gemini-1.5-flash", env="GEMINI_MODEL")
    MAX_TOKENS: int = Field(default=8192, env="MAX_TOKENS")
    TEMPERATURE: float = Field(default=0.1, env="TEMPERATURE")
    
    # Database Configuration
    DATABASE_URL: str = Field(default="sqlite:///./data/app.db", env="DATABASE_URL")
    
    # File Upload Configuration
    UPLOAD_DIR: str = Field(default="./data/uploads", env="UPLOAD_DIR")
    MAX_FILE_SIZE: str = Field(default="50MB", env="MAX_FILE_SIZE")
    ALLOWED_EXTENSIONS: str = Field(default="pdf,txt", env="ALLOWED_EXTENSIONS")
    
    # Application Configuration
    DEBUG: bool = Field(default=True, env="DEBUG")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Server Configuration
    HOST: str = Field(default="localhost", env="HOST")
    PORT: int = Field(default=8501, env="PORT")
    API_PORT: int = Field(default=8000, env="API_PORT")
    
    # Security Configuration
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", env="SECRET_KEY")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    def get_max_file_size_bytes(self) -> int:
        """Convert MAX_FILE_SIZE string to bytes"""
        size_str = self.MAX_FILE_SIZE.upper()
        if size_str.endswith('MB'):
            return int(size_str[:-2]) * 1024 * 1024
        elif size_str.endswith('KB'):
            return int(size_str[:-2]) * 1024
        elif size_str.endswith('GB'):
            return int(size_str[:-2]) * 1024 * 1024 * 1024
        else:
            return int(size_str)
    
    def get_allowed_extensions(self) -> list:
        """Get list of allowed file extensions"""
        return [ext.strip().lower() for ext in self.ALLOWED_EXTENSIONS.split(',')]

# Global settings instance
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """
    Get application settings (singleton pattern)
    """
    global _settings
    if _settings is None:
        _settings = Settings()
        
        # Ensure directories exist
        Path(_settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path(_settings.DATABASE_URL.replace("sqlite:///", "")).parent.mkdir(parents=True, exist_ok=True)
    
    return _settings

def reload_settings():
    """
    Reload settings (useful for testing)
    """
    global _settings
    _settings = None
    return get_settings()
