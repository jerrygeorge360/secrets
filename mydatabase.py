from datetime import datetime

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"{self.id, self.user_name, self.date}"


db.create_all()
