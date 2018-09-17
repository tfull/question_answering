import sys
import File
import Database
import Reader
import Config

def sample_page(db_handler):
    sql = "select * from entries limit 1"
    db_handler.cursor.execute(sql)
    record = db_handler.cursor.fetchone()
    return record

def main():
    Config.load()

    db_handler = Database.MySQLHandler(Config.get("database"))
    db_handler.connect()
    page = sample_page(db_handler)
    print(Reader.get_plain_text(page["content"]))

    db_handler.close()


if __name__ == '__main__':
    main()
