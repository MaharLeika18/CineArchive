from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<h1>Login</h1>"  # Change this into the right template

@auth.route('/logout')
def logout():
    return "<h1>Logout</h1>"  # Change this into the right template

@auth.route('/sign-up')
def sign_up():
    return "<h1>Sign Up</h1>"  # Change this into the right template