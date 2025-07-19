import asyncio
import logging
import typing
from abc import ABC, abstractmethod

from topsongs.io import server


class IoManager(ABC):
    @property
    @abstractmethod
    def redirect_url(self) -> str:
        pass

    @abstractmethod
    def listen(self) -> str:
        pass

    @abstractmethod
    def info(self, *args, **kwargs):
        pass

    @abstractmethod
    def warning(self, *args, **kwargs):
        pass

    @abstractmethod
    def error(self, *args, **kwargs):
        pass

    @abstractmethod
    def critical(self, *args, **kwargs):
        pass

class ColorFormatter(logging.Formatter):
    LOG_COLORS: typing.ClassVar[dict[str, str]] = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[41m', # Red background
        'RESET': '\033[0m'      # Reset color
    }
    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        color = self.LOG_COLORS.get(levelname, '')
        reset = self.LOG_COLORS['RESET']
        record.levelname = f"{color}{levelname}{reset}"
        record.msg = f"{color}{record.msg}{reset}"
        return super().format(record)

def create_logger(name: str) -> logging.Logger:
    logger = logging.Logger(name)
    handler = logging.StreamHandler()
    formatter = ColorFormatter(
        '[%(asctime)s] %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger

class DefaultLoggingMixin:
    logger = create_logger("default")

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.logger.critical(*args, **kwargs)

class CliManager(DefaultLoggingMixin):
    def __init__(self):
        self.simple_server = server.SimpleServer()

    @property
    def redirect_url(self) -> str:
        return self.simple_server.url

    def listen(self) -> str:
        """Listens on redirect_url for a request containing the token/code."""
        return asyncio.run(self.simple_server.run())


