from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.user



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
