from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from io import BytesIO
import numpy as np
import json

try:
    model = load_model("data/fruit_classifier_model.h5")
    with open("data/label_dict.json", "r") as f:
        label_dict = json.load(f)
    with open("data/calorie_data.json", "r") as f:
        calorie_data = json.load(f)
    print("Model and data files loaded successfully.")
except Exception as e:
    print(f"Error loading model or data files: {e}")
    raise RuntimeError("Failed to load model or data files") from e

def preprocess_image(image):
    img = load_img(BytesIO(image.read()), target_size=(100, 100))
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_image(img):
    #Predict the fruit class of a given preprocessed image.
    prediction = model.predict(img)[0]
    predicted_class = np.argmax(prediction)
    confidence = prediction[predicted_class] * 100
    fruit_name = label_dict.get(str(predicted_class), "Unknown")
    return fruit_name, confidence

