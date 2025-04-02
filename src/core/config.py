from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App config
    AUTH_SECRET: str
    ERROR_LOG_FILENAME: str

    # Data Base config
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # e-mail config
    SMTP_PASSWORD: str
    SMTP_USER: str
    SMTP_HOST: str
    SMTP_PORT: str

    # Redis config
    REDIS_HOST: str
    REDIS_PORT: str

    # Test Data Base config
    DB_HOST_TEST: str
    DB_PORT_TEST: str
    DB_NAME_TEST: str
    DB_USER_TEST: str
    DB_PASS_TEST: str

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()

DSN = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}"
    f"/{settings.POSTGRES_NAME}"
)
DATABASE_URL_TEST = (
    f"postgresql+asyncpg://{settings.DB_USER_TEST}:{settings.DB_PASS_TEST}"
    f"@{settings.DB_HOST_TEST}:{settings.DB_PORT_TEST}/{settings.DB_NAME_TEST}"
)
