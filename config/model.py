from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAISettings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str
    model_config = SettingsConfigDict(env_file=".env")


openai_settings = OpenAISettings()
