# type: ignore
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

    if not firebase_admin._apps:  # Only initialize Firebase once
        try:
            cred_path = r"C:\Users\Axel\School-Repositories\privatekey\firebaseKey.json"
            #cred_path = r"C:\Users\xlea\OneDrive\Skrivbord\privatekey1.json"
            print(f"Attempting to initialize Firebase with credentials file: {cred_path}")
            
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully.")
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            return app

    # Initialize Firestore
    db = firestore.client()

    from .views import views

    app.register_blueprint(views, url_prefix='/')
    #prefix can be changed to e.g /auth/ for different route

    return app