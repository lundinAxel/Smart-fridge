from math import ceil

# Define constants for activity multipliers and macronutrient ratios
ACTIVITY_MULTIPLIERS = {
    "none": 1.2,
    "1-2 times/week": 1.375,
    "3-4 times/week": 1.55,
    "4-7 times/week": 1.725
}

MACRO_RATIOS = {
    "deficit": {"protein": 1.5, "fat_percentage": 0.25},
    "maintenance": {"protein": 1.2, "fat_percentage": 0.25},
    "bulk": {"protein": 1.6, "fat_percentage": 0.20}
}

# Calculate BMR based on gender, age, height, weight
def calculate_bmr(gender, age, height_cm, weight_kg):
    if gender == "male":
        return 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:  # female
        return 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)

# Calculate TDEE based on BMR and activity level
def calculate_tdee(bmr, activity_level):
    return bmr * ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)

# Calculate calorie and macronutrient goals based on goal type
def calculate_macros(goal_type, tdee, weight_kg):
    # Adjust TDEE based on the goal type
    if goal_type == "deficit":
        calorie_goal = tdee - 500  # 500 kcal less for fat loss
    elif goal_type == "bulk":
        calorie_goal = tdee + 500  # 500 kcal more for muscle gain
    else:  # maintenance
        calorie_goal = tdee

    # Calculate macronutrients
    protein_g = MACRO_RATIOS[goal_type]["protein"] * weight_kg
    fat_g = (MACRO_RATIOS[goal_type]["fat_percentage"] * calorie_goal) / 9
    carbs_g = (calorie_goal - (protein_g * 4 + fat_g * 9)) / 4

    return ceil(calorie_goal), ceil(protein_g), ceil(fat_g), ceil(carbs_g)


# Store user information and calculated data in the database
def store_user_data(db, user_data):
    user_ref = db.collection("users").document(user_data["user_id"])
    user_ref.set(user_data)

def main(db):
    # Collect user information
    gender = input("Enter gender (male/female): ")
    age = int(input("Enter age: "))
    height_cm = int(input("Enter height in cm: "))
    weight_kg = float(input("Enter current weight in kg: "))
    activity_level = input("Enter activity level (none, 1-2 times/week, 3-4 times/week, 4-7 times/week): ")
    goal_type = input("Enter goal type (deficit, maintenance, bulk): ")

    # Calculate BMR, TDEE, and macronutrient needs
    bmr = calculate_bmr(gender, age, height_cm, weight_kg)
    tdee = calculate_tdee(bmr, activity_level)
    calorie_goal, protein_g, fat_g, carbs_g = calculate_macros(goal_type, tdee, weight_kg)

    # Prepare user data dictionary
    user_data = {
        "gender": gender,
        "age": age,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "activity_level": activity_level,
        "goal_type": goal_type,
        "bmr": bmr,
        "tdee": tdee,
        "calorie_goal": calorie_goal,
        "protein_g": protein_g,
        "fat_g": fat_g,
        "carbs_g": carbs_g
    }

    # Save user data to database
    store_user_data(db, user_data)

    print("User data saved successfully!")

# Sample database integration
# For Firebase Firestore
# from firebase_admin import firestore
# db = firestore.client()
# main(db)
