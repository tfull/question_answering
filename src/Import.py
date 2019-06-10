import sys
import re
import argparse
import glob

import Config
import Property
import Database
import File
import Logger

def insert(db_handler, page):
    title = page.find("title").text

    for rm in Property.get("extra_titles"):
        if title[:len(rm) + 1] == rm + ":":
            Logger.info("Remove: " + title)
            return

    redirect = page.find("redirect")

    if redirect is not None:
        target = redirect.attrib["title"]
        db_handler.cursor.execute("insert into redirections (source, target) values (%s, %s)", (title, target))
        Logger.info("Redirect: " + title + " -> " + target)
        return

    revision = page.find("revision")
    text = revision.find("text").text

    if text is None:
        Logger.info("Empty: " + title)
        return 

    db_handler.cursor.execute("insert into entries (title, content) values (%s, %s)", (title, text))
    Logger.info("Entry: " + title)

def read(db_handler, path):
    tree = File.load_xml(path)
    for page in tree.findall("page"):
        insert(db_handler, page)

def main(args):
    db_handler = Database.MySQLHandler(Config.get("database"))
    db_handler.connect()

    paths = args.paths

    if len(paths) == 0:
        resource_path = Config.get("workspace.root") + "/" + Config.get("workspace.resource")
        paths = glob.glob(resource_path + "/*.xml")

    for path in paths:
        sys.stdout.write("\033[2K\033[G" + str(path))
        sys.stdout.flush()
        read(db_handler, path)
        db_handler.connection.commit()

    sys.stdout.write("\033[2K\033[G")
    sys.stdout.write("complete {} files!\n".format(len(paths)))

    db_handler.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Master Data Loader")
    parser.add_argument("paths", nargs = "*", help = "XML files")
    args = parser.parse_args(sys.argv[1:])
    main(args)
