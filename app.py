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

# Configure application
app = Flask(__name__)

#configure DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_1')

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    cash = db.Column(db.Integer, default=0)

    def __init__(self, name, mail, key, cash):
        self.name = name
        self.mail = mail
        self.key = key
        self.cash = cash

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
    name = db.session.execute("SELECT name from user WHERE _id = :id",{"id": session["user_id"]}).first()
    name = db.session.execute('SELECT name from user WHERE _id = :id', {"id": session["user_id"]}).first()
    return render_template("index.html", name = name[0])


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
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        mail = request.form.get("mail")
        cash = 0
        key = generate_password_hash(name, method='pbkdf2:sha256', salt_length=4)
        new_data = User(name, mail, key, cash)
        db.session.add(new_data)
        db.session.commit()
        return render_template("register.html", key = key)
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
    return render_template("work.html")
    # get current cash
    cash = db.session.execute("SELECT cash FROM user WHERE _id = :id", {"id": session["user_id"]}).first()
    # acess global variable key and st it to random key
    global key
    key = key_generator()
    # Generate and write image
    data = image.generate(key)
    image.write(key, 'out.png')
    encoded_img_data = base64.b64encode(data.getvalue())
    return render_template("work.html", captcha = encoded_img_data.decode('utf-8'), cash = cash[0])

@app.route("/validate", methods=["GET", "POST"])
def validate():
        if request.method == "POST":
            key_input = request.form.get('key').upper()
            if key.upper() == key_input:
                point = 1
                db.session.execute("UPDATE user SET cash = cash + :point WHERE _id = :id", {"point": point, "id":session["user_id"] })
                db.session.commit()
            else:
                print("NO POINT", key.upper(), key_input)
        return redirect("/work")
