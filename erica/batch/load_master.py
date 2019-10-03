from ..master import *

class BatchLoadMaster:
    @classmethod
    def main(cls):
        MasterBuilder.split()
        MasterBuilder.load_entries()
        MasterBuilder.load_plain_texts()
