import flask
import json
import urllib

from ..core import *
from ..model import *
from ..master import *
from ..method import *


app = flask.Flask(__name__, static_folder="static", template_folder="templates")


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


@app.route("/", methods = ["GET"])
def index_get():
    return flask.render_template("index.html")


@app.route("/", methods = ["POST"])
def index_post():
    body = flask.request.get_data()
    data = urllib.parse.parse_qs(str(body, "utf8"))
    question = data["query"][0]

    answer = MethodClassic.ask(question)

    return flask.render_template("index.html",
        question = question,
        answer = answer
    )


class Server:
    @classmethod
    def start(cls):
        global app
        app.run(host = Config.get("server.host"), port = Config.get("server.port"))
