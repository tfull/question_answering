from erica.core import *
from erica.model import *
from erica.master import *

# Database.Base.metadata.create_all(Database.Engine)

# record = Database.Session.query(Entry).filter_by(id = 10).first()

# print(type(record))

MasterBuilder.load_plain_texts()
