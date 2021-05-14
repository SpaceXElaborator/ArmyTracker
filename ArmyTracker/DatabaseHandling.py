import sqlite3

class Database:
    def __init__(self, app):
        self.webapp = app
    def connect(self):
        print('Connecting to Database...')
        return sqlite3.connect('Tracker.db')
    #def query(self):
        