from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask import Flask
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import login_user, login_required, logout_user, current_user
from .models import Tag, Teacher, Contact
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import shutil
from . import db, create_app
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from base64 import b64encode
import json
import codecs



views = Blueprint('views', __name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['UPLOAD_FOLDER'] = 'static/files'

api = Blueprint('api', __name__)

def load_json_data(file_path):
    with codecs.open(file_path, 'r', 'utf-8') as file:
        data = json.load(file)
        # Explicitly encode string values to UTF-8
        if isinstance(data, dict):
            data = {k: v.encode('utf-8').decode('utf-8') if isinstance(v, str) else v for k, v in data.items()}
            
        
        return data
def listToString(s):
 
    # initialize an empty string
    str1 = " "
 
    # return string
    return (str1.join(s))

def save_json_data(data):
    print(listToString(data.get("contact", {}).get("telephone_numbers", [])))
    teacher = Teacher(
        UUID=data.get("UUID"),
        title_before=data.get("title_before"),
        first_name=data.get("first_name"),
        middle_name=data.get("middle_name"),
        last_name=data.get("last_name"),
        title_after=data.get("title_after"),
        picture_url=data.get("picture_url"),
        location=data.get("location"),
        claim=data.get("claim"),
        bio=data.get("bio"),
        price_per_hour=data.get("price_per_hour")
    )
    tags = [Tag(uuid=tag["uuid"], name=tag["name"]) for tag in data.get("tags", [])]
    teacher.tags = tags
    
    telephone_numbers=listToString(data.get("contact", {}).get("telephone_numbers", []))
    emails=listToString(data.get("contact", {}).get("emails", []))
     
    contact = Contact(telephone_numbers = telephone_numbers, emails = emails, teacher_id= data.get("UUID"))
    db.session.add(teacher)
    db.session.add(contact)
    db.session.commit()
    
def get_teacher_by_uuid(uuid):
    teacher = Teacher.query.filter_by(UUID=uuid).first()
    return teacher

def get_contact_by_uuid(uuid):
    contact = Contact.query.filter_by(teacher_id=uuid).first()
    
    return contact


@views.route('/', methods=['GET', 'POST'])
def home():
    # Get the list of all lecturers from the database
    all_lecturers = Teacher.query.all()
  
    return render_template("home.html", user=current_user, lecturers=all_lecturers)

@views.route('/lecturer/<uuid>', methods=['GET', 'POST'])

def profile(uuid):
    teacher = get_teacher_by_uuid(uuid)
    contact = get_contact_by_uuid(uuid)
   
    return render_template('lecturer.html', teacher=teacher, contact=contact)





  

