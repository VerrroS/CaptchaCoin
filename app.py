from flask import Flask, flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sys
import os
from datetime import datetime
from helpers import login_required, key_generator, datetime
from captcha.image import ImageCaptcha
import base64
from datetime import datetime as dt

# Configure application
app = Flask(__name__)

#configure DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test7.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_1')

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    public_key = db.Column(db.String(100), nullable=False)
    cash = db.Column(db.Integer, default=0)

    def __init__(self, name, mail, key, public_key, cash):
        self.name = name
        self.mail = mail
        self.key = key
        self.cash = cash
        self.public_key = public_key

class Work(db.Model):
    __tablename__ = 'work'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    time = db.Column(db.Float)
    success = db.Column(db.Boolean)
    timestamp = db.Column(db.Numeric)

    def __init__(self, user_id, time, success, timestamp):
        self.user_id = user_id
        self.time = time
        self.success = success
        self.timestamp = timestamp


class Transactions(db.Model):
    __tablename__ = 'transactions'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Numeric, nullable=False)

    def __init__(self, sender_id, amount, receiver_id, timestamp):
        self.sender_id = sender_id
        self.amount = amount
        self.receiver_id = receiver_id
        self.timestamp = timestamp

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
@login_required
def index():
    # Get the users name if he is still logged in
    info = User.query.filter_by(_id = session["user_id"]).first()
    return render_template("index.html", info = info)


@app.route("/login", methods=["GET", "POST"])
def login():
    #clear all sessions
    session.clear()
    if request.method == "POST":
        key = request.form.get("key")
        user = User.query.filter_by(key=key).first()
        if user is not None:
            session["user_id"] = user._id
            return redirect("/")
        return render_template("login.html", incorrect = True)
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        mail = request.form.get("mail")
        cash = 0
        key = generate_password_hash(name, method='pbkdf2:sha256', salt_length=4)
        public_key = key_generator(10)
        # Check if keys are already in user
        # TO-DO check if this works
        if public_key in User.query.filter_by(public_key = public_key).all() or  key in User.query.filter_by(key = key).all():
            return redirect("/register")
        new_data = User(name, mail, key, public_key, cash)
        db.session.add(new_data)
        db.session.commit()
        return render_template("register.html", key = key, registered = True, public_key = public_key)
    return render_template("register.html")

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session["user_id"] = None
    return render_template("logout.html")


# Configute Image Captcha
# https://pypi.org/project/captcha/
#image = ImageCaptcha(fonts=['/path/A.ttf', '/path/B.ttf'])
# options https://www.code-learner.com/generate-graphic-verification-code-using-python-captcha-module/
image = ImageCaptcha(width=250, height=100)
# Initiate key
key = None

@app.route("/work", methods=["GET", "POST"])
@login_required
def work():
    # get current cash
    user = User.query.filter_by(_id = session["user_id"]).first()
    cash = user.cash
    work = Work.query.order_by(Work.timestamp.desc()).filter_by(user_id = session["user_id"]).first()
    time = 0
    avg_time = 0
    if work is not None:
        time = work.time
        avg_time = Work.query.filter_by(user_id = session["user_id"]).with_entities(func.avg(Work.time)).first()[0]
    # acess global variable key and st it to random key
    global key
    key = key_generator()
    # Generate and write image
    data = image.generate(key)
    encoded_img_data = base64.b64encode(data.getvalue())
    return render_template("work.html", captcha = encoded_img_data.decode('utf-8'), cash = cash, time = time, avg_time = round(avg_time, 2))

@app.route("/validate", methods=["GET", "POST"])
def validate():
        if request.method == "POST":
            ts = dt.now().timestamp()
            key_input = request.form.get('key').upper()
            time = request.form.get('time')
            if key.upper() == key_input:
                point = 1
                success = True
                user = User.query.filter_by(_id = session["user_id"]).first()
                user.cash = user.cash + point
                db.session.commit()
                flash('+1 Coin', 'point')
            else:
                success = False
                flash('try again', 'no_point')
        new_data = Work(session["user_id"],time, success, ts)
        db.session.add(new_data)
        db.session.commit()
        return redirect("/work")

@app.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    user = User.query.filter_by(_id = session["user_id"]).first()
    if request.method == "POST":
        ts = dt.now().timestamp()
        receiver = request.form.get("receiver")
        amount = int(request.form.get("amount"))
        # if sender has not enough money
        if float(amount) > float(user.cash):
            return render_template("transfer.html", enough = False, cash = sender_cash[0])
        # if receiver does not exist
        receiver_info = User.query.filter_by(public_key = receiver).first()
        if receiver_info is None:
            return render_template("transfer.html", receiver = False, cash = user.cash)
        receiver_id = receiver_info._id
        # add money to receiver
        receiver_info.cash = receiver_info.cash + amount
        # remove money from sender
        user.cash = user.cash - amount
        # make transactions entry
        new_data = Transactions(session["user_id"], amount, receiver_id, ts)
        db.session.add(new_data)
        db.session.commit()
        return render_template("transfer.html", success = True, cash = user.cash - amount)
    return render_template("transfer.html", cash = user.cash)

@app.route("/blockchain", methods=["GET", "POST"])
@login_required
def blockchain():
    # store data in table
    table = Transactions.query.all()
    return render_template("blockchain.html", table = table)

@app.route("/shop", methods=["GET", "POST"])
@login_required
def shop():
    return render_template("shop.html")


# Custom filter
app.jinja_env.filters["datetime"] = datetime
