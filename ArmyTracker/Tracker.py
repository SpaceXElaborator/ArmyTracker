'''
Created on May 13, 2021

@author: Sean Rahman
'''
# Required Imports
# passlib sqlite3 jinja2 flask

# Python Imports
from flask import Flask, render_template, request, redirect, session

# Local Imports
from DatabaseHandling import Database
from PythonExtension import PythonExtension

app = Flask(__name__)

# Create our configuration to be used for the 
app.config.from_object('ArmyTrackerConfiguration.Config')

# Random string used to create HTTP sessions using Flask
app.secret_key = app.config['SECRET_KEY']
app.jinja_env.add_extension(PythonExtension)

# Create our Database class object that will be used for connection handling and querying
db = Database(app)

@app.route('/')
def index():
    return render_template('index.html')

# Take the incoming post request and start working on handling the log-in portion
@app.route('/HandleLogin', methods = ['POST'])
def login():

    # Only want to check for posting
    if request.method == 'POST':
    
        # Get the form data and store them as local variables
        user = request.form['login']
        passW = request.form['password']
        
        # If the user successfully logs in, set their session and redirect them to the tracker
        if db.loginUser(user, passW):
            session['username'] = user
            return redirect('/tracker')
        
        print('Wrong password')
        return redirect('/')
        
@app.route('/tracker')
def trackerDash():

    # If they don't have a proper session, redirect them back to the homepage
    if 'username' not in session:
        return redirect('/')
    
    # If they login, set their name in the top left corner of the page
    return render_template('tracker.html', loggedInUser=session['username'], users=db.query('SELECT * FROM users'))

@app.route('/AddUser', methods = ['POST'])
def addUser():
    
    #If they don't have a proper session, redirect them back to the homepage
    if 'username' not in session:
        return redirect('/')
    
    # Get the required fields to add a user from the <form> tag in html document
    first = request.form['First']
    last = request.form['Last']
    rank = request.form['Rank']
    squad = request.form['Squad']
    
    # Connect to the Database and have it handle the interaction
    if not db.addTrackerUser(first, last, rank, squad):
        session['FailedInteraction'] = 'User Creation Failed'
        session['Warning'] = 'User Already Exists!'
    
    # Send them back to the tracker homepage once they have added the user to update the page
    return redirect('/tracker')

@app.route('/RemUser', methods = ['POST'])
def remUser():
    
    #If they don't have a proper session, redirect them back to the homepage
    if 'username' not in session:
        return redirect('/')
    
    # Get the first and last name from the <option> tag from the html form
    name = request.form['UserName'].split(' ')
    first = name[0]
    last = name[1]
    
    # Connect to the Database and have it handle the interaction
    if not db.remTrackerUser(first, last):
        session['FailedInteraction'] = 'User Deletion Failed'
        session['Warning'] = 'User Does Not Exists!'
    
    # Send them back to the tracker homepage once they have added the user to update the page    
    return redirect('/tracker')

if __name__ == '__main__':
    app.run()