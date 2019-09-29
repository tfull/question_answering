from sqlalchemy import *
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from ..core.database import Database

class PlainText(Database.Base):
    __tablename__ = "plain_texts"

    id = Column("id", Integer, primary_key = True)
    entry_id = Column("entry_id", Integer, index = True, nullable = False)
    text = Column("text", MEDIUMTEXT, nullable = False)
