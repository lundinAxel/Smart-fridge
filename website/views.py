#Anything the user can navigate to, except authentication
from flask import Blueprint

views = Blueprint('views', __name__)

#defines route for the home page
@views.route('/') 
def home():
    return "<h1>Test</h1>"
