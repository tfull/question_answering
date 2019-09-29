from sqlalchemy import *
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from ..core.database import Database

class Entry(Database.Base):
    __tablename__ = "entries"

    id = Column("id", Integer, primary_key = True)
    title = Column("title", String(255), index = True, nullable = False)
    content = Column("content", MEDIUMTEXT, nullable = False)
