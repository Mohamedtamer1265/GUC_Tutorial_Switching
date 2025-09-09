from . import db
from flask_login import UserMixin #

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255))
    telephone = db.Column(db.String(255), unique=True, nullable=True)
    user_id = db.Column(db.String(255))
    major = db.Column(db.String(255))
    semester = db.Column(db.Integer)
    english_level = db.Column(db.String(255))
    german_level = db.Column(db.Integer)
    current_group = db.Column(db.Integer)
    current_tut = db.Column(db.Integer)
    desired_group_1 = db.Column(db.Integer)
    desired_tut_1 = db.Column(db.Integer)
    desired_group_2 = db.Column(db.Integer)
    desired_tut_2 = db.Column(db.Integer)