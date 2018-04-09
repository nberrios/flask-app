from flask import render_template, redirect, url_for, request, flash
from app.auth import bp
from app.auth.forms import LoginForm, UserRegistrationForm
from app.models.users import User
from app.db import db
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('keys.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('keys.index')
        return redirect(next_page)
    return render_template('login.html', title='Log in', login_form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('keys.index'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user = User(user_name=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created! Now go make some keys.')
        return redirect(url_for('keys.index'))
    return render_template('register.html', title='Create Account', register_form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
