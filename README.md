# FreshLife
## Collaborators

| Name                | Organization                          | Department                                 | Email                           |
|---------------------|--------------------------------------|-------------------------------------------|---------------------------------|
| **Aleksander Jankovic**   | Högskolan i Halmstad |         Computer Engineering              | [alejan22@student.hh.se](mailto:alejan22@student.hh.se) |
| **Axel Lundin**      | Högskolan i Halmstad | Computer Engineering | [axelun22@student.hh.se](mailto:axelun22@student.hh.se) |
| **Hyunsuk Lee**     | Hanyang University                   | tbh                      | [tbh] |
| **Mohammed Ismaili**      | Hanyang University             | tbh                      | [tbh] |

## About the App

The app integrates with a smart refrigerator connected via Wi-Fi and synced with a fitness app. Equipped with cameras and an internal scale, the fridge helps users automatically track the nutritional values of the food they consume throughout the day. By leveraging real-time data from both the food recognition system and weight measurements, the app provides an accurate calculation of daily nutritional intake.

### Features
- **Real-time Food Tracking**: Automatically detect and record nutritional values using internal cameras and weight sensors.
- **Personalized Guidance**: Tailored dietary recommendations to help achieve specific goals:
  - Addressing nutritional deficiencies.
  - Bulking to build muscle.
  - Losing weight.
- **Progress Tracking**: Detailed charts displaying daily calorie consumption and trends for better decision-making and goal adjustments.

---

This app is designed to help users make informed dietary choices and achieve their fitness goals with ease.

**Datasets**

The application relies on multiple datasets to ensure accurate food recognition and nutritional analysis:

***Image Classification Dataset:***

The core of the application’s food recognition feature relies on a labeled dataset of fruit and vegetable images, originally sourced from the Kaggle Fruits 360 Dataset. This dataset was carefully curated and modified to meet the specific requirements of our project.

**Custom Dataset Preparation**
**Original Dataset:** 
- The Kaggle dataset includes a wide variety of fruits and vegetables, providing a robust foundation for image classification tasks.
**Modifications:**
- Unnecessary classes were removed to create a smaller, more focused dataset tailored to our use case. This reduction minimized noise and ensured that the training set aligned with the types of fruits likely to be encountered in real-world refrigerator environments.
- Data augmentation techniques (e.g., rotation, scaling, flipping, and shifting) were applied to increase the diversity of training images without the need for additional data collection. This improved the model's robustness to variations in lighting, orientation, and scale.
- **Training Process**
  - The dataset was used to train a custom Convolutional Neural Network (CNN) built with TensorFlow and Keras:

  - The model architecture includes dropout layers to prevent overfitting, achieving a balance between complexity and generalizability.
  Training involved 40 epochs, leveraging data augmentation to improve accuracy and adaptability.
  The final model achieved a test accuracy of 97%, demonstrating its reliability for real-world applications.
  Rationale for Custom Dataset
  - Alignment with Testing Environment: The smaller, curated dataset ensures the model is highly optimized for the specific fruits and vegetables likely to be tracked in a 
  smart refrigerator.
  - Improved Accuracy: By focusing on a limited but relevant set of classes, the model performs exceptionally well, with minimal misclassification errors.
  - Enhanced Practicality: The model's ability to handle images and videos aligns with the app's functionality to process camera data from a refrigerator and determine 
  which items are added or removed. This is paired with internal scales to calculate the nutritional impact of consumption, providing users with accurate calorie tracking.
  This combination of a streamlined dataset and tailored training approach ensures the model is both efficient and effective, perfectly suited for the app's requirements.

***Nutritional Information Dataset:***

The **Nutritional Information Dataset** forms a critical part of the app's functionality, providing the caloric and macronutrient details necessary for accurate consumption tracking. Here's how it is structured and utilized:

**Dataset Structure:**

- The dataset contains nutritional values (calories, protein, fats, and carbohydrates per 100g) for various food items.
- Stored in JSON format (calorie_data.json), it acts as a backup to prevent data loss in case of errors within the Firebase database.
- Each food item is labeled consistently with the fruit classification model to ensure seamless integration. For example, different types of bananas are grouped under the same label, allowing the app to easily fetch the correct nutritional data.
**Integration:**

- The dataset is synced with Firebase Firestore to enable real-time data access. When the app's fruit recognition model identifies an item, it queries the database for its corresponding nutritional information.
- This integration ensures that the app can calculate the calories and macronutrients consumed based on the fruit detected and its recorded weight changes from the internal refrigerator scale.
**Why This Approach?:**

- Accuracy: By using a structured and verified dataset (derived from sources like USDA and user-provided entries), the app ensures that the nutritional information is both reliable and precise.
- Consistency with the Model: Labeling alignment between the machine learning model and the nutritional dataset eliminates errors, allowing for accurate tracking and calculation of calories consumed.
- User Personalization: Once the nutritional data is processed, it is stored in the user’s account, ensuring personalized tracking and progress monitoring over time.
**For the user, this means:**

-The app not only detects what food they are consuming but also calculates how it contributes to their daily caloric and macronutrient intake.
This personalized tracking helps users make informed dietary decisions, aligning their consumption patterns with their fitness and health goals.

***User Input Data:***

Data collected from users, including age, weight, height, activity levels, and dietary goals, is stored securely in Firebase. This data is used to calculate personalized nutritional requirements such as Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE).
Real-Time Fridge Data:

Data from the smart refrigerator includes weight measurements and visual data captured by internal cameras. This data is used for automatic updates of the food inventory and consumption tracking.
The integration of these datasets enables the app to provide precise nutritional tracking and personalized dietary recommendations tailored to user goals.

Methdology

TBD

Evaluation & Analysis

TBD

Related Work

TBD

Conclusion

TBD
