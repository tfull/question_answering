import sys

def split(arguments):
    import erica.base
    import erica.master

    erica.master.split()

def load(arguments):
    import erica.master
    import erica.base

    erica.base.initialize()
    erica.master.reset_database()
    erica.master.load_to_database()
    erica.base.finalize()

def read(arguments):
    pass

def insert_plain_text(arguments):
    import erica.master
    import erica.base

    erica.base.initialize()
    erica.master.insert_plain_text()
    erica.base.finalize()

def method1_build(arguments):
    import erica.base
    import erica.master
    import erica.brain.basic

    erica.base.initialize()
    erica.brain.basic.build()
    erica.base.finalize()

def method1_load(arguments):
    import erica.base
    import erica.master
    import erica.brain.basic

    inf = None
    sup = None

    if len(arguments) > 0:
        inf, sup = [int(x) for x in arguments[0].split(":")]

    erica.base.initialize()
    erica.brain.basic.load(inf, sup)
    erica.base.finalize()

def method1_ask(arguments):
    import erica.base
    import erica.master
    import erica.brain.basic

    erica.base.initialize()
    print(erica.brain.basic.ask(arguments[0]))
    erica.base.finalize()

if __name__ == '__main__':
    command = sys.argv[1]

    methods = {
        "split": split,
        "load": load,
        "insert_plain_text": insert_plain_text,
        "m1:build": method1_build,
        "m1:load": method1_load,
        "m1:ask": method1_ask,
        "read": read }
    
    methods[command](sys.argv[2:])
