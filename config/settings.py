from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MILVUS_HOST: str
    MILVUS_PORT: int
    MILVUS_DISK_INFO: str

    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int

    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str

    ZHIPU_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
