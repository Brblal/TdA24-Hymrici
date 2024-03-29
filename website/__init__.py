from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager



db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
        app.config['UPLOAD_FOLDER'] = 'static/files'
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
        db.init_app(app)
        

        
        

        from .views import views
        from .auth import auth
        from .api import api

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')
        app.register_blueprint(api, url_prefix='/api')

        from .models import Tag, Teacher, Contact
        
        with app.app_context():
                create_database(app)
        
        
        
        return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database!')

