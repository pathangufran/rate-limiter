from functools import lru_cache
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):

    RULE_CACHE_TTL_SECONDS: int = 60
    
    app_name: str = "Distributed Rate Limiter"
    app_env: str = "development"
    debug: bool = False

    database_url: str
    redis_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    api_key_prefix: str = "rl_live_"
    api_key_cache_ttl_seconds: int = 300

    admin_email: str | None = None
    admin_password: str | None = None

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()