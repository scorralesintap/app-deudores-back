from functools import lru_cache
from typing import Literal
from zoneinfo import ZoneInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    ENVIRONMENT: Literal["development", "qa", "production"] = "development"
    DEBUG: bool
    TIMEZONE_OFFSET: int = -5

    FGA_API_BASE_URL: str | None = None
    FGA_API_KEY: str | None = None

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
