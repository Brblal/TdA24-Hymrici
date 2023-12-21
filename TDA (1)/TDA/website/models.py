from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nametext = db.Column(db.String(50))
    date = db.Column(db.String)
    progLang = db.Column(db.String(50))
    rate = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    entry = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(50))
    user_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.Integer)
    entries = db.relationship('Entry')
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    Profile_pic = db.Column(db.BigInteger)
    
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User')
    
