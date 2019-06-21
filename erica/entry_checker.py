import falcon
from wsgiref import simple_server
import json

from . import base as Base
from . import config as Config
from . import command as Command

class EntryChecker(object):
    def on_get(self, req, resp):
        result = Command.get_entry(req.params)
        resp.body = json.dumps(result)

def serve():
    Base.initialize()
    app = falcon.API()
    app.add_route("/", EntryChecker())
    httpd = simple_server.make_server("0.0.0.0", Config.get("api.port"), app)
    httpd.serve_forever()
    Base.finalize()

if __name__ == '__main__':
    serve()
