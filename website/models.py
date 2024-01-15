from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UUID = db.Column(db.String(100), unique=True)
    title_before = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    middle_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    title_after = db.Column(db.String(20))
    picture_url = db.Column(db.String(200))
    location = db.Column(db.String(50)) 
    claim = db.Column(db.String(100))
    bio = db.Column(db.String(1000))
    tags = db.relationship('Tag')
    price_per_hour = db.Column(db.Integer)
    contact = db.relationship('Contact')
    
    
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telephone_numbers = db.Column(db.String(100))
    emails = db.Column(db.String(100))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
   
    

    
