import Logger
import Database

class EricaException():
    pass

def initialize():
    Logger.initialize()
    Database.initialize()

def finalize():
    Database.finalize()
