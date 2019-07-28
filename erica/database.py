import MySQLdb

from . import config as Config

CONNECTIONS = None
CURSORS = None

def initialize():
    global CONNECTIONS
    global CURSORS

    CONNECTIONS = []
    CURSORS = []

    new()

def new():
    global CONNECTIONS
    global CURSORS

    charset = "utf8"

    config = Config.get("database")
    connection = MySQLdb.connect(
        user = config["user"],
        passwd = config["password"],
        host = config["host"],
        db = config["dbname"],
        charset = charset
    )
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SET NAMES {}".format(charset))
    cursor.execute("SET CHARACTER SET {}".format(charset))
    cursor.execute("SET character_set_connection={}".format(charset))

    CONNECTIONS.append(connection)
    CURSORS.append(cursor)

    return len(CONNECTIONS)

def finalize():
    global CONNECTIONS
    global CURSORS

    for cursor in CURSORS:
        cursor.close()

    for connection in CONNECTIONS:
        connection.close()

def execute(query, parameters = None, *, handler_id = 1):
    global CURSORS

    cursor = CURSORS[handler_id - 1]

    if parameters is None:
        cursor.execute(query)
    else:
        cursor.execute(query, parameters)

def fetchone(handler_id = 1):
    global CURSORS

    cursor = CURSORS[handler_id - 1]

    return cursor.fetchone()

def fetchall(handler_id = 1):
    global CURSORS

    cursor = CURSORS[handler_id - 1]

    return cursor.fetchall()

def commit(handler_id = 1):
    global CONNECTIONS

    connection = CONNECTIONS[handler_id - 1]

    connection.commit()
