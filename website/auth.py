from flask import Blueprint, render_template, request, flash, get_flashed_messages, redirect, url_for  # Importing necessary Flask functions
from .model import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from sqlalchemy import and_, or_, case, not_
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        data = request.form
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            flash('complete your data', category='error')
        elif email and not email.endswith('@student.guc.edu.eg'):
            flash('Write your email correctly', category='error')
        else:
            user = User.query.filter_by(email=email).first() 
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)  # remember him that he logged in before
                    flash('login successful', category='success')
                    return redirect(url_for('auth.query', user_id=user.id))
                else:
                    flash('Incorrect Password', category='error')
            else:
                flash('email does not exist', category='error')
        return render_template("login.html", boolean=True)
    return render_template("login.html", boolean=True)

@auth.route('/logout')
@login_required 
def logout():
    logout_user() 
    return redirect(url_for('auth.login')) 

@auth.route('/delete')
@login_required
def delete():
    try:
        user = current_user
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash('Your account has been successfully deleted.', category='success')
    except Exception:
        db.session.rollback()
        flash('An error occurred while deleting your account. Please try again later.', category='error')
    return redirect(url_for('auth.login'))

from flask_login import current_user, login_required



@auth.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if current_user.is_authenticated:  # Ensure the user is authenticated
        user = current_user  # Get the logged-in user
        if request.method == 'POST':
            # Get updated data from the form
            user.name = request.form['name']
            user.current_group = request.form['current_group']
            user.current_tut = request.form['current_tutorial']
            user.desired_group_1 = request.form['desired_group1']
            user.desired_tut_1 = request.form['desired_tutorial1']
            user.desired_group_2 = request.form['desired_group2']
            user.desired_tut_2 = request.form['desired_tutorial2']
            user.telephone = request.form['phone']
            if int(user.current_group) > 10 or int(user.current_group) < 0 or int(user.desired_group_1) > 10 or int(user.desired_group_1) < 0 or int(user.desired_group_2) > 10 or int(user.desired_group_2) < 0:
                flash('Group must be an integer between 1 and 10.', category='error')
            else:
              db.session.commit()
              flash('Your information has been updated successfully!', 'success')
              return redirect(url_for('auth.query', user_id=user.id))
        return render_template('update.html')
    else:
        flash('You need to be logged in to update your information.', 'danger')
        return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    fields = {
        'email': None,
        'name': None,
        'user_id': None,
        'password': None,
        'phone': None,
        'major': None,
        'semester': None,
        'english': None,
        'german': None,
        'current_group': None,
        'current_tutorial': None,
        'desired_group1': None,
        'desired_tutorial1': None,
        'desired_group2': None,
        'desired_tutorial2': None
    }

    if request.method == 'POST':  # Check if the request method is POST
        # Extract form data
        data = request.form
        fields = {
            'email': data.get('email', None),
            'name': data.get('name', None),
            'user_id': data.get('id', None),
            'password': data.get('password', None),
            'phone': data.get('phone', None),
            'major': data.get('major', None),
            'semester': int(data.get('semester', None)) if data.get('semester') else None,
            'english': data.get('english', None),
            'german': data.get('german', None),
            'current_group': int(data.get('current_group', None)) if data.get('current_group') else None,
            'current_tutorial': int(data.get('current_tutorial', None)) if data.get('current_tutorial') else None,
            'desired_group1': int(data.get('desired_group1', None)) if data.get('desired_group1') else None,
            'desired_tutorial1': int(data.get('desired_tutorial1', None)) if data.get('desired_tutorial1') else None,
            'desired_group2': int(data.get('desired_group2', None)) if data.get('desired_group2') else None,
            'desired_tutorial2': int(data.get('desired_tutorial2', None)) if data.get('desired_tutorial2') else None
        }

        flash_message_set = False  # Flag to check if a flash message is already set

        # Check if email already exists
        user = User.query.filter_by(email=fields['email']).first()
        if user and not flash_message_set:
            flash('Email already exists', category='error')
            flash_message_set = True
        
        existing_user = User.query.filter_by(user_id=fields['user_id']).first()
        if existing_user and not flash_message_set:
            flash('User with this ID already exists!', 'error')
            flash_message_set = True  
        
        # Form validation logic
        for field, value in fields.items():
            if value is None or value == '':
                if not flash_message_set:
                    flash(f'{field.replace("_", " ").capitalize()} is required.', category='error')
                    flash_message_set = True
                break

        # Email validation
        if fields['email'] and not fields['email'].endswith('@student.guc.edu.eg'):
            if not flash_message_set:
                flash('Email must end with @student.guc.edu.eg', category='error')
                flash_message_set = True
        
        # Password validation
        elif fields['password'] and len(fields['password']) < 6:
            if not flash_message_set:
                flash('Password must be at least 6 characters long.', category='error')
                flash_message_set = True
        
        # Group validation (ensure values are integers and between 1-10)
        elif (fields['current_group'] and (fields['current_group'] < 0 or fields['current_group'] > 10)) or \
             (fields['desired_group1'] and (fields['desired_group1'] < 0 or fields['desired_group1'] > 10)) or \
             (fields['desired_group2'] and (fields['desired_group2'] < 0 or fields['desired_group2'] > 10)):
            if not flash_message_set:
                flash('Group must be an integer between 1 and 10.', category='error')
                flash_message_set = True

        # If there are no flash messages, proceed with user creation
        if not flash_message_set:  # Only proceed if no flash message has been triggered
            new_user = User(name=fields['name'], email=fields['email'], telephone=fields['phone'], major=fields['major'],
                            semester=fields['semester'], english_level=fields['english'], german_level=fields['german'],
                            current_group=fields['current_group'], current_tut=fields['current_tutorial'],
                            desired_group_1=fields['desired_group1'], desired_tut_1=fields['desired_tutorial1'],
                            desired_group_2=fields['desired_group2'], desired_tut_2=fields['desired_tutorial2'],
                            password=generate_password_hash(fields['password'], method='pbkdf2:sha256'), user_id=fields['user_id'])
            db.session.add(new_user)
            db.session.commit()
            flash('Account successfully created!', category='success')
            login_user(new_user, remember=True)  # remember him that he logged in before
            return redirect(url_for('auth.login'))  # Redirect to login after successful signup

        # If there are flash messages, pass the entered data back to the template
        return render_template("sign_up.html", data=fields)

    # Handle GET request (when the form is first accessed)
    return render_template("sign_up.html", data=fields)

