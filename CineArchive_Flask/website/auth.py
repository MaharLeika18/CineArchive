from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            stmt = text("CALL get_user_credentials(:uname)")
            result = db.session.execute(stmt, {'uname': username}).fetchone()

            if result:
                user_id, uname, stored_hash = result
                if check_password_hash(stored_hash, password):
                    user = User.query.get(user_id)
                    login_user(user)
                    flash('Logged in successfully!', 'success')
                    return redirect(url_for('views.view_watchlist'))
                else:
                    flash('Incorrect password.', 'danger')
            else:
                flash('Username not found.', 'warning')

        except Exception as e:
            db.session.rollback()
            flash(f"Login error: {e}", 'danger')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        if password != confirm:
            flash('Passwords do not match.', 'warning')
            return redirect(url_for('auth.register'))

        hashed = generate_password_hash(password)

        try:
            stmt = text("CALL register_user(:uname, :p_hash)")
            db.session.execute(stmt, {'uname': username, 'p_hash': hashed})
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'danger')

    return render_template('register.html')