from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p>log in</p>"

@auth.route('/logout')
def logout():
    return "<p>log out</p>"

@auth.route('/sign-up')
def sign_up():
    return "<p>sign up</p>"