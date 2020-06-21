import sys
import re
import glob
import os
from sqlalchemy.sql import func

from ..model import *
from ..core import *
from .constant import MasterConstant
from .reader import MasterReader


class MasterBuilder:
    @classmethod
    def split(cls):
        re_start = re.compile(r"<page>")
        re_end = re.compile(r"</page>")
        chunk = 10000

        fname = Config.get("corpus.root") + "/" + Config.get("corpus.file.wikipedia")
        dirname = Config.get("workspace.root") + "/" + Config.get("workspace.resource")

        os.makedirs(dirname, exist_ok = True)

        flag = False
        body = []
        item_n = 0
        file_id = 1

        with open(fname, "r") as f:
            for line in f:
                if re_start.search(line):
                    flag = True

                if flag:
                    body.append(line)

                if re_end.search(line):
                    flag = False
                    item_n += 1

                    if item_n % chunk == 0:
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

    @classmethod
    def load_entries(cls):
        resource_path = Config.get("workspace.root") + "/" + Config.get("workspace.resource")
        paths = glob.glob(resource_path + "/*.xml")

        for path in paths:
            sys.stdout.write("\033[2K\033[G" + str(path))
            sys.stdout.flush()

            read(path)
            Session.commit()

        log = "completed %s files!" % len(paths)
        sys.stdout.write("\033[2K\033[G" + log + "\n")
        Logger.info(log)

    @classmethod
    def load_plain_texts(cls):
        chunk = 1000

        result = Session.query(func.max(Entry.id).label("max_id")).first()
        count = result.max_id

        if count is None:
            raise Exception("no entries")

        n_entries = 0

        for i in range(1, count + chunk + 1, chunk):
            for record in Session.query(Entry.id, Entry.content).filter(Entry.id >= i).filter(Entry.id < i + chunk):
                content = record.content
                entry_id = record.id
                sys.stdout.write("\033[2K\033[Gentry: " + str(entry_id))
                sys.stdout.flush()

                paragraphs = MasterReader.split_text_to_paragraphs(MasterReader.get_plain_text(content))
                text = "\n".join([sentence[1] for sentence in paragraphs])

                result = Session.query(PlainText.id).filter(PlainText.entry_id == entry_id).first()

                if result is not None:
                    result.text = text
                else:
                    Session.add(PlainText(entry_id = entry_id, text = text))

                n_entries += 1

            Session.commit()

        log = "completed %s entries!" % n_entries
        sys.stdout.write("\033[2K\033[G" + log + "\n")
        Logger.info(log)


def write(body, path):
    with open(path, "w") as f:
        f.write("<wikipedia>\n")

        for line in body:
            f.write(line)

        f.write("</wikipedia>\n")


def insert(page):
    title = page.find("title").text

    for rm in MasterConstant.extra_titles_ja:
        if title[:len(rm) + 1] == rm + ":":
            Logger.info("Remove: " + title)
            return

    redirect = page.find("redirect")

    if redirect is not None:
        target = redirect.attrib["title"]
        record = Redirection(source = title, target = target)
        Session.add(record)
        Logger.info("Redirect: " + title + " -> " + target)
        return

    revision = page.find("revision")
    text = revision.find("text").text

    if text is None:
        Logger.info("Empty: " + title)
        return 

    text = "".join(filter(lambda c: ord(c) < 0x10000, text))
    entry = Entry(title = title, content = text)
    Session.add(entry)
    Logger.info("Entry: " + title)


def read(path):
    tree = File.load_xml(path)
    for page in tree.findall("page"):
        insert(page)
