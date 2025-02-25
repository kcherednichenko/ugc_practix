from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    project_name: str = "ugc"

    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_db: str = "ugc"

    jwt_public_key: bytes

    sentry_dsn: str
    log_file: str

    enable_sentry: bool = False


settings = Settings()  # type: ignore[call-arg]
