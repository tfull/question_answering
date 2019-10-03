from ..core import *
from ..model import *
from ..model.classic import *

class BatchMigrate:
    @classmethod
    def main(cls):
        Database.Base.metadata.create_all(Database.Engine)        
