'''
Created on May 13, 2021

@author: Sean Rahman
'''
# Required Imports
# passlib sqlite3 jinja2 flask

# Python Imports
from flask import Flask, render_template, request, redirect, session, url_for
import calendar

# Local Imports
from DatabaseHandling import Database
from ArmyCalendar import ArmyCalendar

app = Flask(__name__)

# Create our configuration to be used for the 
app.config.from_object('ArmyTrackerConfiguration.Config')

# Random string used to create HTTP sessions using Flask
app.secret_key = app.config['SECRET_KEY']

# Create our Database class object that will be used for connection handling and querying
db = Database(app)
cal = ArmyCalendar()

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
    return render_template('tracker.html', loggedInUser=session['username'], users=db.query('SELECT * FROM users'), error=request.args.get('error'))

@app.route('/calendar')
def eventCalendar():
    
    # If they don't have a proper session, redirect them back to the homepage
    if 'username' not in session:
        return redirect('/')
    
    return render_template('calendar.html', loggedInUser=session['username'], calendar=cal, days=cal.createCalendar())

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
    
    err = None
    
    # Connect to the Database and have it handle the interaction
    if not db.addTrackerUser(first, last, rank, squad):
        err = 'User Already Exists!'
    
    # Send them back to the tracker homepage once they have added the user to update the page
    return redirect(url_for('trackerDash', error=err))

@app.route('/RemUser', methods = ['POST'])
def remUser():
    
    #If they don't have a proper session, redirect them back to the homepage
    if 'username' not in session:
        return redirect('/')
    
    # Get the first and last name from the <option> tag from the html form
    name = request.form['UserName'].split(' ')
    first = name[0]
    last = name[1]
    
    err = None
    
    # Connect to the Database and have it handle the interaction
    if not db.remTrackerUser(first, last):
        err = 'User Does Not Exists!'
    
    # Send them back to the tracker homepage once they have added the user to update the page    
    return redirect(url_for('trackerDash', error=err))

@app.route('/HandleLogout')
def logout():

    #If they don't have a proper session, redirect them back to the homepage
    if 'username' not in session:
        return redirect('/')
        
    session.pop('username')
    return redirect('/')

@app.route('/ChangePassword', methods = ['POST'])
def changePass():
    #If they don't have a proper session, redirect them back to the homepage
    if 'username' not in session:
        return redirect('/')
    
    curr = request.form['Current']
    NewPass = request.form['NewPass']
    NewPassCheck = request.form['NewPassCheck']
    
    err = None
    
    if NewPass == NewPassCheck:
        if db.loginUser(session['username'], curr):
            db.changePass(session['username'], NewPass)
            # TODO: send toast saying password got updated
        else:
            err = 'Incorrect Password!'
    else:
        err = 'Passwords Do Not Match!'
        
    return redirect(url_for('trackerDash', error=err))

if __name__ == '__main__':
    app.run(host="0.0.0.0")