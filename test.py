import sys
import json

import erica.base

def f0():
    from erica.brain.basic import BrainBasic

    brain = BrainBasic()
    print("accuracy: brain_basic")

    with open("test_resources/questions.json", "r") as f:
        json_object = json.load(f)

    count = 0

    for item in json_object:
        question = item["question"]
        answer = item["answer"]
        print("question: " + question)
        prediction = brain.ask(question)
        print("prediction: " + prediction)
        print("answer: " + answer)
        print()
        if prediction == answer:
            count += 1

    print("{0} / {1} correct".format(count, len(json_object)))

def f1():
    import erica.database as Database
    from erica.brain.basic import BrainBasic
    brain = BrainBasic()
    with open("test_resources/questions.json", "r") as f:
        json_object = json.load(f)

    for item in json_object:
        answer = item["answer"]
        Database.execute("select id from entries where title = %s", (answer,))
        record = Database.fetchone()
        if record:
            print("id:", record["id"], ", title:", answer)
            brain.load(record["id"] - 100, record["id"] + 100)

if __name__ == '__main__':
    erica.base.initialize()
    [f0, f1][int(sys.argv[1])]()
