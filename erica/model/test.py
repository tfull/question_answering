from sqlalchemy import *

from ..core.database import Database

class Test(Database.Base):
    __tablename__ = "test"

    id = Column("id", Integer, primary_key = True)
    text = Column("text", String(16))
