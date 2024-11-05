#Anything the user can navigate to, except authentication
from flask import Blueprint, render_template, request, jsonify
from .models import *
from .firebase import *

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
    if 'file' not in request.files or 'weight' not in request.form:
        return jsonify({"error": "File or weight not provided"}), 400

    file = request.files['file']
    new_weight = float(request.form['weight'])  # New weight in grams
    img = preprocess_image(file)

    # Make a prediction
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

    # Render the prediction result in predict.html
    return render_template(
        "predict.html",
        fruit_name=fruit_name,
        confidence=f"{confidence:.2f}",
        old_weight=nutrition_info["old_weight"],
        new_weight=new_weight,
        weight_diff=new_weight - nutrition_info["old_weight"],
        calories=f"{nutrition_info['calories']:.2f}",
        protein=f"{nutrition_info['protein']:.2f}",
        carbs=f"{nutrition_info['carbohydrates']:.2f}",
        fat=f"{nutrition_info['fat']:.2f}",
        total_calories=f"{nutrition_info['total_calories']:.2f}",
        total_protein=f"{nutrition_info['total_protein']:.2f}",
        total_carbohydrates=f"{nutrition_info['total_carbohydrates']:.2f}",
        total_fat=f"{nutrition_info['total_fat']:.2f}"
    )
