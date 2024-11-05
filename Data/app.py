from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import json

# Load the model and label dictionary
model = load_model("fruit_classifier_model.h5")
with open("label_dict.json", "r") as f:
    label_dict = json.load(f)

# Function to preprocess the input image
def preprocess_image(image_path):
    img = load_img(image_path, target_size=(100, 100))  # Resize to 100x100 as required by the model
    img = img_to_array(img) / 255.0  # Normalize to [0, 1]
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Iterate over images with names testfruit1.png to testfruit8.png
for i in range(1, 10):
    image_path = f"testfruit{i}.png"  # Construct the filename
    img = preprocess_image(image_path)
    
    prediction = model.predict(img)[0]  # Get prediction probabilities for all classes
    predicted_class = np.argmax(prediction)  # Get the index of the highest probability
    confidence = prediction[predicted_class] * 100  # Convert to percentage
    
    # Map the predicted class index to the corresponding fruit name
    fruit_name = label_dict.get(str(predicted_class), "Unknown")
    
    print(f"Image: testfruit{i}.png | Predicted Fruit: {fruit_name} | Confidence: {confidence:.2f}%")
