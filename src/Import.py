import sys
import re
import logging
import argparse

import Config
import Property
import Database
import File

def insert(db_handler, page, logger):
    title = page.find("title").text

    for rm in Property.get("extra_titles"):
        if title[:len(rm) + 1] == rm + ":":
            logger.info("Remove: " + title)
            return

    redirect = page.find("redirect")

    if redirect is not None:
        target = redirect.attrib["title"]
        logger.info("Redirect: " + title + " -> " + target)
        db_handler.cursor.execute("insert into redirections (source, target) values (%s, %s)", (title, target))
        return

    revision = page.find("revision")
    text = revision.find("text").text

    if text is None:
        logger.info("Empty: " + title)
        return 

    db_handler.cursor.execute("insert into entries (title, content) values (%s, %s)", (title, text))
    logger.info("Entry: " + title)

def read(db_handler, path, logger):
    tree = File.load_xml(path)
    for page in tree.findall("page"):
        insert(db_handler, page, logger)

def logging_level(argument):
    argument = argument.lower()
    if argument == "critical":
        return logging.CRITICAL
    elif argument == "error":
        return logging.ERROR
    elif argument == "warning":
        return logging.WARNING
    elif argument == "info":
        return logging.INFO
    elif argument == "debug":
        return logging.DEBUG
    elif argument == "notset":
        return logging.NOTSET
    else:
        raise Exception("no such log level")

def main(args):
    logging.basicConfig(filename = "import.log", level = logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging_level(args.level))
    db_handler = Database.MySQLHandler(Config.get("database"))
    db_handler.connect()

    for path in args.paths:
        sys.stdout.write("\033[2K\033[G" + str(path))
        sys.stdout.flush()
        read(db_handler, path, logger)
        db_handler.connection.commit()

    sys.stdout.write("\033[2K\033[G")
    sys.stdout.write("complete {} files!\n".format(len(args.paths)))
    sys.stdout.flush()

    db_handler.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Master Data")
    parser.add_argument("--log", type=str, help="log file")
    parser.add_argument("--level", type=str, default="debug", help="logging level")
    parser.add_argument("paths", nargs="+", help="XML files")
    args = parser.parse_args(sys.argv[1:])
    main(args)
