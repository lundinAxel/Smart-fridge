import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask

db = None

def create_app():
    global db

    # Create a Flask app instance
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'database'

    # Firebase setup with credentials file
    cred = credentials.Certificate(r"C:\Users\Axel\School-Repositories\firebase-private-key\firebase-private-key.json")
    firebase_admin.initialize_app(cred)

    # Initialize Firestore
    db = firestore.client()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    #prefix can be changed to e.g /auth/ for different route
    app.register_blueprint(auth, url_prefix='/')

    return app