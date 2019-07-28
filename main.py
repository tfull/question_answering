import sys

def split():
    import erica.base
    import erica.master

    erica.master.split()

def load():
    import erica.master
    import erica.base

    erica.base.initialize()
    erica.master.reset_database()
    erica.master.load_to_database()
    erica.base.finalize()

def read():
    pass

def insert_plain_text():
    import erica.master
    import erica.base

    erica.base.initialize()
    erica.master.insert_plain_text()
    erica.base.finalize()

def initialize_method1():
    import erica.base
    import erica.master
    import erica.brain
    erica.base.initialize()
    erica.brain.build()
    erica.brain.load()
    erica.base.finalize()

if __name__ == '__main__':
    command = sys.argv[1]

    methods = { "split": split, "load": load, "insert_plain_text": insert_plain_text, "m1:build": initialize_method1, "read": read }
    
    methods[command]()
