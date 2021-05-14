'''
Created on May 13, 2021

@author: Sean Rahman
'''

from flask import Flask, render_template, request

app = Flask(__name__)

# Random string used to create HTTP sessions using Flask
app.secret_key = 'urasE3AhMEbFNZfXxRsW'

@app.route('/')
def index():
    return render_template('index.html')

# Take the incoming post request and start working on handling the log-in portion
@app.route('/HandleLogin', methods = ['POST'])
def login():
    if request.method == 'POST':
        user = request.form['login']
        test = '<html><body>' + user + '</body></html>'
        return test

if __name__ == '__main__':
    app.run()