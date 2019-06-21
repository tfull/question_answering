import os

from . import file as File

PATH = os.path.dirname(os.path.abspath(__file__)) + "/../config.yml"
VALUES = None
ENVIRONMENTS = None
TYPES = None
LOADED = False

class ConfigError(Exception):
    pass

def get_from_key(data, key, must = False):
    for k in key.split("."):
        if k not in data:
            raise ConfigError("field {} does not exist".format(key))

        data = data[k]

    return data

def load():
    global LOADED
    global PATH
    global VALUES
    global ENVIRONMENTS
    global TYPES

    if LOADED:
        return

    if not os.path.isfile(PATH):
        raise ConfigError("file {} does not exist".format(PATH))

    data = File.load_yaml(PATH)

    if "values" in data:
        VALUES = data["values"]
    else:
        raise ConfigError("values not found")

    if "environments" in data:
        ENVIRONMENTS = data["environments"]
    else:
        raise ConfigError("environments not found")

    if "types" in data:
        TYPES = data["types"]
    else:
        raise ConfigError("types not found")

    LOADED = True

def cast(value, type_of_value):
    if type_of_value == "string":
        return str(value)
    elif type_of_value == "integer":
        return int(value)
    else:
        raise ConfigError("no type {}".format(type_of_value))

def get(key):
    global VALUES
    global ENVIRONMENTS
    global TYPES

    load()

    value = get_from_key(VALUES, key)

    if value is None:
        environment = os.environ.get(get_from_key(ENVIRONMENTS, key))

        if environment is None:
            raise ConfigError("{} is defined neither values nor environments".format(key))

        type_of_value = get_from_key(TYPES, key)
        value = cast(environment, type_of_value)

    return value
