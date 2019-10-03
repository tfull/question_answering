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

    Engine = create_engine(_URI, encoding = "utf8", echo = False)

    Session = scoped_session(
        sessionmaker(
            autocommit = False,
            autoflush = False,
            bind = Engine
        )
    )

    Base = declarative_base()
    Base.query = Session.query_property()


class DatabaseError(Exception):
    pass


Session = Database.Session


class ModelInterface:
    @classmethod
    def find(cls, item):
        if type(item) == int:
            return Session.query(cls).filter(cls.id == item).one()
        else:
            entries = Session.query(cls).filter(cls.id.in_(item)).all()
            entry_map = { entry.id: entry for entry in entries }

            try:
                return [entry_map[record_id] for record_id in item]
            except KeyError as e:
                raise DatabaseError("invalid id included")
