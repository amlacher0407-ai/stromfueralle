from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    admin_username: str
    admin_default_password: str

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
