import falcon
from wsgiref import simple_server
import json

import Config
import Command

class EntryChecker(object):
    def on_get(self, req, resp):
        result = Command.get_entry(req.params)
        resp.body = json.dumps(result)

if __name__ == '__main__':
    Config.load()
    app = falcon.API()
    app.add_route("/", EntryChecker())
    httpd = simple_server.make_server("127.0.0.1", Config.get("api.port"), app)
    httpd.serve_forever()

