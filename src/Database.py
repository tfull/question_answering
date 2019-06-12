import MySQLdb

import Config

CONNECTION = None
CURSOR = None

def initialize():
    global CONNECTION
    global CURSOR

    config = Config.get("database")
    CONNECTION = MySQLdb.connect(
        user = config["user"],
        passwd = config["password"],
        host = config["host"],
        db = config["dbname"],
        charset = config["charset"]
    )
    CURSOR = CONNECTION.cursor(MySQLdb.cursors.DictCursor)

def finalize():
    global CONNECTION
    global CURSOR

    CURSOR.close()
    CONNECTION.close()

def execute(query, parameters):
    global CURSOR

    CURSOR.execute(query, parameters)

def commit():
    global CONNECTION

    CONNECTION.commit()

# class MySQLHandler:
#     def __init__(self, config):
#         self.config = config
#         self.connection = None
#         self.cursor = None

#     def connect(self):
#         config = self.config
#         self.connection = MySQLdb.connect(user=config["user"], passwd=config["password"], host=config["host"], db=config["dbname"], charset="utf8mb4")
#         self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

#     def close(self):
#         self.cursor.close()
#         self.connection.close()
