from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model):
    __tablename__ = 'user'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    public_key = db.Column(db.String(100), nullable=False)
    cash = db.Column(db.Integer, default=0)

    def __init__(self, name, key, public_key, cash):
        self.name = name
        self.key = key
        self.public_key = public_key
        self.cash = cash

class Work(db.Model):
    __tablename__ = 'work'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    key = db.Column(db.String(100))
    time = db.Column(db.Float)
    success = db.Column(db.Boolean)
    timestamp = db.Column(db.Numeric)

    def __init__(self, user_id,key, time, success, timestamp):
        self.user_id = user_id
        self.key = key
        self.time = time
        self.success = success
        self.timestamp = timestamp


class Transactions(db.Model):
    __tablename__ = 'transactions'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Numeric, nullable=False)

    def __init__(self, sender_id, amount, receiver_id, timestamp):
        self.sender_id = sender_id
        self.amount = amount
        self.receiver_id = receiver_id
        self.timestamp = timestamp
        self.sender_name = None
        self.receiver_name = None

class Items(db.Model):
    __tablename__ = 'items'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100))
    type = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer)
    edition = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, default=0)


    def __init__(self, _id, name, price, img, content, type, duration, edition, owner_id):
        self._id = _id
        self.name = name
        self.price = price
        self.img = img
        self.content = content
        self.type = type
        self.duration = duration
        self.edition = edition
        self.owner_id = owner_id
        self.owner_name = None
