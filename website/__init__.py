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

    return app