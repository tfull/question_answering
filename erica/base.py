from . import logger as Logger
from . import database as Database

def initialize():
    Logger.initialize()
    Database.initialize()

def finalize():
    Database.finalize()
