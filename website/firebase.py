from datetime import datetime, timedelta
from . import db  # Import the Firestore client from __init__.py

# Function to upload calorie data to Firestore

def initialize_user_totals():
    try:
        today_date = datetime.now().strftime('%Y-%m-%d')
        totals_doc_ref = db.collection("user").document(today_date)
        totals_doc_ref.set({
            "total_calories": 0
        })
        print("Initialized user totals to zero for today's date.")
    except Exception as e:
        print(f"Error initializing user totals in Firebase: {e}")


from datetime import datetime

def update_fruit_weight_in_db(fruit_name, new_weight):
    try:
        # Get today's date in YYYY-MM-DD format
        today_date = datetime.now().strftime('%Y-%m-%d')

        # Get the document reference for today's date
        totals_doc_ref = db.collection("user").document(today_date)
        fruit_doc_ref = db.collection("calorie_data").document(fruit_name.lower())

        # Fetch fruit data
        fruit_doc = fruit_doc_ref.get()
        if not fruit_doc.exists:
            print(f"Fruit {fruit_name} not found in database.")
            return None

        fruit_data = fruit_doc.to_dict()
        old_weight = fruit_data.get("weight_in_fridge", 0)
        weight_diff = old_weight -new_weight   # Positive if weight is added, negative if removed

        # Calculate nutrition values for weight_diff per 100g
        calories = (fruit_data["calories_per_100g"] / 100) * weight_diff
        protein = (fruit_data["protein"] / 100) * weight_diff
        carbs = (fruit_data["carbohydrates"] / 100) * weight_diff
        fat = (fruit_data["fat"] / 100) * weight_diff

        # Update the fruit weight in the fridge
        fruit_doc_ref.update({"weight_in_fridge": new_weight})

        # Update totals in Firestore
        totals_doc = totals_doc_ref.get()
        if totals_doc.exists:
            totals = totals_doc.to_dict()
            totals_doc_ref.update({
                "total_calories": totals.get("total_calories", 0) + calories,
                "total_protein": totals.get("total_protein", 0) + protein,
                "total_carbohydrates": totals.get("total_carbohydrates", 0) + carbs,
                "total_fat": totals.get("total_fat", 0) + fat
            })
        else:
            # If the totals document doesn't exist, create it with initial values
            totals_doc_ref.set({
                "total_calories": calories,
                "total_protein": protein,
                "total_carbohydrates": carbs,
                "total_fat": fat
            })

        print(f"Updated totals for {today_date}: Calories: {calories}, Protein: {protein}, Carbs: {carbs}, Fat: {fat}")
        return {
            "old_weight": old_weight,
            "new_weight": new_weight,
            "calories": calories,
            "protein": protein,
            "carbohydrates": carbs,
            "fat": fat
        }

    except Exception as e:
        print(f"Error updating fruit weight in Firebase: {e}")
        return None


# Function to update daily totals

def update_daily_totals(calories):
    try:
        # Get today's date in YYYY-MM-DD format
        today_date = datetime.now().strftime('%Y-%m-%d')

        # Reference the document with today's date
        totals_doc_ref = db.collection("user").document(today_date)

        # Fetch existing data for today or initialize
        doc = totals_doc_ref.get()
        if doc.exists():
            current_totals = doc.to_dict()
            new_total_calories = current_totals.get("total_calories", 0) + calories
            totals_doc_ref.update({"total_calories": new_total_calories})
            print(f"Updated total calories for {today_date} to {new_total_calories}.")
        else:
            # Create a new document for today if it doesn't exist
            totals_doc_ref.set({"total_calories": calories})
            print(f"Created new entry for {today_date} with total calories {calories}.")

    except Exception as e:
        print(f"Error updating daily totals in Firebase: {e}")

# Function to fetch daily totals by date
def fetch_daily_totals(date):
    try:
        totals_doc_ref = db.collection("user").document(date)
        doc = totals_doc_ref.get()
        if doc.exists():
            return doc.to_dict()
        else:
            print(f"No data found for date: {date}")
            return None
    except Exception as e:
        print(f"Error fetching daily totals from Firebase: {e}")
        return None


def fetch_daily_totals(date):
    try:
        totals_doc_ref = db.collection("user").document(date)
        doc = totals_doc_ref.get()
        if doc.exists():
            return doc.to_dict()
        else:
            print(f"No data found for date: {date}")
            return {"total_calories": 0, "total_protein": 0, "total_carbohydrates": 0, "total_fat": 0}
    except Exception as e:
        print(f"Error fetching daily totals from Firebase: {e}")
        return {"error": "Error fetching data"}

def store_user_goals(user_id, goals_data):
    try:
        user_ref = db.collection("user").document(user_id)
        user_ref.set(goals_data)
        print(f"User goals for {user_id} saved successfully!")
    except Exception as e:
        print(f"Error saving user goals in Firebase: {e}")