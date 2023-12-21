from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask import Flask
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_login import login_user, login_required, logout_user, current_user
from .models import Entry, User, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import shutil
from . import db, create_app
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from base64 import b64encode
import json

views = Blueprint('views', __name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['UPLOAD_FOLDER'] = 'static/files'
@app.route('/api/process', methods=['POST'])

def process():
    data = request.get_json()
    # process the data
    result = {'message': 'Processed successfully'}
    return jsonify(result)

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")    
    

@views.route('/', methods=['GET', 'POST'])
def home():          
        

    
    return render_template("home.html", user=current_user)


  

@views.route('/lecturer', methods=['GET', 'POST'])
def profile():
    image = url_for('static', filename='prof.png')


    text = url_for('static', filename="files/img/zaklad.png")    

            
    
    return render_template("lecturer.html", user=current_user, text=text, )

