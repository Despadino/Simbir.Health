from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from yarl import URL
from enum import Enum
from app.logger import logger



class LogLevel(str, Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"

class Settings(BaseSettings):

    log_level: LogLevel = LogLevel.INFO


    POSTGRES_HOST: str = "simbir-health-db"
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str 

    SECRET_KEY: str
    ALGORITHM: str
    access_token_expire_minutes: int
    
    @property
    def db_url(self) -> URL:
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=f"/{self.POSTGRES_DB}",
        )
    
    @property
    def db_url_alembic(self) -> URL:
        return URL.build(
            scheme="postgresql+asyncpg",
            host="127.0.0.1",
            port=5434,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=f"/{self.POSTGRES_DB}",
        )



    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
