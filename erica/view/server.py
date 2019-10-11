import flask
import json
import urllib

from ..core import *
from ..model import *
from ..master import *
from ..method import *


app = flask.Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/", methods = ["GET"])
def index_get():
    return flask.render_template("index.html")


@app.route("/debug", methods = ["GET"])
def debug_get():
    entry = Entry.sample()
    title = entry.title
    content = entry.content
    surface = MasterReader.get_sentences(content)
    segmented_content = MasterReader.split_text_to_paragraphs(content)
    segmented_surface = MasterReader.split_text_to_paragraphs(MasterReader.get_plain_text(content))

    return flask.render_template("debug.html",
        title = title,
        content = content,
        surface = surface,
        segmented_content = segmented_content,
        segmented_surface = segmented_surface
    )


@app.route("/api/ask", methods = ["POST"])
def api_ask_post():
    body = flask.request.json
    question = body["question"]

    answer = MethodClassic.ask(question)

    return flask.jsonify(answer = answer)


class Server:
    @classmethod
    def start(cls):
        global app
        app.run(host = Config.get("server.host"), port = Config.get("server.port"))
