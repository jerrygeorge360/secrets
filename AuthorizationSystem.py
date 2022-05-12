from app import redirect, db, session, make_response,render_template,flash  # ,Session
import mydatabase
from passlib.hash import cisco_type7


class Authorize:
    msg = ''

    def __init__(self, username, password):
        self.username = username
        self.hash_user_name = cisco_type7.hash(self.username)
        self.password = password

    def login(self):
        if not self.username or not self.password:
            self.msg = 'You damn idiot fill in the required field.'
            return make_response(render_template('login.html',error=self.msg),412)
        else:
            try:
                database_object=db.session.query(mydatabase.User).filter_by(user_name=self.username, password=self.password).first()
                if database_object:
                    session['username'] = self.username
                    session['hash_name']=database_object.user_name_hash

                    flash('login successful','success')
                    return redirect('/message')
                elif not db.session.query(mydatabase.User).filter_by(user_name=self.username,
                                                                     password=self.password).first():
                    error='username or password incorrect'
                    return render_template('login.html',error=error)

            except Exception as err:
                self.msg = str(err)
                return redirect('/', code=302)
            return self.msg

    def signup(self):
        if not self.username or not self.password:
            self.msg = 'You damn idiot fill in the required field.'
            return make_response(render_template('register.html',error=self.msg),412)
        elif len(self.password) < 6:
            self.msg = 'You security hater ,will you choose a longer password.'
            return make_response(render_template('register.html',error=self.msg),412)
        elif db.session.query(mydatabase.User).filter_by(user_name=self.username).first():
            self.msg = 'Choose another username you toad.'
            return make_response(render_template('register.html',error=self.msg),412)

        else:
            try:
                user = mydatabase.User(password=self.password, user_name=self.username,
                                       user_name_hash=self.hash_user_name)
                db.session.add(user)
                db.session.commit()
                self.msg = 'ok'
                my_object = db.session.query(mydatabase.User).filter_by(user_name=self.username).first()
                flash(f'Registration successful.Link generated', 'success')
                return make_response(render_template('register.html', url_name=my_object.user_name_hash, msg=self.msg),200)

            except Exception as err:
                # print('Register error: ' + err)
                self.msg = str(err)
                render_template('register.html', error=self.msg)
            return self.msg
