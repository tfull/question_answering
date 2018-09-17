import os
import File

PATH = os.path.dirname(os.path.abspath(__file__)) + "/../config.yml"
DATA = None

def load():
    global DATA
    assert os.path.isfile(PATH), "file {} does not exist".format(PATH)
    DATA = File.load_yaml(PATH)
    print(DATA)

def get(key):
    if DATA is None:
        raise Exception("config is not loaded")
    return DATA[key]
