from sqlalchemy import *
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from ..core.database import *

class Entry(Database.Base, ModelInterface):
    __tablename__ = "entries"

    id = Column("id", Integer, primary_key = True)
    title = Column("title", String(255), index = True, nullable = False)
    content = Column("content", MEDIUMTEXT, nullable = False)

    @classmethod
    def id_to_title(cls, item):
        if type(item) == int:
            return Session.query(cls.title).filter(cls.id == item).one().title
        else:
            entries = Session.query(cls.id, cls.title).filter(cls.id.in_(item)).all()
            title_map = { entry.id: entry.title for entry in entries }

            try:
                return [title_map[record_id] for record_id in item]
            except KeyError:
                raise DatabaseError("invalid id included")
