import MySQLdb

class MySQLHandler:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    def connect(self):
        config = self.config
        self.connection = MySQLdb.connect(user=config["user"], passwd=config["password"], host=config["host"], db=config["dbname"], charset="utf8")
        self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

    def close(self):
        self.connection.close()
        self.cursor.close()
