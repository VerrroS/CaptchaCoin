from flask import Flask, flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sys
import os
from datetime import datetime
from helpers import login_required, key_generator
from captcha.image import ImageCaptcha
import base64
import datetime;

# Configure application
app = Flask(__name__)

#configure DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test6.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_1')

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

class work(db.Model):
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
    info = db.session.execute('SELECT name, cash, public_key from user WHERE _id = :id', {"id": session["user_id"]}).first()
    return render_template("index.html", name = info[0], cash = info[1], public_key = info[2])


@app.route("/login", methods=["GET", "POST"])
def login():
    #clear all sessions
    session.clear()
    if request.method == "POST":
        key = request.form.get("key")
        user = db.session.execute('SELECT name, _id from user WHERE key = :key', {"key": key}).first()
        if user is not None:
            session["user_id"] = user[1]
            return render_template("index.html", name = user[0])
        return render_template("login.html", incorrect = True)
    return redirect("/")

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
        if public_key in db.session.execute("SELECT public_key FROM user").all() or key in db.session.execute("SELECT key FROM user").all():
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
    cash = db.session.execute("SELECT cash FROM user WHERE _id = :id", {"id": session["user_id"]}).first()
    time = db.session.execute("SELECT time FROM work WHERE user_id = :id ORDER BY timestamp DESC", {"id": session["user_id"]}).first()
    avg_time = db.session.execute("SELECT AVG(time) FROM work WHERE user_id = :id", {"id": session["user_id"]}).first()
    if time is not None:
        time = time[0]
    # acess global variable key and st it to random key
    global key
    key = key_generator()
    # Generate and write image
    data = image.generate(key)
    encoded_img_data = base64.b64encode(data.getvalue())
    return render_template("work.html", captcha = encoded_img_data.decode('utf-8'), cash = cash[0], time = time, avg_time = round(avg_time[0], 2))

@app.route("/validate", methods=["GET", "POST"])
def validate():
        if request.method == "POST":
            ts = datetime.datetime.now().timestamp()
            key_input = request.form.get('key').upper()
            time = request.form.get('time')
            if key.upper() == key_input:
                point = 1
                success = True
                db.session.execute("UPDATE user SET cash = cash + :point WHERE _id = :id", {"point": point, "id":session["user_id"] })
                db.session.commit()
                flash('+1 Coin', 'point')
            else:
                success = False
                flash('try again', 'no_point')
        db.session.execute("INSERT INTO work (user_id, time, success, timestamp) VALUES (:user_id, :time, :success, :timestamp)", {"user_id":session["user_id"], "time":time, "success":success, "timestamp": ts})
        db.session.commit()
        return redirect("/work")

@app.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    sender_cash = db.session.execute("SELECT cash FROM user WHERE _id = :id", {"id": session["user_id"]}).first()
    if request.method == "POST":
        ts = datetime.datetime.now().timestamp()
        receiver = request.form.get("receiver")
        amount = request.form.get("amount")
        # if sender has not enough money
        if float(amount) > float(sender_cash[0]):
            return render_template("transfer.html", enough = False, cash = sender_cash[0])
        # if receiver does not exist
        if db.session.execute("SELECT COUNT(public_key) FROM user WHERE public_key = :public_key", {"public_key": receiver}).first()[0] < 1:
            return render_template("transfer.html", receiver = False, cash = sender_cash[0])
        receiver_id = db.session.execute("SELECT _id FROM user WHERE public_key = :receiver", {"receiver": receiver}).first()
        # add money to receiver
        db.session.execute("UPDATE user SET cash = cash + :amount WHERE public_key = :receiver", {"amount": amount, "receiver": receiver})
        # remove money from sender
        db.session.execute("UPDATE user SET cash = cash - :amount WHERE _id = :id", {"amount": amount, "id": session["user_id"]})
        # make transactions entry
        db.session.execute("INSERT INTO transactions (sender_id, receiver_id, amount, timestamp) VALUES(:sender_id, :receiver_id, :amount, :timestamp)",
        {"sender_id": session["user_id"], "receiver_id": receiver_id[0] , "amount": amount, "timestamp": ts})
        db.session.commit()
        return render_template("transfer.html", success = True, cash = sender_cash[0]- int(amount))
    return render_template("transfer.html", cash = sender_cash[0])

@app.route("/blockchain", methods=["GET", "POST"])
@login_required
def blockchain():
    # store data in table
    table = db.session.execute("SELECT sender_id, receiver_id, amount, timestamp FROM transactions").all()
    return render_template("blockchain.html", table = table)

@app.route("/shop", methods=["GET", "POST"])
@login_required
def shop():
    return render_template("shop.html")
