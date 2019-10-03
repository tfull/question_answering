from sqlalchemy import *
from sqlalchemy.dialects.mysql import *

from ..core.database import *

class PlainText(Database.Base, ModelInterface):
    __tablename__ = "plain_texts"

    id = Column("id", Integer, primary_key = True)
    entry_id = Column("entry_id", Integer, index = True, nullable = False)
    text = Column("text", MEDIUMTEXT(collation = "utf8_bin"), nullable = False)
