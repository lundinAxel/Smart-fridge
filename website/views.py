from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import *
from .firebase import *
from . import db  # Import the Firestore client
from datetime import datetime

views = Blueprint('views', __name__)

calorie_goal = 2000  # Default values
protein_goal = 150
carbs_goal = 200
fat_goal = 50

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
from .calculateIndv import calculate_bmr, calculate_tdee, calculate_macros  # Import calculation functions

@views.route('/createUser', methods=['POST'])
def handle_create_user():
    try:
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
        user_id = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}"  # Unique user ID
        goals_data = {
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

        # Save to Firebase
        from .firebase import store_user_goals
        store_user_goals(user_id, goals_data)

        # Redirect to the base page or success page
        return redirect(url_for('views.base'))

    except Exception as e:
        print(f"Error in handle_create_user: {e}")
        return jsonify({"error": "Failed to create user"}), 500




# Updated function in views.py
@views.route('/predict', methods=['POST'])
def predict():
    global calorie_goal, protein_goal, carbs_goal, fat_goal  # Declare global variables

    # Fetch the user's goals from Firebase
    try:
        user_doc_ref = db.collection("user").document("AleksanderJ")
        user_doc = user_doc_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
        else:
            return jsonify({"error": f"No data found for user {"AleksanderJ"}"}), 404

        # Get the goal values
        calorie_goal = user_data.get('calorie_goal', 2000)  # Default 2000
        carbs_goal = user_data.get('carbs_g', 200)          # Default 200
        protein_goal = user_data.get('protein_g', 150)      # Default 150
        fat_goal = user_data.get('fat_g', 50)               # Default 50
        print(calorie_goal) 
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return jsonify({"error": "Failed to fetch user data"}), 500

    # Fetch today's totals
    try:
        today_date = datetime.now().strftime('%Y-%m-%d')
        totals_doc_ref = db.collection("user").document(today_date)
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
    selected_date = request.form.get('selected_date')
    if not selected_date:
        return jsonify({"error": "No date selected"}), 400

    try:
        # Fetch data for the selected date
        totals_doc_ref = db.collection("user").document(selected_date)
        doc = totals_doc_ref.get()
        if doc.exists:
            totals = doc.to_dict()
        else:
            totals = {"total_calories": 0, "total_protein": 0, "total_carbohydrates": 0, "total_fat": 0}

        # Calculate percentages
        total_calories = totals.get("total_calories", 0)
        total_protein = totals.get("total_protein", 0)
        total_carbohydrates = totals.get("total_carbohydrates", 0)
        total_fat = totals.get("total_fat", 0)
        calorie_percentage = (totals.get("total_calories", 0) / calorie_goal) * 100
        protein_percentage = (totals.get("total_protein", 0) / protein_goal) * 100
        carbs_percentage = (totals.get("total_carbohydrates", 0) / carbs_goal) * 100
        fat_percentage = (totals.get("total_fat", 0) / fat_goal) * 100

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
