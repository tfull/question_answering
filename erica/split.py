import sys
import re
import os

from . import config as Config

RE_START = re.compile(r"<page>")
RE_END = re.compile(r"</page>")

def write(body, path):
    with open(path, "w") as f:
        f.write("<wikipedia>\n")

        for line in body:
            f.write(line)

        f.write("</wikipedia>\n")

def main():
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

if __name__ == '__main__':
    main()
