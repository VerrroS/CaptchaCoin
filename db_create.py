from app import db, app
from tables import User, Work, Transactions, Items
from flask_sqlalchemy import SQLAlchemy
import os
db.create_all()

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test8.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('HEROKU_POSTGRESQL_NAVY_URL')

# initialize shop as 1st user
name = "Shop"
cash = 0
key = ""
public_key = "send_to_shop"
new_data = User(name, key, public_key, cash)
db.session.add(new_data)
db.session.commit()

def populate_shop():
    for i in range(6):
        id = i+1
        name = "mug - not a robot"
        price = 10
        img = "/static/mug.jpg"
        content = "/static/mug_loop.mp4"
        type = "gif"
        duration = 5
        edition = "%d/6" % (i+1)
        owner_id = 1
        link = "https://veronikasimmering.de/mug_loop.mp4"
        new_data = Items(id, name, price, img, content, type, duration, edition, owner_id, link)
        db.session.add(new_data)
    for i in range(6):
        id = i+ 7
        name = "shirt - no robot allowed"
        price = 20
        img = "/static/shirt.jpg"
        type = "jpg"
        duration = 0
        content = ""
        edition = "%d/6" % (i+1)
        owner_id = 1
        link = "https://veronikasimmering.de/shirt.jpg"
        new_data = Items(id, name, price, img, content, type, duration, edition, owner_id, link)
        db.session.add(new_data)
    for i in range(6):
          id = i+ 13
          name = "desktop background"
          price = 0.1
          img = "/static/background_q.png"
          type = "png"
          duration = 0
          content = ""
          owner_id = 1
          edition = "%d/6" % (i+1)
          link = "https://veronikasimmering.de/background.png"
          new_data = Items(id, name, price, img, content,type, duration,edition, owner_id, link)
          db.session.add(new_data)
    db.session.commit()
populate_shop()
