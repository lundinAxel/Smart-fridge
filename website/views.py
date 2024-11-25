from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import *
from .firebase import *
from . import db  
from datetime import datetime
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
#Test
views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'mp4'}

model = load_model('static/models/video_prediction_model.h5')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def trim_video(input_path, output_path, duration=10):
    command = [
        'ffmpeg', '-i', input_path, '-t', str(duration),
        '-c', 'copy', output_path
    ]
    subprocess.run(command)


def extract_frames(video_path, frame_count=10):
    video = cv2.VideoCapture(video_path)
    frames = []
    success, image = video.read()
    count = 0
    while success and count < frame_count:
        frames.append(image)
        success, image = video.read()
        count += 1
    video.release()
    return frames


# Root route redirects to login by default
@views.route('/')
def home():
    return redirect(url_for('views.login'))

@views.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        prediction_result = process_and_predict(filepath)
        return jsonify({'message': 'File uploaded successfully', 'prediction': prediction_result}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400

def process_and_predict(filepath):
    cap = cv2.VideoCapture(filepath)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (224, 224))  
        frames.append(frame)
    cap.release()
    frames = np.array(frames)

    prediction = model.predict(frames)
    return np.argmax(prediction, axis=-1).tolist()

# Route for the login page
@views.route('/login')
def login():
    return render_template("login.html")

# Route to handle login button click
from flask import request, jsonify, session

@views.route('/login', methods=['POST'])
def handle_login():
    # Get UID from the frontend request
    data = request.get_json()
    uid = data.get('uid')

    if not uid:
        return jsonify({"error": "User not logged in"}), 401

    # Store the UID in the session for later use
    session['user_id'] = uid

    return jsonify({"success": True, "message": "Login successful", "uid": uid})

    # Here you would implement your login validation logic
    # If login is successful, redirect to the base (home) page
    return redirect(url_for('views.base'))

# Route for the base page after login
@views.route('/base')
def base():
    return render_template("base.html")

# Route for the user registration page (first step)
@views.route('/userReg')
def user_registration():
    return render_template("userReg.html")

# Route for the create user page (second step after user registration)
@views.route('/createUser')
def create_user():
    return render_template("createUser.html")

@views.route('/modifyUser')
def modify_user():
    return render_template("modifyUser.html")

# Route to handle create user button click in userReg
@views.route('/createUser', methods=['POST'])
def handle_create_user():
    try:
        # Get the user ID from the session
        user_id = session.get('user_id')  # Fetch the user ID if logged in
        if not user_id:
            # If not logged in, generate a new user ID (for example, during new user registration)
            user_id = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Collect data from the form
        age = int(request.form.get('age'))
        height = int(request.form.get('height'))
        weight = float(request.form.get('weight'))
        gender = request.form.get('gender')
        goal = request.form.get('goal')
        activity = request.form.get('activity')

        # Validate inputs
        if not all([age, height, weight, gender, goal, activity]):
            return jsonify({"error": "All fields are required"}), 400

        # Calculate user goals
        from .calculateIndv import calculate_bmr, calculate_tdee, calculate_macros

        bmr = calculate_bmr(gender, age, height, weight)
        tdee = calculate_tdee(bmr, activity)
        calorie_goal, protein_g, fat_g, carbs_g = calculate_macros(goal, tdee, weight)

        # Prepare goals data
        goals_data = {
            "user_id": user_id,
            "gender": gender,
            "age": age,
            "height_cm": height,
            "weight_kg": weight,
            "activity_level": activity,
            "goal_type": goal,
            "bmr": round(bmr, 2),
            "tdee": round(tdee, 2),
            "calorie_goal": calorie_goal,
            "protein_g": protein_g,
            "fat_g": fat_g,
            "carbs_g": carbs_g
        }

        # Store user goals in Firebase using the store_user_goals function
        from .firebase import store_user_goals
        store_user_goals(user_id, goals_data)

        # Redirect to the base page or a success page
        return redirect(url_for('views.base'))

    except Exception as e:
        print(f"Error in handle_create_user: {e}")
        return jsonify({"error": "Failed to create user"}), 500




