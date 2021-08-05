from functools import wraps
from flask import request, redirect, url_for, session
from flask_session import Session
import string
import random
from datetime import datetime as dt
import numpy

# Use decorator function to ensure that login is required
#https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


#random key generator found here https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
def key_generator(size=7, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def datetime(value):
    """Format timestap into readable valus"""
    return dt.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

def exchange(coin_dollar):
    value = coin_dollar + numpy.random.normal(0, 2)
    if value < 0:
        value = 0
    return value

CURRENT_RATE = exchange(1000)

def dollar(coins):
    return f"{(coins/CURRENT_RATE):,.2f}"

def coins(dollar):
    return f"{(dollar*CURRENT_RATE):,.2f}"



# While I dont have engough items for the shop use this to populate shop site
inventory = []
for i in range(6):
    inventory.append({"id": i, "img": "static/mug.jpg", "price": 10, "edition": i+1, "name": "mug - not a robot"})


#inventory = [
#{'img': 'static/mug.jpg',
#'price': 10,
#'name': 'mug - not a robot'}
#]
