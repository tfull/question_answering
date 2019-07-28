from janome.tokenizer import Tokenizer
from . import database as Database
from collections import defaultdict

def build():
    Database.execute("drop table if exists m1_word_counts")
    Database.execute("create table m1_word_counts ( \
        id int not null auto_increment primary key, \
        entry_id int not null, \
        word varchar(255) not null, \
        `count` int not null, \
        key idx_entry_id (entry_id), \
        key idx_word (word) \
        ) default charset utf8 collate utf8_bin")

def load():
    handler_id = Database.new()

    Database.execute("select max(entry_id) from plain_texts")
    record = Database.fetchone()
    count = record["max(entry_id)"]

    for i in range(count):
        entry_id = i + 1

        Database.execute("select * from plain_texts where entry_id = %s", (entry_id,))
        record = Database.fetchone()
        text = record["text"]

        dictionary = read_text(text)

        for word in dictionary:
            Database.execute("select count(1) from m1_word_counts where entry_id = %s and word = %s", (entry_id, word))
            record = Database.fetchone()
            if record["count(1)"] > 0:
                Database.execute("update m1_word_counts set count = %s where entry_id = %s and word = %s", (dictionary[word], entry_id, word))
            else:
                Database.execute("insert into m1_word_counts (entry_id, word, `count`) values (%s, %s, %s)", (entry_id, word, dictionary[word]))

        Database.commit()

def read_text(text):
    dictionary = defaultdict(int)

    tokenizer = Tokenizer()

    for sentence in text.split("\n"):
        for token in tokenizer.tokenize(sentence):
            word = token.base_form
            dictionary[word] += 1

    return dictionary
