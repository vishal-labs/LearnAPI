from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str = "testdb"
    KEY: str
    SMTP_PASSWORD: str = ""
    REFRESH_KEY: str = "super_secret_refresh_key" # default value for now

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
