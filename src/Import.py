import sys
import re
import Property
import Database
import File

def insert(db_handler, page):
    title = page.find("title").text
    for rm in Property.get("extra_titles"):
        if title[:len(rm) + 1] == rm + ":":
            sys.stderr.write("remove: " + title + "\n")
            return
    redirect = page.find("reirect")
    if redirect is not None:
        sys.stderr.write("redirect: " + title + " -> " + redirect.attrib["title"] + "\n")
        return
    revision = page.find("revision")
    text = revision.find("text").text
    if text is None:
        sys.stderr.write("empty text: " + title + "\n")
        return 
    db_handler.cursor.execute("insert into entries (title, content) values (%s, %s)", (title, text))

def read(db_handler, path):
    tree = File.load_xml(path)
    for page in tree.findall("page"):
        insert(db_handler, page)

def main(configure_path, paths):
    configure = File.load_yaml(configure_path)
    db_handler = Database.MySQLHandler(configure["database"])
    db_handler.connect()
    for path in paths:
        print(path)
        sys.stderr.write(str(path) + "\n")
        read(db_handler, path)
        db_handler.connection.commit()
    db_handler.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write("few arguments\n")
        exit(1)
    main(sys.argv[1], sys.argv[2:])
