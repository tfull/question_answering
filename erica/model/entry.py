import random
from sqlalchemy import *
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import *

from ..core.database import *

class Entry(Database.Base, ModelInterface):
    __tablename__ = "entries"

    id = Column("id", Integer, primary_key = True)
    title = Column("title", VARCHAR(255, collation = "utf8_bin"), index = True, nullable = False)
    content = Column("content", MEDIUMTEXT(collation = "utf8_bin"), nullable = False)

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

    @classmethod
    def sample(cls, count = None):
        result = Session.query(func.max(cls.id).label("max_id")).one()
        max_id = result.max_id

        if count is None:
            target_id = random.randint(1, max_id)
            return cls.find(target_id)
        else:
            id_list = random.sample(range(1, max_id + 1), count)
            return cls.find(id_list)
