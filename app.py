import os

from flask import Flask, render_template, session, redirect, request, make_response, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
import json
from flask_session import Session

uri=os.environ['DATABASE_URL']
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.environ['FLASK_SECRET_KEY']
Session(app)
db = SQLAlchemy(app)
from mydatabase import *
from AuthorizationSystem import *


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        session["name"] = request.form.get("name")
        msg = Authorize(username=username, password=password).login()
        return msg
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        msg = Authorize(username=username, password=password).signup()
        return msg

    return render_template('register.html')


@app.route('/incognito/<username>', methods=['GET', 'POST'])
def secret_message(username):
    username.replace('%20', ' ')
    print(username)
    if request.method == 'POST':
        message = request.form['message']
        print(message)
        user = db.session.query(User).filter_by(user_name_hash=username).first()
        cursor = SecretMessage(message=message, receiver=user)
        db.session.add(cursor)
        db.session.commit()
        db.session.close()
        flash(f'Message was successfully sent.Register to generate your own unique link.', 'success')
        return make_response(redirect('/signup'))

    elif request.method == 'GET':
        if User.query.filter_by(user_name_hash=username).first():
            print(username)
            return render_template('secretmessage.html')

        else:

            return redirect('/404')
    else:
        error = 'Not successful'

        return render_template('secretmessage.html', error=error)


@app.route('/message', methods=['POST', 'GET'])
def message():
    user_name = session.get('username')
    a = User.query.filter_by(user_name=user_name).first()

    return render_template('messages.html', a=a)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorpage.html'), 404


@app.route('/logout')
def logout():
    session['username'] = None
    return redirect('/')




if __name__ == '__main__':
    app.run()
