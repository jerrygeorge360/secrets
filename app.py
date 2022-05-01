from flask import Flask, render_template, session, redirect, request
from flask_sqlalchemy import SQLAlchemy

# from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anonymous.db' + '?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
db = SQLAlchemy(app)
from mydatabase import *
from AuthorizationSystem import *


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        msg = Authorize(username=username, password=password).login()
        return msg
    return render_template('secretmessage.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        msg = Authorize(username=username, password=password).signup()
        return msg
    return render_template('register.html')


@app.route('/myanonymous/<username>')
def secret_message():
    return render_template('comment.html')


@app.route('/message')
def message():
    #  if not session.get('username'):
    #     return redirect('/signup')

    return render_template('')


@app.route('/logout')
def logout():
    session['username'] = None
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
