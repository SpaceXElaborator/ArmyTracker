import sqlite3
import os
from passlib.hash import pbkdf2_sha256

class Database:
    def __init__(self, app):
        self.webapp = app
        self.initDatabase()
    
    # Connect to our database file and run the sql script for initializing all tables and login users
    def initDatabase(self):
    
        # Check if the database file from the from configuration exists
        if not os.path.exists(self.webapp.config['DATABASE']):
        
            #Create an empty database file if none exists
            with open(self.webapp.config['DATABASE'], 'w') as f:
                pass
      
        with open('scheme.sql', 'r') as f:
            db = self.connect()
            db.cursor().executescript(f.read())
        db.commit()
        db.close()
        adminExists = self.query('SELECT * FROM login WHERE username = ?', ['admin'], one = True)
        if adminExists == None:
            print('Adding Admin User...')
            self.createUser('admin', 'password1')
        
    # Create connection to SQLite Database file from configuration
    def connect(self):
        return sqlite3.connect(self.webapp.config['DATABASE'])
        
    # sqlargument will be the sql script to be ran
    # args will change inplace of '?' when getting specific columns
    # one will tell the code whether it needs to find only one thing (first find) or all
    def query(self, sqlargument, args=(), one = False):
        db = self.connect()
        cursor = db.execute(sqlargument, args)
        result = cursor.fetchall()
        cursor.close()
        return(result[0] if result else None) if one else result
    
    # Check for the username in the login database to make sure two usernames do not exists that are the same
    def checkUser(self, username):
        userFound = self.query('SELECT * FROM login WHERE username = ?', [username.casefold()], one = True)
        return  (True if userFound else False)
    
    def checkTrackedUser(self, first, last):
        userFound = self.query('SELECT * FROM users WHERE first = ? AND last = ?', [first.lower().capitalize(), last.lower().capitalize()], one = True)
        return (True if userFound else False)
    
    # Create a given user for the login portion using pbkdf2_sha256 recommended database password storing
    def createUser(self, username, password):
        if not self.checkUser(username):
            hashPass = pbkdf2_sha256.hash(password)
            db = self.connect()
            # Uses None to Auto-Increment value into Database
            db.execute('INSERT INTO login VALUES(?, ?, ?)', [None, username.casefold(), hashPass])
            db.commit()
            db.close()
            return True
        return False
        
    def loginUser(self, username, password):
        if self.checkUser(username):
            user = self.query('SELECT * FROM login WHERE username = ?', [username.casefold()], one = True)
            return pbkdf2_sha256.verify(password, user[2])
        return False
    
    def addTrackerUser(self, first, last, rank, squad):
        if not self.checkTrackedUser(first, last):
            db = self.connect()
            db.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?)', [None, first.capitalize(), last.capitalize(), rank.upper(), int(squad)])
            db.commit()
            db.close()
            return True
        return False
    
    def changePass(self, username, newpass):
        hashPass = pbkdf2_sha256.hash(newpass)
        db = self.connect()
        db.execute('UPDATE login SET password = ? WHERE username = ?', [hashPass, username])
        db.commit()
        db.close()
    def remTrackerUser(self, first, last):
        if self.checkTrackedUser(first, last):
            db = self.connect()
            db.execute('DELETE FROM users WHERE first = ? AND last = ?', [first.lower().capitalize(), last.lower().capitalize()])
            db.commit()
            db.close()
            return True
        return False