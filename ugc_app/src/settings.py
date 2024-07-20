from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    project_name: str = "ugc"

    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_db: str = "ugc"

    project_name: str = "ugc"
    jwt_public_key: bytes


settings = Settings()
