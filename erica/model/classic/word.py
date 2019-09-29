from sqlalchemy import *

from ...core.database import Database

class ClassicWord(Database.Base):
    __tablename__ = "classic_words"

    id = Column("id", BigInteger, primary_key = True)
    word = Column("word", String(255), index = True, nullable = False)
