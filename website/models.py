from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from io import BytesIO
import numpy as np
import json
import cv2 

try:
    model = load_model("Data/fruit_classifier_model.h5")
    with open("Data/label_dict.json", "r") as f:
        label_dict = json.load(f)
    with open("Data/calorie_data.json", "r") as f:
        calorie_data = json.load(f)
    print("Model and data files loaded successfully.")
except Exception as e:
    print(f"Error loading model or data files: {e}")
    raise RuntimeError("Failed to load model or data files") from e

def preprocess_image(image):
    if isinstance(image, np.ndarray):
        # Handle numpy array (video frame)
        img = cv2.resize(image, (100, 100))  # Resize frame to target size
        img = img / 255.0  # Normalize pixel values
        img = np.expand_dims(img, axis=0)  # Add batch dimension
    else:
        # Handle file-like object (uploaded image)
        img = load_img(BytesIO(image.read()), target_size=(100, 100))  # Resize to target size
        img = img_to_array(img) / 255.0  # Normalize pixel values
        img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

def predict_image(img):
    #Predict the fruit class of a given preprocessed image.
    prediction = model.predict(img)[0]
    predicted_class = np.argmax(prediction)
    confidence = prediction[predicted_class] * 100
    fruit_name = label_dict.get(str(predicted_class), "Unknown")
    print(f"\nBest prediction: {fruit_name} with confidence: {confidence:.2f}%")
    return fruit_name, confidence

