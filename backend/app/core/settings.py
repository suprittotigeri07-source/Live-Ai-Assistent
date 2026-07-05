from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    DEBUG: bool
    HOST: str
    PORT: int

    LLM_PROVIDER: str

    OLLAMA_BASE_URL: str
    OLLAMA_API_KEY: str
    OLLAMA_MODEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()