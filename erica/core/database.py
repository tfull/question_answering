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
