'''
Created on May 13, 2021

@author: Sean Rahman
'''
# Python Imports
from flask import Flask, render_template, request

# Local Imports
from DatabaseHandling import Database

app = Flask(__name__)

# Create our configuration to be used for the 
app.config.from_object('ArmyTrackerConfiguration.Config')

# Random string used to create HTTP sessions using Flask
app.secret_key = app.config['SECRET_KEY']

# Create our Database class object that will be used for connection handling and querying
db = Database(app)

@app.route('/')
def index():
    title = 'Sawah'
    return render_template('index.html', title=title)

# Take the incoming post request and start working on handling the log-in portion
@app.route('/HandleLogin', methods = ['POST'])
def login():
    if request.method == 'POST':
        user = request.form['login']
        test = '<html><body>' + user + '</body></html>'
        return test

if __name__ == '__main__':
    db.connect()
    app.run()