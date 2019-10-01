from sqlalchemy import *

from ..core.database import *

class Redirection(Database.Base, ModelInterface):
    __tablename__ = "redirections"

    id = Column("id", Integer, primary_key = True)
    source = Column("source", String(255), index = True, nullable = False)
    target = Column("target", String(255), index = True, nullable = False)
