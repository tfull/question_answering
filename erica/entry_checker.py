import falcon
from wsgiref import simple_server
import json

from . import base as Base
from . import config as Config
from . import command as Command
from . import reader as Reader

class EntryChecker(object):
    def on_get(self, req, resp):
#        result = Command.get_entry(req.params)
        entry = Command.sample_raw_entry()
        entry["surface"] = Reader.get_sentences(entry["content"])
        entry["segmented_content"] = Reader.split_text_to_paragraphs(entry["content"])
        entry["segmented_surface"] = Reader.split_text_to_paragraphs(Reader.get_plain_text(entry["content"]))
        resp.body = json.dumps(entry)

def serve():
    app = falcon.API()
    app.add_route("/", EntryChecker())
    httpd = simple_server.make_server("localhost", Config.get("api.port"), app)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
