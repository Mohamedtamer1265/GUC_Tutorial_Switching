from flask import Flask
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv
db = SQLAlchemy()
DB_NAME = "students.db"

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all route
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', os.getenv('Db_pass'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() == 'true'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix ='/')
    app.register_blueprint(auth, url_prefix ='/')

    from .model import User
    create_database(app)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    #If a user tries to access a route that requires login but isn't authenticated, they will be redirected to the auth.login route.
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
      return User.query.get(int(user_id))
    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        print('Database tables created!')

