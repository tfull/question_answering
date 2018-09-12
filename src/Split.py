import sys
import re

RE_START = re.compile(r"<page>")
RE_END = re.compile(r"</page>")

def write(body, path):
    with open(path, "w") as f:
        f.write("<wikipedia>\n")
        for line in body:
            f.write(line)
        f.write("</wikipedia>\n")

def main(fname, dirname):
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
                if item_n >= 10000:
                    write(body, "{0}/{1:04d}.xml".format(dirname, file_id))
                    print("output: {0:04d}.xml".format(file_id))
                    body = []
                    item_n = 0
                    file_id += 1

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
