#Anything the user can navigate to, except authentication
from flask import Blueprint, render_template, request, jsonify
from .models import preprocess_image, predict_image

views = Blueprint('views', __name__)

#defines route for the home page
@views.route('/') 
def home():
    return render_template("base.html")

@views.route('/test') 
def test_page():
    return render_template("predict.html")

@views.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    img = preprocess_image(file)

    # Make a prediction
    fruit_name, confidence = predict_image(img)

    # Return the result as JSON
    return render_template("predict.html", fruit=fruit_name, confidence=confidence)