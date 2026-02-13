from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str

    # Mistral AI settings
    MISTRAL_API_KEY: str

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis settings for Celery
    REDIS_BROKER_URL: str
    REDIS_BACKEND_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
