from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import *
from website.firebase import *
from . import db  
import mimetypes
import subprocess
import os
import cv2  
from firebase import upload_to_firebase 

views = Blueprint('views', __name__)

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

# Route for the login page
@views.route('/login')
def login():
    return render_template("login.html")

# Route to handle login button click
@views.route('/login', methods=['POST'])
def handle_login():
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

# Route to handle create user button click in userReg
@views.route('/createUser', methods=['POST'])
def handle_create_user():
    # Logic to handle the creation of a new user
    # Redirect to the base page after creating the user
    return redirect(url_for('views.base'))

# Predict route
@views.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files or 'weight' not in request.form:
        return jsonify({"error": "File or weight not provided"}), 400

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
    nutrition_info = update_fruit_weight_in_db(fruit_name, new_weight)
    if not nutrition_info:
        return jsonify({"error": f"Nutritional data for {fruit_name} not available"}), 400

    # Fetch updated total nutrition values from Firestore
    try:
        user_doc_ref = db.collection("user").document("totals")
        doc = user_doc_ref.get()
        if doc.exists:
            totals = doc.to_dict()
        else:
            totals = {"total_calories": 0, "total_protein": 0, "total_carbohydrates": 0, "total_fat": 0}
    except Exception as e:
        print(f"Error fetching user totals from Firebase: {e}")
        totals = {"total_calories": 0, "total_protein": 0, "total_carbohydrates": 0, "total_fat": 0}

    # Calculate total percentages
    calorie_percentage = (totals['total_calories'] / 2000) * 100
    protein_percentage = (totals['total_protein'] / 150) * 100
    carbs_percentage = (totals['total_carbohydrates'] / 200) * 100
    fat_percentage = (totals['total_fat'] / 50) * 100

    # Render the prediction result in predict.html with updated totals and percentages
    return render_template(
        "predict.html",
        fruit_name=fruit_name,
        confidence=f"{confidence:.2f}",
        old_weight=nutrition_info["old_weight"],
        new_weight=new_weight,
        weight_diff=new_weight - nutrition_info["old_weight"],
        total_calories=totals['total_calories'],
        total_protein=totals['total_protein'],
        total_carbohydrates=totals['total_carbohydrates'],
        total_fat=totals['total_fat'],
        calorie_percentage=calorie_percentage,
        protein_percentage=protein_percentage,
        carbs_percentage=carbs_percentage,
        fat_percentage=fat_percentage
    )
