import yaml
import xml.etree.ElementTree

def load_yaml(path):
    with open(path, "r") as stream:
        return yaml.load(stream, Loader=yaml.FullLoader)

def load_xml(path):
    with open(path, "r") as f:
        parser = xml.etree.ElementTree.XMLParser()
        for line in f:
            parser.feed(line)
        return parser.close()
