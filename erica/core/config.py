import os

from .file import File

class ConfigError(Exception):
    pass

class Config:
    PATH = os.path.dirname(os.path.abspath(__file__)) + "/../../config.yml"
    VALUES = None
    ENVIRONMENTS = None
    TYPES = None
    LOADED = False

    @classmethod
    def load(cls):
        if cls.LOADED:
            return

        if not os.path.isfile(cls.PATH):
            raise ConfigError("file {} does not exist".format(cls.PATH))

        data = File.load_yaml(cls.PATH)

        if "values" in data:
            cls.VALUES = data["values"]
        else:
            raise ConfigError("values not found")

        if "environments" in data:
            cls.ENVIRONMENTS = data["environments"]
        else:
            raise ConfigError("environments not found")

        if "types" in data:
            cls.TYPES = data["types"]
        else:
            raise ConfigError("types not found")

        cls.LOADED = True

    @classmethod
    def get(cls, key):
        cls.load()

        value = get_from_key(cls.VALUES, key)

        if value is None:
            environment = os.environ.get(get_from_key(cls.ENVIRONMENTS, key))

            if environment is None:
                raise ConfigError("{} is defined neither values nor environments".format(key))

            type_of_value = get_from_key(cls.TYPES, key)
            value = cast(environment, type_of_value)

        return value


def get_from_key(data, key, must = False):
    for k in key.split("."):
        if k not in data:
            raise ConfigError("field {} does not exist".format(key))

        data = data[k]

    return data


def cast(value, type_of_value):
    if type_of_value == "string":
        return str(value)
    elif type_of_value == "integer":
        return int(value)
    else:
        raise ConfigError("no type {}".format(type_of_value))