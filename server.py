import flask
import json
import urllib

import erica.base as Base
import erica.config as Config
import erica.brain as Brain
import erica.command as Command
import erica.reader as Reader

app = flask.Flask(__name__)

@app.route("/debug", methods = ["GET"])
def debug_get():
    entry = Command.sample_raw_entry()
    title = entry["title"]
    content = entry["content"]
    surface = Reader.get_sentences(content)
    segmented_content = Reader.split_text_to_paragraphs(content)
    segmented_surface = Reader.split_text_to_paragraphs(Reader.get_plain_text(content))

    return flask.render_template("debug.html", title = title, content = content, surface = surface, segmented_content = segmented_content, segmented_surface = segmented_surface)

@app.route("/", methods = ["GET"])
def index_get():
    return flask.render_template("index.html")

@app.route("/", methods = ["POST"])
def index_post():
    body = flask.request.get_data()
    data = urllib.parse.parse_qs(str(body, "UTF-8"))
    question = data["query"][0]

    answer = Brain.ask(question)

    return flask.render_template("index.html", question = question, answer = answer)

def serve():
    global app
    app.run(host = "0.0.0.0", port = Config.get("api.port"))

if __name__ == '__main__':
    Base.initialize()
    serve()
