from sqlalchemy import *
from sqlalchemy.dialects.mysql import *

from ...core.database import *

class ClassicWordCount(Database.Base, ModelInterface):
    __tablename__ = "classic_word_counts"

    id = Column("id", BigInteger, primary_key = True)
    entry_id = Column("entry_id", Integer, index = True, nullable = False)
    classic_word_id = Column("classic_word_id", BigInteger, index = True, nullable = False)
    count = Column("count", Integer, nullable = False)
