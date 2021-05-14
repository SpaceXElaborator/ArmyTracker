'''
Created on May 13, 2021

@author: Sean Rahman
'''

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title = "Test Template File"
    return render_template('index.html', title=title)

if __name__ == '__main__':
    app.run()