# Updated function in views.py
@views.route('/predict', methods=['POST'])
def predict():
    global calorie_goal, protein_goal, carbs_goal, fat_goal  # Declare global variables

    # Fetch the user ID from the session
    user_id = session.get('user_id')  # Ensure user_id is stored in the session during login
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    if 'file' not in request.files or 'weight' not in request.form:
        return jsonify({"error": "File or weight not provided"}), 400
    
    initialize_user_totals(user_id)

    file = request.files['file']
    new_weight = float(request.form['weight'])  # New weight in grams
    mime_type, _ = mimetypes.guess_type(file.filename)

    # Define paths for saving and processing files
    input_path = f'/tmp/{file.filename}'
    output_path = f'/tmp/trimmed_{file.filename}'

    # Save the uploaded file temporarily
    with open(input_path, 'wb+') as destination:
        for chunk in file.stream:
            destination.write(chunk)

    # Check if the uploaded file is a video or image
    if mime_type and mime_type.startswith('video'):
        # Trim video to 10 seconds
        try:
            trim_video(input_path, output_path, duration=10)
        except Exception as e:
            print(f"Error trimming video: {e}")
            return jsonify({"error": "Video processing failed"}), 500

        # Optional: Extract frames from the trimmed video
        frames = extract_frames(output_path, frame_count=10)

        # Use the first frame as a sample for prediction (adjust as needed)
        img = preprocess_image(frames[0])
    elif mime_type and mime_type.startswith('image'):
        # If the file is an image, proceed with the usual image preprocessing
        img = preprocess_image(file)
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    try:
        prediction = model.predict(img)[0]
        predicted_class = np.argmax(prediction)
        confidence = prediction[predicted_class] * 100
        fruit_name = label_dict.get(str(predicted_class), "Unknown")
    except Exception as e:
        print(f"Error in prediction process: {e}")
        return jsonify({"error": "Prediction failed"}), 500

    # Retrieve and update nutritional info for the predicted fruit
    nutrition_info = update_fruit_weight_in_db(user_id, fruit_name, new_weight)
    if not nutrition_info:
        return jsonify({"error": f"Nutritional data for {fruit_name} not available"}), 400

    # Fetch updated total nutrition values from Firestore
    try:
        user_doc_ref = db.collection("users").document(user_id).collection("goals").document("goal")
        print(user_id)
        user_doc = user_doc_ref.get()
        print(user_doc)
        if user_doc.exists:
            user_data = user_doc.to_dict()
        else:
            return jsonify({"error": f"No goals found for user {user_id}"}), 404

        # Get the goal values
        calorie_goal = user_data.get('calorie_goal', 2000)  # Default 2000
        carbs_goal = user_data.get('carbs_g', 200)          # Default 200
        protein_goal = user_data.get('protein_g', 150)      # Default 150
        fat_goal = user_data.get('fat_g', 50)               # Default 50
        print(calorie_goal)
    except Exception as e:
        print(f"Error fetching user data: {e}")
        #return jsonify({"error": "Failed to fetch user data"}), 500

    # Fetch today's totals
    try:
        today_date = datetime.now().strftime('%Y-%m-%d')
        totals_doc_ref = db.collection("users").document(user_id).collection("daily").document(today_date)
        totals_doc = totals_doc_ref.get()
        if totals_doc.exists:
            totals = totals_doc.to_dict()
        else:
            totals = {"total_calories": 0, "total_protein": 0, "total_carbohydrates": 0, "total_fat": 0}
    except Exception as e:
        print(f"Error fetching daily totals: {e}")
        totals = {"total_calories": 0, "total_protein": 0, "total_carbohydrates": 0, "total_fat": 0}

    # Safely fetch today's totals
    total_calories = totals.get("total_calories", 0)
    total_protein = totals.get("total_protein", 0)
    total_carbohydrates = totals.get("total_carbohydrates", 0)
    total_fat = totals.get("total_fat", 0)

    # Calculate percentages based on the fetched user goals
    calorie_percentage = (total_calories / calorie_goal) * 100
    protein_percentage = (total_protein / protein_goal) * 100
    carbs_percentage = (total_carbohydrates / carbs_goal) * 100
    fat_percentage = (total_fat / fat_goal) * 100

    # Render the prediction result in predict.html
    return render_template(
        "predict.html",
        total_calories=total_calories,
        total_protein=total_protein,
        total_carbohydrates=total_carbohydrates,
        total_fat=total_fat,
        calorie_percentage=calorie_percentage,
        protein_percentage=protein_percentage,
        carbs_percentage=carbs_percentage,
        fat_percentage=fat_percentage,
        calorie_goal=calorie_goal,
        protein_goal=protein_goal,
        carbs_goal=carbs_goal,
        fat_goal=fat_goal
    )


