from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf

def setup_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    #app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_secret_key')
    #app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///fallback.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://efraimzetterqvist:@localhost/dodgeball_throws'
    csrf = CSRFProtect(app)
    db = SQLAlchemy(app)
    return app, csrf, db

