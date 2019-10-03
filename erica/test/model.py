from ..model import *

class TestModel:
    @classmethod
    def debug(cls):
        for title in Entry.id_to_title([4,2,3]):
            print(title)
