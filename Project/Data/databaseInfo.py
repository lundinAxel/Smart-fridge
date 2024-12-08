import json

# Define each fruit/vegetable with placeholder values (replace with actual values later)
data = [
    {
        "name": "Avocado 1",
        "calories_per_100g": 160,
        "carbohydrates": 9,
        "protein": 2,
        "fat": 15,
        "weight_in_fridge": 1842
    },
    {
        "name": "Avocado ripe 1",
        "calories_per_100g": 160,
        "carbohydrates": 9,
        "protein": 2,
        "fat": 15,
        "weight_in_fridge": 2391
    },
    {
        "name": "Banana 1",
        "calories_per_100g": 96,
        "carbohydrates": 27,
        "protein": 1.3,
        "fat": 0.3,
        "weight_in_fridge": 2131
    },
    {
        "name": "Banana Lady Finger 1",
        "calories_per_100g": 90,
        "carbohydrates": 23,
        "protein": 1.1,
        "fat": 0.3,
        "weight_in_fridge": 1249
    },
    {
        "name": "Onion Red 1",
        "calories_per_100g": 40,
        "carbohydrates": 9,
        "protein": 1.1,
        "fat": 0.1,
        "weight_in_fridge": 1239
    },
    {
        "name": "Onion Red Peeled 1",
        "calories_per_100g": 40,
        "carbohydrates": 9,
        "protein": 1.1,
        "fat": 0.1,
        "weight_in_fridge": 1293
    },
    {
        "name": "Potato Red 1",
        "calories_per_100g": 77,
        "carbohydrates": 17,
        "protein": 2,
        "fat": 0.1,
        "weight_in_fridge": 2301
    },
    {
        "name": "Potato Red Washed 1",
        "calories_per_100g": 77,
        "carbohydrates": 17,
        "protein": 2,
        "fat": 0.1,
        "weight_in_fridge": 1231
    },
    {
        "name": "Potato Sweet 1",
        "calories_per_100g": 86,
        "carbohydrates": 20,
        "protein": 1.6,
        "fat": 0.1,
        "weight_in_fridge": 1241
    },
    {
        "name": "Potato White 1",
        "calories_per_100g": 77,
        "carbohydrates": 17,
        "protein": 2,
        "fat": 0.1,
        "weight_in_fridge": 4532
    }
]

# Write data to a JSON file
with open("calorie_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("Calorie data has been written to 'calorie_data.json'")
