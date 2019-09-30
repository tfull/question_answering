import time

from ..core import *
from ..model import *
from ..method import *
from .constant import TestConstant


class TestClassic:
    @classmethod
    def load(cls):
        session = Database.Session()

        title_list = [item["answer"] for item in TestConstant.sample_qa_list]

        records = session.query(Entry.id, Entry.title).filter(Entry.title.in_(title_list)).all()

        for record in records:
            entry_id = record.id
            inf_id = max(entry_id - 100, 1)
            sup_id = entry_id + 100

            log = "[Classic: load] %s: %s ~ %s ~ %s" % (record.title, inf_id, entry_id, sup_id)
            print(log)
            Logger.info(log)

            MethodClassic.load(inf_id, sup_id)

        session.close()

    @classmethod
    def ask_one(cls):
        item = TestConstant.sample_qa_list[0]
        question = item["question"]
        answer = item["answer"]

        time_start = time.time()
        response = MethodClassic.ask(question)
        time_end = time.time()

        log = "question: %s\nresponse: %s\nanswer: %s" % (question, response, answer)
        print(log)
        Logger.info(log)

        log = "time: {0:.3f}".format(time_end - time_start)
        print(log)
        Logger.info(log)

    @classmethod
    def check_sample_questions(cls):
        correct_count = 0

        for item in TestConstant.sample_qa_list:
            question = item["question"]
            answer = item["answer"]

            response = MethodClassic.ask(question)

            log = "==========\nquestion: %s\nresponse: %s\nanswer: %s" % (question, response, answer)
            print(log)
            Logger.info(log)

            if response == answer:
                correct_count += 1

        log = "accuracy: %s / %s" % (correct_count, len(TestConstant.sample_qa_list))
        print(log)
        Logger.info(log)
