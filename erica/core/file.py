import yaml
import xml.etree.ElementTree

class File:
    @classmethod
    def load_yaml(cls, path):
        with open(path, "r") as stream:
            return yaml.load(stream, Loader=yaml.FullLoader)

    @classmethod
    def load_xml(cls, path):
        with open(path, "r") as f:
            parser = xml.etree.ElementTree.XMLParser()

            for line in f:
                parser.feed(line)

            return parser.close()
