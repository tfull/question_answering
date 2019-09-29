import logging

from .config import Config

class Logger:
    _FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
    _LOGGER = None

    @classmethod
    def initialize(cls):
        filename = Config.get("log.path")
        level = cls.logging_level(Config.get("log.level"))

        logging.basicConfig(filename = filename, level = level, format = cls._FORMAT)
        cls._LOGGER = logging.getLogger(__name__)

    @classmethod
    def logging_level(cls, argument):
        argument = argument.lower()

        if argument == "critical":
            return logging.CRITICAL
        elif argument == "error":
            return logging.ERROR
        elif argument == "warning":
            return logging.WARNING
        elif argument == "info":
            return logging.INFO
        elif argument == "debug":
            return logging.DEBUG
        elif argument == "notset":
            return logging.NOTSET
        else:
            raise Exception("no such log level")

    @classmethod
    def validate(cls):
        if cls._LOGGER is None:
            cls.initialize()

    @classmethod
    def critical(cls, message):
        cls.validate()
        cls._LOGGER.critical(message)

    @classmethod
    def error(cls, message):
        cls.validate()
        cls._LOGGER.error(message)

    @classmethod
    def warning(cls, message):
        cls.validate()
        cls._LOGGER.warning(message)

    @classmethod
    def info(cls, message):
        cls.validate()
        cls._LOGGER.info(message)

    @classmethod
    def debug(cls, message):
        cls.validate()
        cls._LOGGER.debug(message)
