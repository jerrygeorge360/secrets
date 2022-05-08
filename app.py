from flask import Flask, render_template, session, redirect, request
from flask_sqlalchemy import SQLAlchemy

from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anonymous.db' + '?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
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
        myobject = db.session.query(mydatabase.User).filter_by(user_name=username).first()
        return render_template('register.html', url_name=myobject.user_name_hash)
    return render_template('register.html')


@app.route('/myanonymous/<username>', methods=['GET', 'POST'])
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
        return 'successful'

    elif request.method == 'GET':
        if User.query.filter_by(user_name_hash=username).first():
            print(username)
            return render_template('secretmessage.html')

        else:

            return redirect('/404')


@app.route('/message', methods=['POST', 'GET'])
def message():
    user_name = session.get('username')
    a = User.query.filter_by(user_name=user_name).first()
    #  if not session.get('username'):
    #     return redirect('/signup')

    return render_template('messages.html', a=a)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorpage.html'), 404


@app.route('/logout')
def logout():
    session['username'] = None
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
