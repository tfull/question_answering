import logging

import Config

LOGGER = None

FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"

def initialize():
    global LOGGER
    global FORMAT

    filename = Config.get("log.path")
    level = logging_level(Config.get("log.level"))

    logging.basicConfig(filename = filename, level = level, format = FORMAT)
    LOGGER = logging.getLogger(__name__)

def logging_level(argument):
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

def critical(message):
    LOGGER.critical(message)

def error(message):
    LOGGER.error(message)

def warning(message):
    LOGGER.warning(message)

def info(message):
    LOGGER.info(message)

def debug(message):
    LOGGER.debug(message)
