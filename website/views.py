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

def load_json_data(file_path):
    with codecs.open(file_path, 'r', 'utf-8') as file:
        data = json.load(file)
        # Explicitly encode string values to UTF-8
        if isinstance(data, dict):
            data = {k: v.encode('utf-8').decode('utf-8') if isinstance(v, str) else v for k, v in data.items()}
        return data

@views.route('/', methods=['GET', 'POST'])
def home():          
        

    
    return render_template("home.html", user=current_user)


  

@views.route('/lecturer', methods=['GET', 'POST'])
def profile():
    data = load_json_data('data/lecturer.json')
    return render_template('lecturer.html', data=data)

