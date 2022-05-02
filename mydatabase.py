from datetime import datetime

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, unique=True)
    user_name_hash=db.Column(db.String)
    password = db.Column(db.String)
    posts = db.relationship("SecretMessage", backref="receiver", lazy=True)

    def __repr__(self):
        return f"{self.id, self.user_name}"


class SecretMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)

    def __repr__(self):
        return f"{self.id, self.message}"


db.create_all()
