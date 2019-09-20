from janome.tokenizer import Tokenizer
from collections import defaultdict
import math

from .. import database as Database
from .. import logger as Logger

class Migrator:
    pass

class Loader:
    pass

class Answerer:
    pass

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
    tokenizer = Tokenizer()

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

        dictionary = read_text(tokenizer, text)

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

def read_text(tokenizer, text):
    dictionary = defaultdict(int)

    for sentence in text.split("\n"):
        for token in tokenizer.tokenize(sentence):
            word = token.base_form
            dictionary[word] += 1

    return dictionary

def ask(query):
    tokenizer = Tokenizer()
    words = tokenizer.tokenize(query, wakati = True)

    n_entries = count_entries()

    Logger.info(str(n_entries) + " entries in database")

    n_words = len(words)

    Logger.info(str(n_words) + " words in sentence")

    word_count_map = count_words(words)

    Logger.info("word_count_map: " + str(word_count_map))

    word_id_count_map = word_to_id(word_count_map)

    Logger.info("word_id_count_map: " + str(word_id_count_map))

    word_id_count_map = extract_important_words(word_id_count_map, 0.4, n_entries)

    Logger.info("word_id_count_map: " + str(word_id_count_map))

    vec_q = word_id_count_map

    entry_id_list = gather_related_entry_id_list(word_id_count_map)
    Logger.info(str(len(entry_id_list)) + " candidates")

    candidates = []

    for entry_id in entry_id_list:
        Database.execute("select * from m1_word_counts where entry_id = %s", (entry_id,))
        records = Database.fetchall()

        sentence_map = { record["m1_word_id"]: record["count"] for record in records }
        n_words_in_entry = sum(sentence_map.values())

        vec_e = {}

        for word_id in sentence_map:
            count = sentence_map[word_id]
            vec_e[word_id] = count / n_words_in_entry * math.log(n_entries / document_frequency(word_id), 10)

        entry_score = cosine_similarity(vec_q, vec_e)

        candidates = ranking(candidates, (entry_id, entry_score))

    if len(candidates) == 0:
        return None

    for candidate in candidates:
        Logger.info(entry_id_to_title(candidate[0]) + " " + str(candidate[1]))

    return entry_id_to_title(candidates[0][0])

def cosine_similarity(vec_q, vec_e):
    total = 0

    for word in vec_q:
        if word in vec_e:
            total += vec_q[word] * vec_e[word]

    norm_q = math.sqrt(sum([x * x for x in vec_q.values()]))
    norm_e = math.sqrt(sum([x * x for x in vec_e.values()]))

    return total / (norm_q * norm_e)

def entry_id_to_title(entry_id):
    Database.execute("select title from entries where id = %s", (entry_id,))
    record = Database.fetchone()

    return record["title"]

def ranking(sorted_candidates, item):
    return sorted(sorted_candidates + [item], key = lambda x: -x[1])[:20]

def extract_important_words(word_id_count_map, threshold, n_entries):
    dictionary = {}

    for word_id, count in word_id_count_map.items():
        if document_frequency(word_id) / n_entries < threshold:
            dictionary[word_id] = count

    return dictionary

def document_frequency(word_id):
    Database.execute("select count(1) from m1_word_counts where m1_word_id = %s", (word_id,))
    record = Database.fetchone()
    return record["count(1)"]

def query_list_arguments(n):
    return ", ".join(["%s" for i in range(n)])

def count_entries():
    Database.execute("select count(distinct entry_id) from m1_word_counts")
    record = Database.fetchone()

    return record["count(distinct entry_id)"]

def count_words(words):
    dd = defaultdict(int)

    for word in words:
        dd[word] += 1

    return dd

def word_to_id(word_count_map):
    Database.execute("select * from m1_words where word in ({})".format(query_list_arguments(len(word_count_map))), tuple(word_count_map.keys()))
    records = Database.fetchall()

    dd = {}

    for record in records:
        dd[record["id"]] = word_count_map[record["word"]]

    return dd

def gather_related_entry_id_list(word_id_count_map):
    Database.execute("select entry_id from m1_word_counts where m1_word_id in ({}) group by entry_id".format(query_list_arguments(len(word_id_count_map))), tuple(word_id_count_map.keys()))

    return [record["entry_id"] for record in Database.fetchall()]
