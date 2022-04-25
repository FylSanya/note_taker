from functools import lru_cache

from pydantic import BaseSettings
from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "notetaker"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "notetaker": {"handlers": ["default"], "level": LOG_LEVEL},
    }


class Config(BaseSettings):
    app_name: str = "Notetaker API"
    db_path: str
    db_name: str
    host: str
    port: int

    class Config:
        env_file = ".env"


@lru_cache()
def get_config():
    return Config()
