from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    project_name: str = "my_service"
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_base: str = 'TestBase'

    pg_host: str = "127.0.0.1"
    pg_port: int = 5432
    pg_user: str = "my_user"
    pg_database: str = "my_database"
    pg_password: str = "123qwe"


settings = Settings()