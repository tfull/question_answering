from janome.tokenizer import Tokenizer
from collections import defaultdict
from sqlalchemy import distinct
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
            top_entry_id = min(bottom_entry_id + chunk - 1, max_entry_id)

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
    def ask(cls, question):
        tokenizer = Tokenizer()
        question_words = tokenizer.tokenize(question, wakati = True)

        session = Database.Session()

        n_entries = session.query(distinct(ClassicWordCount.entry_id)).count()
        Logger.info("%s entries in database" % n_entries)

        n_question_words = len(question_words)
        Logger.info("%s words in sentence" % n_question_words)

        word_count_map = count_words(question_words)
        Logger.info("word_count_map: %s" % word_count_map)

        word_id_count_map = word_map_to_id_map(session, word_count_map)
        Logger.info("word_id_count_map: %s" % word_id_count_map)

        word_id_count_map = extract_important_words(session, word_id_count_map, 0.4, n_entries)
        Logger.info("word_id_count_map: %s" % word_id_count_map)

        vec_q = word_id_count_map

        entry_id_list = gather_related_entry_id_list(session, word_id_count_map)
        Logger.info("%s candidates" % len(entry_id_list))

        if len(entry_id_list) > n_entries * 0.8:
            return "[Ambiguous Question]"

        # for entry_id in entry_id_list:
        #     Logger.debug(entry_id_to_title(session, entry_id))

        session.close()

        # session.query(ClassicWordCount.entry_id, func.count("*")).group_by(ClassicWordCount.entry_id)

        candidates = []

        for entry_id in entry_id_list:
            Logger.debug("scoring entry_id = %s" % entry_id)

            session = Database.Session()
            records = session.query(ClassicWordCount).filter(ClassicWordCount.entry_id == entry_id).all()

            sentence_map = { record.classic_word_id: record.count for record in records }
            n_words_in_entry = sum(sentence_map.values())

            Logger.debug("word gathered: % words" % n_words_in_entry)

            vec_e = {}

            for word_id in sentence_map:
                count = sentence_map[word_id]
                vec_e[word_id] = count / n_words_in_entry * math.log(n_entries / document_frequency(session, word_id), 10)

            entry_score = cosine_similarity(vec_q, vec_e)

            Logger.debug("scored: %s" % entry_score)

            candidates = ranking(candidates, (entry_id, entry_score))

            session.close()

        if len(candidates) == 0:
            return None

        session = Database.Session()

        for candidate in candidates:
            Logger.info(entry_id_to_title(session, candidate[0]) + " " + str(candidate[1]))

        answer = entry_id_to_title(session, candidates[0][0])
        session.close()

        return answer


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


def entry_id_to_title(session, entry_id):
    result = session.query(Entry.title).\
        filter(Entry.id == entry_id).\
        one()

    return result.title


def ranking(sorted_candidates, item):
    return sorted(sorted_candidates + [item], key = lambda x: -x[1])[:20]


def extract_important_words(session, word_id_count_map, threshold, n_entries):
    dictionary = {}

    for word_id, count in word_id_count_map.items():
        if document_frequency(session, word_id) / n_entries < threshold:
            dictionary[word_id] = count

    return dictionary


def document_frequency(session, word_id):
    return session.query(ClassicWordCount).\
        filter(ClassicWordCount.classic_word_id == word_id).\
        count()

def count_words(words):
    dd = defaultdict(int)

    for word in words:
        dd[word] += 1

    return dd


def word_map_to_id_map(session, word_count_map):
    records = session.query(ClassicWord).\
        filter(ClassicWord.word.in_(word_count_map.keys())).\
        all()

    return { record.id: word_count_map[record.word] for record in records }


def gather_related_entry_id_list(session, word_id_count_map):
    records = session.query(ClassicWordCount.entry_id).\
        filter(ClassicWordCount.classic_word_id.in_(word_id_count_map.keys())).\
        group_by(ClassicWordCount.entry_id).\
        all()

    return [record.entry_id for record in records]
 