@views.route('/fetch_date', methods=['POST'])
def fetch_date():
    # Fetch the selected date from the request
    selected_date = request.form.get('selected_date')
    if not selected_date:
        return jsonify({"error": "No date selected"}), 400

    # Fetch the user ID from the session
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    try:
        # Path to the daily data in the updated database structure
        totals_doc_ref = db.collection("users").document(user_id).collection("daily").document(selected_date)
        doc = totals_doc_ref.get()

        if doc.exists:
            totals = doc.to_dict()
        else:
            # Default values if no data exists for the selected date
            totals = {"total_calories": 0, "total_protein": 0, "total_carbohydrates": 0, "total_fat": 0}

        # Fetch today's goal values from the user's goals in the database
        goals_doc_ref = db.collection("users").document(user_id).collection("goals").document("goal")
        goals_doc = goals_doc_ref.get()
        if goals_doc.exists:
            goals = goals_doc.to_dict()
            calorie_goal = goals.get("calorie_goal", 2000)
            protein_goal = goals.get("protein_g", 150)
            carbs_goal = goals.get("carbs_g", 200)
            fat_goal = goals.get("fat_g", 50)
        else:
            return jsonify({"error": "User goals not found"}), 404

        # Calculate percentages
        total_calories = totals.get("total_calories", 0)
        total_protein = totals.get("total_protein", 0)
        total_carbohydrates = totals.get("total_carbohydrates", 0)
        total_fat = totals.get("total_fat", 0)
        calorie_percentage = (total_calories / calorie_goal) * 100
        protein_percentage = (total_protein / protein_goal) * 100
        carbs_percentage = (total_carbohydrates / carbs_goal) * 100
        fat_percentage = (total_fat / fat_goal) * 100

        # Return the data as JSON
        return jsonify({
            "calorie_percentage": calorie_percentage,
            "protein_percentage": protein_percentage,
            "carbs_percentage": carbs_percentage,
            "fat_percentage": fat_percentage,
            "total_calories": total_calories,
            "total_protein": total_protein,
            "total_carbohydrates": total_carbohydrates,
            "total_fat": total_fat,
        })
    except Exception as e:
        print(f"Error fetching data for selected date: {e}")
        return jsonify({"error": "Failed to fetch data for the selected date"}), 500
    
@views.route('/updateUser', methods=['POST'])
def update_user():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "User not logged in"}), 401

        # Parse input data
        try:
            age = int(request.form.get('age'))
            height = int(request.form.get('height'))
            weight = float(request.form.get('weight'))
            goal = request.form.get('goal')
            activity = request.form.get('activity')
        except Exception as e:
            print(f"Error parsing input data: {e}")
            return jsonify({"error": "Invalid input data"}), 400

        # Fetch original data
        try:
            original_data = db.collection("users").document(user_id).collection("goals").document("goal").get().to_dict()
            if not original_data:
                return jsonify({"error": "Original user data not found"}), 404
        except Exception as e:
            print(f"Error fetching original data from Firestore: {e}")
            return jsonify({"error": "Failed to fetch original user data"}), 500

        # Calculate new goals
        try:
            from .calculateIndv import calculate_bmr, calculate_tdee, calculate_macros
            bmr = calculate_bmr(
                original_data["gender"],
                age or original_data["age"],
                height or original_data["height_cm"],
                weight or original_data["weight_kg"]
            )
            tdee = calculate_tdee(bmr, activity or original_data["activity_level"])
            calorie_goal, protein_g, fat_g, carbs_g = calculate_macros(
                goal or original_data["goal_type"],
                tdee,
                weight or original_data["weight_kg"]
            )

            new_goals_data = {
                "user_id": user_id,
                "gender": original_data["gender"],
                "age": age or original_data["age"],
                "height_cm": height or original_data["height_cm"],
                "weight_kg": weight or original_data["weight_kg"],
                "activity_level": activity or original_data["activity_level"],
                "goal_type": goal or original_data["goal_type"],
                "bmr": round(bmr, 2),
                "tdee": round(tdee, 2),
                "calorie_goal": calorie_goal,
                "protein_g": protein_g,
                "fat_g": fat_g,
                "carbs_g": carbs_g
            }
        except Exception as e:
            print(f"Error recalculating BMR, TDEE, or macros: {e}")
            return jsonify({"error": "Failed to recalculate user data"}), 500

        # Save both old and new goals
        try:
            from .firebase import store_user_goals
            store_user_goals(user_id, new_goals_data, original_data)
        except Exception as e:
            return jsonify({"error": "Failed to save updated user goals"}), 500

        return redirect(url_for('views.base'))

    except Exception as e:
        print(f"Unexpected error in update_user: {e}")
        return jsonify({"error": "Failed to update user"}), 500





