from functools import wraps
from flask import request, redirect, url_for, session
from flask_session import Session
import string
import random


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
