from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_lifetime: int = 15
    refresh_token_lifetime: int = 15
    token_type_field: str = "type"
    access_token_type: str = "access"
    refresh_token_type: str = "refresh"


class Settings(BaseSettings):
    # App config
    ERROR_LOG_FILENAME: str
    STORAGE_LOCATION: Path = Path(BASE_DIR, "media")
    FILE_TYPES: list = ["image/jpeg", "image/png", "image/gif"]

    # Data Base config
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # Yandex ID configuration
    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str = "https://oauth.yandex.ru/verification_code"

    AUTH_JWT: AuthJWT = AuthJWT()

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()

DSN = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}"
    f"/{settings.POSTGRES_NAME}"
)
