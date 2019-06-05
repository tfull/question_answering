import os
import File

PATH = os.path.dirname(os.path.abspath(__file__)) + "/../config.yml"
DATA = None

def load():
    global DATA
    if DATA is not None:
        return
    assert os.path.isfile(PATH), "file {} does not exist".format(PATH)
    DATA = File.load_yaml(PATH)

def get(key):
    global DATA
    if DATA is None:
        load()
    data = DATA
    for k in key.split("."):
        data = data[k]
    return data
