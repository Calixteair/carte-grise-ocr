from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql+psycopg2://user:password@db:5432/carte_grise_ocr_db"

    # Mistral AI settings
    MISTRAL_API_KEY: str = "your_mistral_api_key"

    # JWT settings
    SECRET_KEY: str = "super-secret-jwt-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis settings for Celery
    REDIS_BROKER_URL: str = "redis://redis:6379/0"
    REDIS_BACKEND_URL: str = "redis://redis:6379/1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
