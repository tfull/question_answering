from janome.tokenizer import Tokenizer
from collections import defaultdict
from sqlalchemy import distinct, and_
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

        result = Session.query(func.max(PlainText.entry_id).label("max_entry_id")).one()

        if result is None:
            raise Exception("no entries in plain_texts")

        max_entry_id = result.max_entry_id

        if sup is not None:
            max_entry_id = min(max_entry_id, sup)

        min_entry_id = inf or 1

        for entry_id in range(min_entry_id, max_entry_id):
            delete_old_entry(entry_id)

            plain_text_record = Session.query(PlainText.text).filter(PlainText.entry_id == entry_id).first()

            if plain_text_record is None:
                continue

            dictionary = read_text(tokenizer, plain_text_record.text)

            word_count_records = []

            for word in dictionary:
                if len(word) > 255:
                    continue

                record_word = Session.query(ClassicWord).filter(ClassicWord.word == word).first()

                if record_word is None:
                    classic_word = ClassicWord(word = word, document_frequency = 1)
                    Session.add(classic_word)
                    Session.commit()

                    word_id = classic_word.id
                else:
                    record_word.document_frequency += 1
                    Session.commit()
                    word_id = record_word.id

                word_count_records.append(ClassicWordCount(entry_id = entry_id, classic_word_id = word_id, count = dictionary[word]))

            Session.bulk_save_objects(word_count_records)
            Session.commit()

    @classmethod
    def ask(cls, question):
        tokenizer = Tokenizer()
        question_words = tokenizer.tokenize(question, wakati = True)

        n_entries = Session.query(distinct(ClassicWordCount.entry_id)).count()
        Logger.info("%s entries in database" % n_entries)

        n_question_words = len(question_words)
        Logger.info("%s words in sentence" % n_question_words)

        word_count_map = count_words(question_words)
        Logger.info("word_count_map: %s" % word_count_map)

        word_id_count_map = create_important_word_id_map(word_count_map, int(n_entries * 0.4))
        Logger.info("word_id_count_map: %s" % word_id_count_map)

        vec_q = word_id_count_map

        entry_id_list = gather_related_entry_id_list(word_id_count_map)
        Logger.info("%s candidates" % len(entry_id_list))

        if len(entry_id_list) > n_entries * 0.8:
            return "[Ambiguous Question]"

        candidates = []

        for entry_id in entry_id_list:
            Logger.debug("scoring entry_id = %s" % entry_id)

            records = Session.query(ClassicWordCount, ClassicWord).\
                join(ClassicWord, and_(ClassicWordCount.classic_word_id == ClassicWord.id, ClassicWordCount.entry_id == entry_id)).\
                all()

            sentence_map = { w.id: wc.count for (wc, w) in records }
            frequency_map = { w.id: w.document_frequency for (_, w) in records }
            n_words_in_entry = sum(sentence_map.values())

            Logger.debug("words gathered: %s words" % n_words_in_entry)

            vec_e = {}

            for word_id in sentence_map:
                count = sentence_map[word_id]
                document_frequency = frequency_map[word_id]
                vec_e[word_id] = count / n_words_in_entry * math.log(n_entries / document_frequency, 10)

            entry_score = cosine_similarity(vec_q, vec_e)

            Logger.debug("scored: %s" % entry_score)

            candidates = ranking(candidates, (entry_id, entry_score))

        if len(candidates) == 0:
            return None

        for entry_id, score in candidates:
            Logger.info("%s: %s" % (Entry.id_to_title(entry_id), score))

        return Entry.id_to_title(candidates[0][0])


def delete_old_entry(entry_id):
    old_records = Session.query(ClassicWordCount).\
        filter(ClassicWordCount.entry_id == entry_id).\
        all()

    for classic_word in ClassicWord.find([x.classic_word_id for x in old_records]):
        classic_word.document_frequency -= 1

    Session.query(ClassicWordCount).\
        filter(ClassicWordCount.entry_id == entry_id).\
        delete()

    Session.commit()


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


def ranking(sorted_candidates, item):
    return sorted(sorted_candidates + [item], key = lambda x: -x[1])[:20]


def document_frequency(session, word_id):
    return session.query(ClassicWordCount).\
        filter(ClassicWordCount.classic_word_id == word_id).\
        count()


def count_words(words):
    dd = defaultdict(int)

    for word in words:
        dd[word] += 1

    return dict(dd)


def create_important_word_id_map(word_count_map, threshold):
    records = Session.query(ClassicWord).\
        filter(ClassicWord.word.in_(word_count_map.keys()), ClassicWord.document_frequency <= threshold).\
        all()

    return { record.id: word_count_map[record.word] for record in records }


def gather_related_entry_id_list(word_id_count_map):
    records = Session.query(ClassicWordCount.entry_id).\
        filter(ClassicWordCount.classic_word_id.in_(word_id_count_map.keys())).\
        group_by(ClassicWordCount.entry_id).\
        all()

    return [record.entry_id for record in records]
 