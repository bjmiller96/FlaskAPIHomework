from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def sign_up():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(email, password = password)
            
            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account at {email}', 'user-created')
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')
    return render_template('sign_up.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def sign_in():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash("You're logged in!", 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash("You email 0r password is incorrect.", 'auth-failed')
                return redirect(url_for('auth.sign_in'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')
    return render_template('sign_in.html', form = form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))