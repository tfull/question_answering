from sqlalchemy import *

from ..core.database import Database

class Redirection(Database.Base):
    __tablename__ = "redirections"

    id = Column("id", Integer, primary_key = True)
    source = Column("source", String(255), index = True)
    target = Column("target", String(255), index = True)
