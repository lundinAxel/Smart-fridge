# type: ignore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os

# Initialize Firestore DB
db = None

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    try:
        # Path to your Firebase credentials JSON file
        cred_path = r"C:\Users\xlea\OneDrive\Skrivbord\privatekey1.json"
        print(f"Attempting to initialize Firebase with credentials file: {cred_path}")
        
        # Load the credentials and initialize the Firebase app
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully.")
        
        # Initialize Firestore client
        db = firestore.client()
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        db = None

def load_calorie_data(filename):
    """Load calorie data from a JSON file."""
    if not os.path.exists(filename):
        print(f"File {filename} does not exist.")
        return None
    
    try:
        with open(filename, 'r') as file:
            calorie_data = json.load(file)
            print(f"Loaded calorie data from {filename}.")
            return calorie_data
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file {filename}: {e}")
        return None

def upload_calorie_data(calorie_data):
    if db is None:
        print("Firestore database not initialized.")
        return

    try:
        calorie_collection = db.collection("calorie_data")
        
        # Delete existing data
        docs = calorie_collection.stream()
        for doc in docs:
            calorie_collection.document(doc.id).delete()
        
        # Upload new data
        for item in calorie_data:
            fruit_name = item["name"].lower()
            calorie_collection.document(fruit_name).set(item)
            print(f"Uploaded calorie data for {fruit_name}")
        
        print("Calorie data initialization complete.")
    except Exception as e:
        print(f"Error uploading calorie data to Firebase: {e}")

# Load calorie data from calorie_data.json and upload it
calorie_data_file = "calorie_data.json"
calorie_data = load_calorie_data(calorie_data_file)

if calorie_data:
    upload_calorie_data(calorie_data)
