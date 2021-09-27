from flask import Flask, flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sys
import os
from datetime import datetime
from helpers import login_required, key_generator, datetime, dollar, coins, CURRENT_RATE
from captcha.image import ImageCaptcha
import base64
from threading import Lock
from datetime import datetime as dt

# Configure application
app = Flask(__name__)
db = SQLAlchemy(app)

from tables import User, Work, Transactions, Items
#configure DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test8.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_2')

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configute the amount of false captchas befor user gets banned
BAN_COUNT = 7

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
        cash = 0
        key = "CC$" + key_generator(15)
        public_key = key_generator(10)
        # Check if keys are already in user
        # TO-DO check if this works
        if public_key in User.query.filter_by(public_key = public_key).all() or  key in User.query.filter_by(key = key).all():
            return redirect("/register")
        new_data = User(name, key, public_key, cash)
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
image = ImageCaptcha(width=350, height=200, fonts = ['/app/static/arial.ttf'])
# Initiate key
# Assing a value here already to prevent usein the function upper() on nontype value in case the site dosen't (re) load properly
key = key_generator(5)

@app.route("/work", methods=["GET", "POST"])
@login_required
def work():
    key = key_generator(5)
    new_data = Work(session["user_id"],key, 0,0,0)
    db.session.add(new_data)
    db.session.commit()
    # get current cash
    user = User.query.filter_by(_id = session["user_id"]).first()
    cash = user.cash
    work = Work.query.order_by(Work.timestamp.desc()).filter_by(user_id = session["user_id"]).first()
    time = 0
    avg_time = 0
    sucess_rate = 0
    ban = False
    if work is not None:
        time = work.time
        avg_time = Work.query.filter_by(user_id = session["user_id"]).with_entities(func.avg(Work.time)).first()[0]
        wrong_count = 0
        wrong = Work.query.order_by(Work.timestamp.desc()).filter_by(user_id = session["user_id"]).all()
        if len(wrong) >= BAN_COUNT:
            for i in range(BAN_COUNT):
                if wrong[i].success is False:
                    wrong_count += 1
        if wrong_count >= BAN_COUNT:
            ban = True
        work_all =  Work.query.filter_by(user_id = session["user_id"]).all()
        success_count = 0
        for row in work_all:
            if row.success == True:
                success_count += 1
        sucess_rate = round(((success_count/ len(work_all))*100), 2)
    # Generate and write image
    data = image.generate(key)
    encoded_img_data = base64.b64encode(data.getvalue())
    return render_template("work.html", captcha = encoded_img_data.decode('utf-8'), cash = cash, time = time, avg_time = round(avg_time, 2), sucess_rate = sucess_rate, ban = ban)

@app.route("/insights", methods=["GET"])
@login_required
def insights():
    avg_time = 0
    sucess_rate = 0
    work = Work.query.order_by(Work.timestamp.desc()).filter_by(user_id = session["user_id"]).first()
    if work is not None:
        time = work.time
        avg_time = Work.query.filter_by(user_id = session["user_id"]).with_entities(func.avg(Work.time)).first()[0]
        work_all =  Work.query.filter_by(user_id = session["user_id"]).all()
        success_count = 0
        for row in work_all:
            if row.success == True:
                success_count += 1
        sucess_rate = round(((success_count/ len(work_all))*100), 2)
    return render_template("insights.html", avg_time = round(avg_time, 2), sucess_rate = sucess_rate)

lock = Lock()
@app.route("/validate", methods=["GET", "POST"])
def validate():
    latest_work = Work.query.filter_by(user_id = session["user_id"]).order_by(Work._id.desc()).first()
    current_key = latest_work.key.upper()
    if request.method == "POST" and lock:
        lock.acquire()
        ts = dt.now().timestamp()
        key_input = request.form.get('key').upper()
        time = request.form.get('time')
        point = 1
        # Prevent user from submitting multiple times and getting multiple points
        if current_key == key_input:
            success = True
            user = User.query.filter_by(_id = session["user_id"]).first()
            user.cash = user.cash + point
            db.session.commit()
            flash('1 Coin', 'point')
        else:
            success = False
            flash('try again', 'no_point')
        latest_work.success = success
        latest_work.timestamp = ts
        latest_work.time = time
        db.session.commit()
        lock.release()
        return redirect("/work")

@app.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    user = User.query.filter_by(_id = session["user_id"]).first()
    all_user = User.query.all()
    if request.method == "POST":
        ts = dt.now().timestamp()
        receiver = request.form.get("receiver")
        amount = int(request.form.get("amount"))
        # if sender has not enough money
        if float(amount) > float(user.cash):
            return render_template("transfer.html", enough = False, cash = user.cash)
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
    return render_template("transfer.html", cash = user.cash, persons = all_user)

@app.route("/blockchain", methods=["GET", "POST"])
@login_required
def blockchain():
    # store data in table
    table = Transactions.query.all()
    for row in table:
        row.sender_name = User.query.filter_by(_id = row.sender_id).first().name
        row.receiver_name = User.query.filter_by(_id = row.receiver_id).first().name
    return render_template("blockchain.html", table = table)

@app.route("/shop", methods=["GET", "POST"])
@login_required
def shop():
    user = User.query.filter_by(_id = session["user_id"]).first()
    shop_items = Items.query.all()
    inventory = Items.query.all()
    for row in shop_items:
        row.owner_name = User.query.filter_by(_id = row.owner_id).first().name
    if request.method == "POST":
        items_str = request.form.get("cart_items")
        items = items_str.split(",");
        total = 0
        # Calculate price
        for item in shop_items:
            if str(item._id) in items:
                total += float(item.price)*CURRENT_RATE
        if user.cash < float(total) and total > 0:
            rest = float(total) - float(user.cash)
            return render_template("shop.html", inventory = inventory, rest = round(rest, 2))
        ts = dt.now().timestamp()
        # Change owner and add to blockchain shop -> user
        for item in shop_items:
            if str(item._id) in items:
                item.owner_id = user._id
                new_data = Transactions(1, item.name, session["user_id"], ts)
                db.session.add(new_data)
        user.cash -= round(total, 2);
        user.cash = round(user.cash, 2)
        # Add to Blockchain user -> Shop
        new_data = Transactions(session["user_id"], round(total, 2), 1, ts)
        db.session.add(new_data)
        db.session.commit()
        return redirect("/items")
    return render_template("shop.html", inventory = inventory, rest = None)

@app.route("/items", methods=["GET", "POST"])
def items():
    all_user = User.query.all()
    items = Items.query.filter_by(owner_id = session["user_id"]).all()
    if request.method == "POST":
        ts = dt.now().timestamp()
        receiver = request.form.get("key")
        receiver_info = User.query.filter_by(public_key = receiver).first()
        if receiver_info is None:
            flash("This receiver does not exist", "error")
            return render_template("items.html", items = items)
        receiver_id = receiver_info._id
        item = request.form.get("item")
        # Query specific item to set the new owner
        this_item = Items.query.filter_by(_id = item).first()
        this_item.owner_id = receiver_id
        new_data = Transactions(session["user_id"], this_item.name, receiver_id, ts)
        db.session.add(new_data)
        db.session.commit()
        flash("Transaction successful", "success")
    return render_template("items.html", items = items, persons = all_user)


@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")


# Custom filter
app.jinja_env.filters["datetime"] = datetime
app.jinja_env.filters["dollar"] = dollar
app.jinja_env.filters["coins"] = coins
