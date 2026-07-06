from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    APP_NAME: str = "SISTECH NEXUS"
    APP_VERSION: str = "0.0.8-dev"

    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    FIRST_SUPERUSER_USERNAME: str = "admin"
    FIRST_SUPERUSER_EMAIL: str = "admin@sistech.local"
    FIRST_SUPERUSER_FULL_NAME: str = "System Administrator"
    FIRST_SUPERUSER_PASSWORD: str = "Admin@12345"

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        extra="ignore",
    )


settings = Settings()