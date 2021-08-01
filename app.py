from flask import Flask, flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sys
import os
from datetime import datetime

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

    def __init__(self, name, email):
        self.name = name
        self.mail = mail
        self.key = key

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        submit = request.form.get("key")
        return render_template("login.html", submit = submit)
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        mail = request.form.get("mail")
        key = generate_password_hash(name, method='pbkdf2:sha256', salt_length=4)
        new_data = User(name, mail, key)
        db.session.add(new_data)
        db.session.commit()
        return render_template("register.html", key = key)
    return render_template("register.html")

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session["user_id"] = None
    return render_template("logout.html")


@app.route("/work", methods=["GET", "POST"])
@login_required
def work():
    return render_template("work.html")
