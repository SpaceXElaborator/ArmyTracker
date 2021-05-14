import sqlite3
from contextlib import closing

class Database:
    def __init__(self, app):
        self.webapp = app
        self.initDatabase()
    def initDatabase(self):
        with open('scheme.sql', 'r') as f:
            db = self.connect()
            db.cursor().executescript(f.read())
        db.commit()
    def connect(self):
        print('Connecting to Database...')
        return sqlite3.connect('Tracker.db')
    #def query(self):        