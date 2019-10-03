from sqlalchemy import *
from sqlalchemy.dialects.mysql import *

from ...core.database import *

class ClassicWord(Database.Base, ModelInterface):
    __tablename__ = "classic_words"

    id = Column("id", BigInteger, primary_key = True)
    word = Column("word", VARCHAR(255, collation = "utf8_bin"), index = True, nullable = False)
    document_frequency = Column("document_frequency", Integer, nullable = False)
