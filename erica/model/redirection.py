from sqlalchemy import *
from sqlalchemy.dialects.mysql import *

from ..core.database import *

class Redirection(Database.Base, ModelInterface):
    __tablename__ = "redirections"

    id = Column("id", Integer, primary_key = True)
    source = Column("source", VARCHAR(255, collation = "utf8_bin"), index = True, nullable = False)
    target = Column("target", VARCHAR(255, collation = "utf8_bin"), index = True, nullable = False)
