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
    # Convert the FileStorage object to BytesIO
    img = load_img(BytesIO(image.read()), target_size=(100, 100))  # Resize to 100x100 as the model expects this input size
    img = img_to_array(img) / 255.0  # Normalize to [0, 1]
    img = np.expand_dims(img, axis=0)  # Add batch dimension
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
    </head>
    <body>
        <h1>Upload an Image to Identify the Fruit</h1>
        <form action="/predict" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*" required>
            <button type="submit">Upload and Predict</button>
        </form>
    </body>
    </html>
    ''')

# Prediction route with confidence score
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    img = preprocess_image(file)

    # Make a prediction
    prediction = model.predict(img)[0]  # Get the prediction probabilities for all classes
    predicted_class = np.argmax(prediction)  # Get the index of the highest probability
    confidence = prediction[predicted_class] * 100  # Convert to percentage
    
    # Map the predicted class index to the corresponding fruit name
    fruit_name = label_dict.get(str(predicted_class), "Unknown")
    
    return jsonify({"prediction": fruit_name, "confidence": f"{confidence:.2f}%"})

if __name__ == '__main__':
    app.run(debug=True, port=5002)