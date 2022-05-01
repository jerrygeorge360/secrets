from app import redirect, db, session#,Session
import mydatabase


class Authorize:
    msg = ''

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        if not self.username or not self.password:
            self.msg = 'You damn idiot fill in the required field.'
            return f'<alert>{self.msg}</alert>'
        else:
            try:
                if db.session.query(mydatabase.User).filter_by(user_name=self.username, password=self.password).first():
                    session['username'] = self.username
                    return redirect('/index')
                elif not db.session.query(mydatabase.User).filter_by(user_name=self.username, password=self.password).first():
                    return redirect('/signup', code=302)

            except Exception as err:
                self.msg = str(err)
                return redirect('/', code=302)
            return self.msg

    def signup(self):
        if not self.username or not self.password:
            self.msg = 'You damn idiot fill in the required field.'
            return {self.msg}
        elif len(self.password) < 6:
            self.msg = 'You security hater ,will you choose a longer password.'
            return {self.msg}
        elif db.session.query(mydatabase.User).filter_by(user_name=self.username).first():
            self.msg = 'Choose another username you toad.'
            return self.msg
        else:
            try:
                user = mydatabase.User(password=self.password, user_name=self.username)
                db.session.add(user)
                db.session.commit()
                self.msg = 'ok'
                return redirect('/signin', code=302)
            except Exception as err:
                # print('Register error: ' + err)
                self.msg = str(err)
            return self.msg
