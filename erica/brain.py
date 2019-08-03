from janome.tokenizer import Tokenizer
from . import database as Database
from collections import defaultdict

def build():
    Database.execute("drop table if exists m1_words")
    Database.execute("create table m1_words ( \
        id bigint not null auto_increment primary key, \
        word varchar(255) not null, \
        key idx_word (word) \
        ) default charset utf8 collate utf8_bin")

    Database.execute("drop table if exists m1_word_counts")
    Database.execute("create table m1_word_counts ( \
        id bigint not null auto_increment primary key, \
        entry_id int not null, \
        m1_word_id bigint not null, \
        `count` int not null, \
        key idx_entry_id (entry_id), \
        key idx_m1_word_id (m1_word_id) \
        ) default charset utf8 collate utf8_bin")

def load(inf = None, sup = None):
    handler_id = Database.new()

    Database.execute("select max(entry_id) from plain_texts")
    record = Database.fetchone()
    max_entry_id = record["max(entry_id)"]

    if sup is not None:
        max_entry_id = min(max_entry_id, sup)

    min_entry_id = inf or 1

    for entry_id in range(min_entry_id, max_entry_id + 1):
        Database.execute("delete from m1_word_counts where entry_id = %s", (entry_id,))

        Database.execute("select * from plain_texts where entry_id = %s", (entry_id,))
        record = Database.fetchone()
        text = record["text"]

        dictionary = read_text(text)

        for word in dictionary:
            if len(word) > 255:
                continue

            Database.execute("select id from m1_words where word = %s", (word,))
            record = Database.fetchone()

            if record is None:
                Database.execute("insert into m1_words (word) values (%s)", (word,))
                Database.execute("select id from m1_words where word = %s", (word,))
                record = Database.fetchone()

            word_id = record["id"]

            Database.execute("insert into m1_word_counts (entry_id, m1_word_id, `count`) values (%s, %s, %s)", (entry_id, word_id, dictionary[word]))

        Database.commit()

def read_text(text):
    dictionary = defaultdict(int)

    tokenizer = Tokenizer()

    for sentence in text.split("\n"):
        for token in tokenizer.tokenize(sentence):
            word = token.base_form
            dictionary[word] += 1

    return dictionary
