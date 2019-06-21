import MySQLdb

from . import config as Config

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

def execute(query, parameters = None):
    global CURSOR

    if parameters is None:
        CURSOR.execute(query)
    else:
        CURSOR.execute(query, parameters)

def fetchone():
    global CURSOR

    return CURSOR.fetchone()

def fetchall():
    global CURSOR

    return CURSOR.fetchall()

def commit():
    global CONNECTION

    CONNECTION.commit()
