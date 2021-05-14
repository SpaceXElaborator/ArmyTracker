import sqlite3
from contextlib import closing

class Database:
    def __init__(self, app):
        self.webapp = app
        self.initDatabase()
    
    # Connect to our database file and run the sql script for initializing all tables and login users
    def initDatabase(self):
        with open('scheme.sql', 'r') as f:
            db = self.connect()
            db.cursor().executescript(f.read())
        db.commit()
    def connect(self):
        print('Connecting to Database...')
        return sqlite3.connect('Tracker.db')
    def query(self, sqlargument, args=(), one=False):
        db = self.connect()
        cursor = db.execute(sqlargument, args)
        result = cursor.fetchall()
        cursor.close()
        return(result[0] if result else None) if one else result