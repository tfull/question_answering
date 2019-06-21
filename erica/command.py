import sys
import random

from . import file as File
from . import database as Database
from . import reader as Reader
from . import config as Config

def get_raw_entry(title):
    sql = "select * from entries where title = %s limit 1"
    Database.execute(sql, (title,))
    record = Database.fetchone()

    return record

def sample_raw_entry():
    count_sql = "select count(1) from entries"
    Database.execute(count_sql)
    record = Database.fetchone()
    count = record["count(1)"]

    entry_id = random.randint(1, count)
    entry_sql = "select * from entries where id = %s"
    Database.execute(entry_sql, (entry_id,))
    record = Database.fetchone()

    return record

def get_entry(options):
    title = options.get("title")

    if title is not None:
        result = get_raw_entry(title)
    else:
        result = sample_raw_entry()

    result["sentences"] = Reader.get_sentences(result["content"])

    return result
