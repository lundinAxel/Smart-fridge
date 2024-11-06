from . import db  # Import the Firestore client from __init__.py

# Function to upload calorie data to Firestore
def upload_calorie_data(calorie_data):
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
        

def initialize_user_totals():
    try:
        user_doc_ref = db.collection("user").document("totals")
        user_doc_ref.set({
            "total_calories": 0,
            "total_protein": 0,
            "total_carbohydrates": 0,
            "total_fat": 0
        })
        print("Initialized user totals to zero.")
    except Exception as e:
        print(f"Error initializing user totals in Firebase: {e}")
    

def update_fruit_weight_in_db(fruit_name, new_weight):
        try:
            doc_ref = db.collection("calorie_data").document(fruit_name.lower())
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                old_weight = data.get("weight_in_fridge", 0)
                weight_diff = old_weight - new_weight
                
                # Calculate nutrition values for weight_diff per 100g
                calories = (data["calories_per_100g"] / 100) * weight_diff
                protein = (data["protein"] / 100) * weight_diff
                carbs = (data["carbohydrates"] / 100) * weight_diff
                fat = (data["fat"] / 100) * weight_diff

                # Calculate total nutrition based on new weight in fridge
                total_calories = (data["calories_per_100g"] / 100) * new_weight
                total_protein = (data["protein"] / 100) * new_weight
                total_carbs = (data["carbohydrates"] / 100) * new_weight
                total_fat = (data["fat"] / 100) * new_weight

                # Update the weight in the fridge
                doc_ref.update({"weight_in_fridge": new_weight})

                # Update user totals
                update_user_totals(calories, protein, carbs, fat)

                print(f"Updated {fruit_name} in fridge from {old_weight}g to {new_weight}g.")
                return {
                    "old_weight": old_weight,
                    "new_weight": new_weight,
                    "calories": calories,
                    "protein": protein,
                    "carbohydrates": carbs,
                    "fat": fat,
                    "total_calories": total_calories,
                    "total_protein": total_protein,
                    "total_carbohydrates": total_carbs,
                    "total_fat": total_fat
                }
            else:
                print(f"Fruit {fruit_name} not found in database.")
                return None
        except Exception as e:
            print(f"Error updating fruit weight in Firebase: {e}")
            return None

# Function to update user totals
def update_user_totals(calories, protein, carbs, fat):
    try:
        user_doc_ref = db.collection("user").document("totals")
        doc = user_doc_ref.get()
        if doc.exists:
            current_totals = doc.to_dict()
            new_totals = {
                "total_calories": current_totals["total_calories"] + calories,
                "total_protein": current_totals["total_protein"] + protein,
                "total_carbohydrates": current_totals["total_carbohydrates"] + carbs,
                "total_fat": current_totals["total_fat"] + fat
            }
            user_doc_ref.set(new_totals)
        else:
            # Initialize if missing
            user_doc_ref.set({
                "total_calories": calories,
                "total_protein": protein,
                "total_carbohydrates": carbs,
                "total_fat": fat
            })
    except Exception as e:
        print(f"Error updating user totals in Firebase: {e}")

        