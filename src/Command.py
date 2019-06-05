import sys
import random
import File
import Database
import Reader
import Config

def get_raw_entry(db_handler, title):
    sql = "select * from entries where title = %s limit 1"
    db_handler.cursor.execute(sql, (title,))
    record = db_handler.cursor.fetchone()
    return record

def sample_raw_entry(db_handler):
    count_sql = "select count(1) from entries"
    db_handler.cursor.execute(count_sql)
    record = db_handler.cursor.fetchone()
    count = record["count(1)"]
    entry_id = random.randint(1, count)
    entry_sql = "select * from entries where id = %s"
    db_handler.cursor.execute(entry_sql, (entry_id,))
    record = db_handler.cursor.fetchone()
    return record

def get_entry(options):
    if "title" in options:
        title = options["title"]
    else:
        title = None

    db_handler = Database.MySQLHandler(Config.get("database"))
    db_handler.connect()
    if title is not None:
        result = get_raw_entry(db_handler, title)
    else:
        result = sample_raw_entry(db_handler)
    db_handler.close()
    result["sentences"] = Reader.get_sentences(result["content"])
    return result
