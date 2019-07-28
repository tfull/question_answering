import sys
import re
import argparse
import glob
import os

from . import base as Base
from . import config as Config
from . import constant as Constant
from . import database as Database
from . import file as File
from . import logger as Logger
from . import reader as Reader

RE_START = re.compile(r"<page>")
RE_END = re.compile(r"</page>")

def reset_database():
    db = Config.get("database.dbname")

    Database.execute("drop table if exists entries")
    Database.execute("create table entries ( \
        id int not null auto_increment primary key, \
        title varchar(255) not null, \
        content mediumtext not null, \
        key idx_title (title) \
        ) default charset utf8 collate utf8_bin")

    Database.execute("drop table if exists redirections")
    Database.execute("create table redirections ( \
        id int not null auto_increment primary key, \
        source varchar(255) not null, \
        target varchar(255) not null, \
        key idx_source (source), \
        key idx_target (target) \
        ) default charset utf8 collate utf8_bin")

    Database.execute("drop table if exists plain_texts")
    Database.execute("create table plain_texts ( \
        id int not null auto_increment primary key, \
        entry_id int not null, \
        `text` mediumtext not null, \
        key idx_entry_id (entry_id) \
        ) default charset utf8 collate utf8_bin")

def write(body, path):
    with open(path, "w") as f:
        f.write("<wikipedia>\n")

        for line in body:
            f.write(line)

        f.write("</wikipedia>\n")

def split():
    fname = Config.get("workspace.root") + "/" + Config.get("workspace.wikipedia")
    dirname = Config.get("workspace.root") + "/" + Config.get("workspace.resource")

    flag = False
    body = []
    item_n = 0
    file_id = 1

    with open(fname, "r") as f:
        for line in f:
            if RE_START.search(line):
                flag = True

            if flag:
                body.append(line)

            if RE_END.search(line):
                flag = False
                item_n += 1

                if item_n % 10000 == 0:
                    write(body, "{0}/{1:04d}.xml".format(dirname, file_id))
                    sys.stdout.write("\033[2K\033[G{0:04d}.xml".format(file_id))
                    sys.stdout.flush()
                    body = []
                    file_id += 1

    if len(body) > 0:
        write(body, "{0}/{1:04d}.xml".format(dirname, file_id))
        sys.stdout.write("\033[2K\033[G{0:04d}.xml".format(file_id))
        sys.stdout.flush()
    else:
        file_id -= 1

    sys.stdout.write("\033[2K\033[GCompleted: {0} items in {1} files\n".format(item_n, file_id))

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

    text = "".join(filter(lambda c: ord(c) < 0x10000, text))
    Database.execute("insert into entries (title, content) values (%s, %s)", (title, text))
    Logger.info("Entry: " + title)

def read(path):
    tree = File.load_xml(path)
    for page in tree.findall("page"):
        insert(page)

def load_to_database():
    resource_path = Config.get("workspace.root") + "/" + Config.get("workspace.resource")
    paths = glob.glob(resource_path + "/*.xml")

    for path in paths:
        sys.stdout.write("\033[2K\033[G" + str(path))
        sys.stdout.flush()
        read(path)
        Database.commit()

    sys.stdout.write("\033[2K\033[G" + "complete {} files!\n".format(len(paths)))

def insert_plain_text():
    Database.execute("select max(id) from entries")
    record = Database.fetchone()
    count = record["max(id)"]

    for i in range(count):
        entry_id = i + 1
        Database.execute("select content from entries where id = %s", (entry_id,))
        record = Database.fetchone()

        content = record["content"]

        paragraphs = Reader.split_text_to_paragraphs(Reader.get_plain_text(content))
        text = "\n".join([sentence[1] for sentence in paragraphs])

        Database.execute("select 1 from plain_texts where entry_id = %s", (entry_id,))

        if Database.fetchone():
            Database.execute("update plain_texts set `text` = %s where entry_id = %s", (text, entry_id))
        else:
            Database.execute("insert into plain_texts (entry_id, `text`) values (%s, %s)", (entry_id, text))

        Database.commit()
