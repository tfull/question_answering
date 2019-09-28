from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

from .config import Config

class Database:
    _URI = "mysql://%s:%s@%s/%s?charset=utf8" % (
        Config.get("database.user"),
        Config.get("database.password"),
        Config.get("database.host"),
        Config.get("database.dbname"),
    )

    Engine = create_engine(_URI, encoding = "utf-8", echo = False)

    Session = scoped_session(
        sessionmaker(
            autocommit = False,
            autoflush = False,
            bind = Engine
        )
    )

    Base = declarative_base()
    Base.query = Session.query_property()

# import MySQLdb

# from . import config as Config

# CONNECTIONS = None
# CURSORS = None

# def initialize():
#     global CONNECTIONS
#     global CURSORS

#     CONNECTIONS = []
#     CURSORS = []

#     new()

# def new():
#     global CONNECTIONS
#     global CURSORS

#     charset = "utf8"

#     config = Config.get("database")
#     connection = MySQLdb.connect(
#         user = config["user"],
#         passwd = config["password"],
#         host = config["host"],
#         db = config["dbname"],
#         charset = charset
#     )
#     cursor = connection.cursor(MySQLdb.cursors.DictCursor)

#     cursor.execute("SET NAMES {}".format(charset))
#     cursor.execute("SET CHARACTER SET {}".format(charset))
#     cursor.execute("SET character_set_connection={}".format(charset))

#     CONNECTIONS.append(connection)
#     CURSORS.append(cursor)

#     return len(CONNECTIONS)

# def finalize():
#     global CONNECTIONS
#     global CURSORS

#     for cursor in CURSORS:
#         cursor.close()

#     for connection in CONNECTIONS:
#         connection.close()

# def execute(query, parameters = None, *, handler_id = 1):
#     global CURSORS

#     cursor = CURSORS[handler_id - 1]

#     if parameters is None:
#         cursor.execute(query)
#     else:
#         cursor.execute(query, parameters)

# def fetchone(handler_id = 1):
#     global CURSORS

#     cursor = CURSORS[handler_id - 1]

#     return cursor.fetchone()

# def fetchall(handler_id = 1):
#     global CURSORS

#     cursor = CURSORS[handler_id - 1]

#     return cursor.fetchall()

# def commit(handler_id = 1):
#     global CONNECTIONS

#     connection = CONNECTIONS[handler_id - 1]

#     connection.commit()


# class Entry(Base):
#     __tablename__ = "entries"

#     id = Column("id", Integer, primary_key = True)
#     title = Column("title", String(255), index = True)
#     content = Column("content", MEDIUMTEXT)

# class Redirection(Base):
#     __tablename__ = "redirections"

#     id = Colum("id", Integer, primary_key = True)
#     source = Column("source", String(255), index = True)
#     target = Column("target", String(255), index = True)

# class PlainText(Base):
#     __tablename__ = "plain_texts"