@auth.route('/query', methods=['GET'])
@login_required
def query():
    requested_user_id = request.args.get('user_id')

    if requested_user_id and int(requested_user_id) != current_user.id: 
        return redirect(url_for('auth.query', user_id=current_user.id))

    user = current_user
    users = User.query.filter(
        and_(
            User.major == user.major,
            User.english_level == user.english_level,
            User.german_level == user.german_level,
            User.semester == user.semester,
            not_(User.id == user.id)
        )
    ).order_by(
        case(
            # Each condition must be a tuple with the first element being the condition and
            # the second element being the value to return when the condition is true
            (and_(
                User.current_group == user.desired_group_1,
                User.current_tut == user.desired_tut_1,
                User.desired_group_1 == user.current_group,
                User.desired_tut_1 == user.current_tut
            ), 0),

            (and_(
                User.current_group == user.desired_group_1,
                User.current_tut == user.desired_tut_1,
                User.desired_group_2 == user.current_group,
                User.desired_tut_2 == user.current_tut
            ), 1),

            (and_(
                User.current_group == user.desired_group_2,
                User.current_tut == user.desired_tut_2,
                User.desired_group_1 == user.current_group,
                User.desired_tut_1 == user.current_tut
            ), 2),

            (and_(
                User.current_group == user.desired_group_2,
                User.current_tut == user.desired_tut_2,
                User.desired_group_2 == user.current_group,
                User.desired_tut_2 == user.current_tut
            ), 3),

            (and_(
                User.current_group == user.desired_group_1,
                User.desired_group_1 == user.current_group
            ), 4),

            (and_(
                User.current_group == user.desired_group_1,
                User.desired_group_2 == user.current_group
            ), 5),

            (and_(
                User.current_group == user.desired_group_2,
                User.desired_group_1 == user.current_group
            ), 6),

            (and_(
                User.current_group == user.desired_group_2,
                User.desired_group_2 == user.current_group
            ), 7),
              (and_(
                User.current_group == user.desired_group_1,
            ), 8),
              (and_(
                User.current_group == user.desired_group_2,
            ), 9),

            # Default case (else_)
            else_=10
        ),
         User.id.desc()
    ).all()
    return render_template('query.html', users=users)
