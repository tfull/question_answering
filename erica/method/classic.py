from janome.tokenizer import Tokenizer
from collections import defaultdict
from sqlalchemy.sql import func
import math

from ..core import *
from ..model import *
from ..model.classic import *

class MethodClassic():
    @classmethod
    def load(cls, inf = None, sup = None):
        chunk = 100

        tokenizer = Tokenizer()

        session = Database.Session()
        result = session.query(func.max(PlainText.entry_id).label("max_entry_id")).one()
        session.close()

        if result is None:
            raise Exception("no entries in plain_texts")

        max_entry_id = result.max_entry_id

        if sup is not None:
            max_entry_id = min(max_entry_id, sup)

        min_entry_id = inf or 1

        for bottom_entry_id in range(min_entry_id, max_entry_id + 1, chunk):
            session = Database.Session()
            top_entry_id = bottom_entry_id + chunk - 1

            old_records = session.query(ClassicWordCount).filter(ClassicWordCount.entry_id.between(bottom_entry_id, top_entry_id)).all()

            if len(old_records) > 0:
                session.delete(old_records)

            for entry_id in range(bottom_entry_id, top_entry_id + 1):
                record = session.query(PlainText.text).filter(PlainText.entry_id == entry_id).first()

                if record is None:
                    continue

                text = record.text

                dictionary = read_text(tokenizer, text)

                word_count_records = []

                for word in dictionary:
                    if len(word) > 255:
                        continue

                    record_word = session.query(ClassicWord.id).filter(ClassicWord.word == word).first()

                    if record_word is None:
                        session_insert = Database.Session()

                        classic_word = ClassicWord(word = word)

                        session_insert.add(classic_word)
                        session_insert.commit()

                        word_id = classic_word.id
                    else:
                        word_id = record_word.id

                    word_count_records.append(ClassicWordCount(entry_id = entry_id, classic_word_id = word_id, count = dictionary[word]))

                session.bulk_save_objects(word_count_records)

            session.commit()
            session.close()

    @classmethod
    def ask(cls, query):
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
            Database.execute("select * from {}_word_counts where entry_id = %s".format(BrainBasic.code_name), (entry_id,))
            records = Database.fetchall()

            sentence_map = { record["{}_word_id".format(BrainBasic.code_name)]: record["count"] for record in records }
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


def read_text(tokenizer, text):
    dictionary = defaultdict(int)

    for sentence in text.split("\n"):
        for token in tokenizer.tokenize(sentence):
            word = token.base_form
            dictionary[word] += 1

    return dictionary

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
    Database.execute("select count(1) from {0}_word_counts where {0}_word_id = %s".format(BrainBasic.code_name), (word_id,))
    record = Database.fetchone()
    return record["count(1)"]

def query_list_arguments(n):
    return ", ".join(["%s" for i in range(n)])

def count_entries():
    Database.execute("select count(distinct entry_id) from {}_word_counts".format(BrainBasic.code_name))
    record = Database.fetchone()

    return record["count(distinct entry_id)"]

def count_words(words):
    dd = defaultdict(int)

    for word in words:
        dd[word] += 1

    return dd

def word_to_id(word_count_map):
    Database.execute("select * from {0}_words where word in ({1})".format(BrainBasic.code_name, query_list_arguments(len(word_count_map))), tuple(word_count_map.keys()))
    records = Database.fetchall()

    dd = {}

    for record in records:
        dd[record["id"]] = word_count_map[record["word"]]

    return dd

def gather_related_entry_id_list(word_id_count_map):
    query = "select entry_id from {0}_word_counts where {0}_word_id in ({1}) group by entry_id".format(BrainBasic.code_name, query_list_arguments(len(word_id_count_map)))
    Database.execute(query, tuple(word_id_count_map.keys()))

    return [record["entry_id"] for record in Database.fetchall()]
