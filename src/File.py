import os
import yaml
import xml.etree.ElementTree

def load_yaml(path):
    with open(path, "r") as stream:
        return yaml.load(stream)

def load_xml(path):
    with open(path, "r") as f:
        parser = xml.etree.ElementTree.XMLParser()
        for line in f:
            parser.feed(line)
        return parser.close()

def load_config():
    path = os.path.dirname(os.path.abspath(__file__)) + "/../config.yml"
    assert os.path.isfile(path), "file {} does not exist".format(path)
    return load_yaml(path)
