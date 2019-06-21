import sys
import re
import argparse
import glob

from . import base as Base
from . import config as Config
from . import constant as Constant
from . import database as Database
from . import file as File
from . import logger as Logger

def insert(page):
    title = page.find("title").text

    for rm in Constant.extra_titles:
        if title[:len(rm) + 1] == rm + ":":
            Logger.info("Remove: " + title)
            return

    redirect = page.find("redirect")

    if redirect is not None:
        target = redirect.attrib["title"]
        Database.execute("insert into redirections (source, target) values (%s, %s)", (title, target))
        Logger.info("Redirect: " + title + " -> " + target)
        return

    revision = page.find("revision")
    text = revision.find("text").text

    if text is None:
        Logger.info("Empty: " + title)
        return 

    Database.execute("insert into entries (title, content) values (%s, %s)", (title, text))
    Logger.info("Entry: " + title)

def read(path):
    tree = File.load_xml(path)
    for page in tree.findall("page"):
        insert(page)

def main(args):
    Base.initialize()

    paths = args.paths

    if len(paths) == 0:
        resource_path = Config.get("workspace.root") + "/" + Config.get("workspace.resource")
        paths = glob.glob(resource_path + "/*.xml")

    for path in paths:
        sys.stdout.write("\033[2K\033[G" + str(path))
        sys.stdout.flush()
        read(path)
        Database.commit()

    sys.stdout.write("\033[2K\033[G" + "complete {} files!\n".format(len(paths)))

    Base.finalize()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Master Data Loader")
    parser.add_argument("paths", nargs = "*", help = "XML files")
    args = parser.parse_args(sys.argv[1:])
    main(args)
