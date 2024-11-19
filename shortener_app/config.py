from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str
    base_url: str
    redis_broker_url: str
    redis_backend_url: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
