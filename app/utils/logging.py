from logging.config import dictConfig
import logging

from app.config import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("notetaker")
