from flask import Flask, request, jsonify, render_template_string
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import json
from io import BytesIO

# Initialize the Flask app
app = Flask(__name__)

# Load the model and label dictionary
model = load_model("fruit_classifier_model.h5")
with open("label_dict.json", "r") as f:
    label_dict = json.load(f)

# Function to preprocess the input image
def preprocess_image(image):
    img = load_img(BytesIO(image.read()), target_size=(100, 100))
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Route to serve the upload form
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fruit Recognition</title>
        <style>
            body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f8f9fa; }
            .container { text-align: center; padding: 20px; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); background-color: #fff; width: 300px; }
            h1 { color: #343a40; }
            form { margin-top: 20px; }
            button { padding: 10px 20px; background-color: #007bff; color: #fff; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Fruit Recognition</h1>
            <p>Upload an image to identify the fruit.</p>
            <form action="/predict" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*" required>
                <br><br>
                <button type="submit">Upload and Predict</button>
            </form>
        </div>
    </body>
    </html>
    ''')    

# Prediction route with confidence score and a "Back" button
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    img = preprocess_image(file)

    # Make a prediction
    prediction = model.predict(img)[0]
    predicted_class = np.argmax(prediction)
    confidence = prediction[predicted_class] * 100
    
    # Map the predicted class index to the corresponding fruit name
    fruit_name = label_dict.get(str(predicted_class), "Unknown")
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Prediction Result</title>
        <style>
            body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f8f9fa; }
            .container { text-align: center; padding: 20px; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); background-color: #fff; width: 300px; }
            h2 { color: #343a40; }
            p { font-size: 1.1em; }
            .back-button { margin-top: 20px; padding: 10px 20px; background-color: #007bff; color: #fff; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; }
            .back-button:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Prediction Result</h2>
            <p><strong>Fruit:</strong> {{ fruit_name }}</p>
            <p><strong>Confidence:</strong> {{ confidence }}%</p>
            <a href="/" class="back-button">Try Another Image</a>
        </div>
    </body>
    </html>
    ''', fruit_name=fruit_name, confidence=f"{confidence:.2f}")

if __name__ == '__main__':
    app.run(debug=True, port=5003)
