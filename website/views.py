# type: ignore
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import *
from .firebase import *
from . import db  # Import the Firestore client
from datetime import datetime
import os 
import mimetypes
import subprocess
import numpy as np 
import cv2  
import time

views = Blueprint('views', __name__)

calorie_goal = 2000  # Default values
protein_goal = 150
carbs_goal = 200
fat_goal = 50

def extract_frames(video_path, interval=1, output_dir="output_frames"):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    video = cv2.VideoCapture(video_path)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    print(f"Frames per second: {fps}")
    frames = []
    
    count = 0
    frame_count = 0

    while True:
        success, frame = video.read()
        if not success:
            break
        if count % int(fps * interval) == 0:
            # Save the frame as an image
            frames.append(frame)
            frame_filename = os.path.join(output_dir, f"{frame_count}.jpg")
            cv2.imwrite(frame_filename, frame)
            frame_count += 1
        count += 1

    video.release()
    return frames  # Return the number of saved frames



# Root route redirects to login by default
@views.route('/')
def home():
    return redirect(url_for('views.login'))

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
from .calculateIndv import calculate_bmr, calculate_tdee, calculate_macros  # Import calculation functions

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

@views.route('/predict', methods=['GET', 'POST'])
def predict():
    global calorie_goal, protein_goal, carbs_goal, fat_goal

    # Fetch the user ID from the session
    user_id = session.get('user_id')  # Ensure user_id is stored in the session during login
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    # Handle GET requests for opening the page with today's data
    if request.method == 'GET':
        # Fetch today's date
        today_date = datetime.now().strftime('%Y-%m-%d')

        # Fetch today's totals
        try:
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

        # Render the prediction result page
        return render_template(
            "predict.html",
            total_calories=total_calories,
            total_protein=total_protein,
            total_carbohydrates=total_carbohydrates,
            total_fat=total_fat,
            calorie_goal=calorie_goal,
            protein_goal=protein_goal,
            carbs_goal=carbs_goal,
            fat_goal=fat_goal,
            fruit_name=None,
            confidence=None
        )

    # Existing POST logic for predictions
    if request.method == 'POST':
        if 'file' not in request.files or 'weight' not in request.form:
            return jsonify({"error": "File or weight not provided"}), 400

    file = request.files['file']
    new_weight = float(request.form['weight'])  # New weight in grams
    mime_type = file.content_type

    if mime_type.startswith('image'):
        # Handle image file
        try:
            img = preprocess_image(file)
            prediction = model.predict(img)[0]
            predicted_class = np.argmax(prediction)
            confidence = prediction[predicted_class] * 100
            fruit_name = label_dict.get(str(predicted_class), "Unknown")
            print(f"\nBest prediction: {fruit_name} with confidence: {confidence:.2f}%")
        except Exception as e:
            print(f"Error in image prediction process: {e}")
            return jsonify({"error": "Prediction failed"}), 500

    elif mime_type.startswith('video'):
        # Handle video file
        try:
            # Save the uploaded video
            video_path = os.path.join("uploads", file.filename)
            os.makedirs(os.path.dirname(video_path), exist_ok=True)
            file.save(video_path)
            print(f"Video saved at: {video_path}")

            # Extract frames at 0.5-second intervals
            frames = extract_frames(video_path, interval=0.5)
            frame_predictions = []  # To store predictions for each frame

            # Save and reload frames to ensure consistency
            processed_frames = []
            for i, frame in enumerate(frames):
                # Save frame to disk
                frame_path = os.path.join("output_frames", f"frame_{i}.jpg")
                os.makedirs("output_frames", exist_ok=True)
                cv2.imwrite(frame_path, frame)  # Save in RGB format

                # Reload saved frame and preprocess it
                reloaded_frame = load_img(frame_path, target_size=(100, 100))
                preprocessed_frame = img_to_array(reloaded_frame) / 255.0
                preprocessed_frame = np.expand_dims(preprocessed_frame, axis=0)  # Add batch dimension
                processed_frames.append(preprocessed_frame)

                # Predict on the preprocessed frame
                prediction = model.predict(preprocessed_frame)[0]
                predicted_class = np.argmax(prediction)
                confidence = max(prediction) * 100
                fruit_name = label_dict.get(str(predicted_class), "Unknown")
                frame_predictions.append((fruit_name, confidence))

                print(f"Frame {i}: Predicted {fruit_name} with confidence {confidence:.2f}%")

            # Combine predictions into a single batch
            batch = np.vstack(processed_frames)
            predictions = model.predict(batch)

            # Find the best prediction across all frames
            best_idx = np.argmax(predictions, axis=1)
            best_confidences = np.max(predictions, axis=1)
            best_frame_idx = np.argmax(best_confidences)
            best_class = best_idx[best_frame_idx]
            best_confidence = best_confidences[best_frame_idx]

            # Map the best class to a label
            fruit_name = label_dict.get(str(best_class), "Unknown")
            confidence = best_confidence * 100

            # Print final best prediction
            print(f"\nBest prediction: {fruit_name} with confidence: {confidence:.2f}%")

            # Print all frame predictions for debugging
            print("\nAll frame predictions:")
            for i, (fruit, conf) in enumerate(frame_predictions):
                print(f"Frame {i}: Predicted {fruit} with confidence {conf:.2f}%")

        except Exception as e:
            print(f"Error in video prediction process: {e}")
            return jsonify({"error": "Video processing failed"}), 500

    else:
        return jsonify({"error": "Unsupported file type"}), 400

    # Retrieve and update nutritional info for the predicted fruit
    try:
        nutrition_info = update_fruit_weight_in_db(user_id, fruit_name, new_weight)
        if not nutrition_info:
            return jsonify({"error": f"Nutritional data for {fruit_name} not available"}), 400
    except Exception as e:
        print(f"Error updating nutrition info: {e}")
        return jsonify({"error": "Failed to update nutritional info"}), 500

    # Fetch the user's goals from Firebase
    try:
        user_doc_ref = db.collection("users").document(user_id).collection("goals").document("goal")
        user_doc = user_doc_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            calorie_goal = user_data.get('calorie_goal', 2000)
            carbs_goal = user_data.get('carbs_g', 200)
            protein_goal = user_data.get('protein_g', 150)
            fat_goal = user_data.get('fat_g', 50)
        else:
            return jsonify({"error": f"No goals found for user {user_id}"}), 404
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return jsonify({"error": "Failed to fetch user data"}), 500

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
        fat_goal=fat_goal,
        fruit_name=fruit_name,
        confidence=confidence
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

@views.route('/fetch_weekly_calories', methods=['GET'])
def fetch_weekly_calories():
    try:
        # Get the user's UID from the session
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "User not logged in"}), 401

        # Define the date range for the last 7 days
        today = datetime.now()
        dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

        # Fetch calorie data for the last 7 days
        weekly_data = []
        for date in dates:
            daily_data = fetch_daily_totals(user_id, date)
            if daily_data and not daily_data.get("error"):
                weekly_data.append({"date": date, "total_calories": daily_data["total_calories"]})
            else:
                weekly_data.append({"date": date, "total_calories": 0})  # Default to 0 if no data

        # Fetch user calorie goal
        user_doc_ref = db.collection("users").document(user_id).collection("goals").document("goal")
        user_doc = user_doc_ref.get()
        calorie_goal = user_doc.to_dict().get('calorie_goal', 2000) if user_doc.exists else 2000
        
        # Return data including calorie goal
        return jsonify({
            "success": True,
            "data": weekly_data,  # Existing weekly data
            "calorie_goal": calorie_goal  # Add calorie goal
        })
    except Exception as e:
        print(f"Error fetching weekly calories: {e}")
        return jsonify({"error": "Failed to fetch weekly data"}), 500




