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
            session['role'] = db.checkRole(user)
            return redirect('/tracker')
        
        print('Wrong password')
        return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('tracker', error='Page Not Found'))

@app.route('/tracker')
def tracker():
    # If they don't have a proper session, redirect them back to the homepage
    if 'username' not in session:
        return redirect('/')
    return render_template('tracker.html', loggedInUser=session['username'], role=session['role'], success=request.args.get('success'), error=request.args.get('error'))

@app.route('/soldier')
def soldier():

    # If they don't have a proper session, redirect them back to the homepage
    if 'username' not in session or 'role' not in session:
        return redirect('/')
    
    # If they don't have permission to be here, redirect them back to their previous page
    if session['role'] != 'Admin':
        return redirect(url_for('tracker', error='No Access'))
    
    # If they login, set their name in the top left corner of the page
    return render_template('soldiers.html', loggedInUser=session['username'], role=session['role'], users=db.query('SELECT * FROM users'), success=request.args.get('success'), error=request.args.get('error'))

@app.route('/calendar')
def calendar():
    
    # If they don't have a proper session, redirect them back to the homepage
    if 'username' not in session:
        return redirect('/')
    
    return render_template('calendar.html', loggedInUser=session['username'], role=session['role'], calendar=cal, days=cal.createCalendar(), success=request.args.get('success'), error=request.args.get('error'))

@app.route('/AddUser', methods = ['POST'])
def AddUser():
    
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
    return redirect(url_for('soldierView', error=err))

@app.route('/RemUser', methods = ['POST'])
def RemUser():
    
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
    return redirect(url_for('soldierView', error=err))

@app.route('/HandleLogout')
def HandleLogout():

    # If they don't have a proper session, redirect them back to the homepage
    if 'username' not in session:
        return redirect('/')
    
    # Remove 'username' and 'role' from the session to invalidate
    session.pop('username')
    session.pop('role')
    return redirect('/')

@app.route('/ChangePassword', methods = ['POST'])
def ChangePassword():
    #If they don't have a proper session, redirect them back to the homepage
    if 'username' not in session:
        return redirect('/')
    
    # Get all form data posted to the url
    curr = request.form['Current']
    NewPass = request.form['NewPass']
    NewPassCheck = request.form['NewPassCheck']
    
    err = None
    
    # Make sure the new passwords match
    if NewPass == NewPassCheck:
        if db.loginUser(session['username'], curr):
            db.changePass(session['username'], NewPass)
        else:
            err = 'Incorrect Password!'
    else:
        err = 'Passwords Do Not Match!'
    
    # If there is no error, password has been changed correctly. Post that back to previous page
    change = None
    if not err:
        change = 'Password Has Been Changed!'
    
    return redirect(url_for(request.referrer.split('/')[-1].split('?')[0], success=change, error=err))

if __name__ == '__main__':
    # Making sure to handle 404 errors
    app.register_error_handler(404, page_not_found)
    
    # Begin running the app
    app.run(host="0.0.0.0")