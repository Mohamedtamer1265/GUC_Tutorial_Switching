from flask import Blueprint,render_template # branch of roots
from flask_login import login_required,current_user
views = Blueprint('views',__name__)


@views.route('/') #endpoint
def home():
    return render_template("home.html")