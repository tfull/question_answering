import Logger
import Database

def initialize():
    Logger.initialize()
    Database.initialize()

def finalize():
    Database.finalize()
