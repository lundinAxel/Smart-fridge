# FreshLife
## Collaborators

| Name                | Organization                          | Department                                 | Email                           |
|---------------------|--------------------------------------|-------------------------------------------|---------------------------------|
| **Aleksander Jankovic**   | Högskolan i Halmstad |         Computer Engineering              | [alejan22@student.hh.se](mailto:alejan22@student.hh.se) |
| **Axel Lundin**      | Högskolan i Halmstad | Computer Engineering | [axelun22@student.hh.se](mailto:axelun22@student.hh.se) |
| **Hyunsuk Lee**     | Hanyang University                   | tbh                      | [tbh] |
| **Mohammed Ismaili**      | Al Akhawayn University             | Computer Science                      | [Mo.Ismaili@aui.ma](mailto:Mo.Ismaili@aui.ma) |

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

The **User Input Data** serves as the foundation for the app's personalized nutritional guidance and tracking capabilities. It is designed to provide users with tailored recommendations based on their unique profiles and fitness goals.

**Data Collected:**

  - Personal Information: Age, weight, height, and gender.
  - Activity Levels: Frequency and intensity of physical activity (e.g., sedentary, moderate, or high activity levels).
  - Dietary Goals: Users specify goals such as weight loss, maintenance, or bulking for muscle gain.

**Integration:**

  - This information is stored securely in Firebase, ensuring that user data is safe and accessible for real-time calculations and updates.
  - The app uses this data to compute Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE), which are essential for setting calorie and macronutrient 
  targets.

**Purpose:**

  - The collected data allows the app to personalize recommendations, such as calorie limits and macronutrient distribution, based on the user’s current stats and desired 
  outcomes.
  - For example, a user aiming for weight loss will be guided to maintain a calorie deficit, while someone focusing on muscle gain will receive a higher calorie and protein 
  target.

**For the user, this means:**

  - They can effortlessly track their progress towards specific dietary goals.
  - The app dynamically adjusts recommendations as their weight, activity level, or goals change, ensuring a continuously optimized experience.
  Real-Time Fridge Data
  - In conjunction with user input data, the app also incorporates real-time information from the smart refrigerator:
    - Weight Measurements: Captured by internal scales to detect changes in food quantities.
    - Visual Data: Analyzed by the fruit recognition model to identify items added or removed from the fridge.
    These real-time updates ensure accurate tracking of food consumption, which is automatically synced with the user's profile and dietary goals.

Together, these datasets empower users to make informed dietary choices and align their eating habits with their health objectives seamlessly

Methdology

The **methodology of FreshLife** is centered on the seamless integration of smart technology, machine learning, and personalized nutrition guidance to empower users in achieving their health goals. Here’s how each component contributes to the app’s overall functionality:

**1. Data Collection and Integration**

 - **Image and Nutritional Data:**
   - The Image Classification Dataset is used to train a custom machine learning model capable of identifying fruits and vegetables. This dataset was curated from the 
   Kaggle Fruits 360 Dataset and optimized for the specific requirements of a smart refrigerator environment.
   - The Nutritional Information Dataset provides detailed caloric and macronutrient data for each identified food item. This data is stored in both JSON format and 
   Firebase Firestore for accuracy, consistency, and real-time access.

 - **User Input Data:**
   - Users input personal information (age, weight, height, activity levels, and dietary goals) into the app. This data is securely stored in Firebase and used to compute 
   their Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE), forming the basis of personalized dietary recommendations.

 - **Real-Time Fridge Data:**
   - Smart refrigerator sensors capture weight changes and internal cameras provide visual data, enabling the system to track food consumption dynamically. This data is 
   paired with the classification and nutritional datasets to calculate calories consumed.

**2. Machine Learning Model Development**
  - A Convolutional Neural Network (CNN) was trained on the curated dataset using TensorFlow and Keras. The model processes images and videos to identify food items with a 
  - test accuracy of 97%.

**Data Augmentation:**
  - Techniques such as rotation, scaling, flipping, and shifting were employed during training to improve the model's robustness to variations in lighting, angles, and 
  environmental conditions.
  - The model is optimized for real-world scenarios, such as detecting items in a refrigerator environment, ensuring seamless functionality when paired with internal 
  sensors and cameras.

**3. Data Processing and Storage**
  - Once the machine learning model identifies a food item, the app queries the Nutritional Information Dataset in Firebase Firestore to retrieve corresponding nutritional 
  values. These values are calculated based on weight measurements recorded by the smart refrigerator’s internal scales.
  - All consumption data is securely stored in the user’s profile for tracking and analysis.

**4. Personalized Nutritional Guidance**
  - Using user input data, the app computes personalized targets, including calorie limits and macronutrient distribution, based on the user's goals (e.g., weight loss, 
  maintenance, or bulking).
  - Real-time adjustments are made as users update their weight, activity level, or dietary goals.

**5. Progress Tracking and Feedback**
  - FreshLife provides detailed charts and summaries of daily calorie consumption, macronutrient intake, and trends over time.
  This data empowers users to make informed dietary decisions and refine their habits to align with their fitness objectives.

**Why This Methodology Works**
The integrated approach of using machine learning for food recognition, real-time data from a smart refrigerator, and personalized user profiles ensures:
  - High accuracy and reliability in tracking food consumption.
  - Tailored guidance that adapts to individual needs and progress.
  An intuitive and effortless experience for users aiming to achieve their health and fitness goals.
  - This methodology not only enhances user engagement but also sets the foundation for a smarter, healthier lifestyle through innovative technology.

***Evaluation & Analysis***

The evaluation of **FreshLife** revolves around its modular architecture, performance, real-world integration potential, and overall user impact. This analysis highlights the key strengths and challenges faced during development and testing, along with a comparative assessment against existing solutions.

**User Testing**
 - **Current Status:**
   - While public user testing has not yet been conducted as the app is still in its beta stage, rigorous internal testing was performed to ensure reliability and usability.
   - The development team extensively tested edge cases, including:
     - Functionality under different lighting conditions.
     - Scenarios prone to user errors (e.g., incorrect data inputs, account creation issues).
   - The app's modular programming and MVC structure allowed for swift debugging and incremental feature addition, ensuring adaptability during testing.
   - Extensive try-catch error handling was implemented to mitigate crashes, making the app resilient against common faults.

**Performance Metrics**
 - **Accuracy:**
   - The Convolutional Neural Network (CNN) achieved a 97% test accuracy during internal validation, showcasing high reliability in identifying fruits and vegetables.
 - **Processing Speed:**
   - The decision to reduce the dataset size significantly improved the model's processing speed, optimizing its real-time functionality.
   - On the current hardware setup (a standard laptop), the model processes predictions, updates the database, and calculates results with a latency of less than 50 ms.
   - This speed can be further improved by deploying the app on a dedicated server or cloud platform.

 - **System Efficiency:**
   - By streamlining the dataset and modularizing the code, the app efficiently handles prediction tasks while maintaining the flexibility to integrate additional features 
   in the future.

**Integration and Real-World Use**
 - **Prototype Design:**
   - FreshLife is a prototype designed to showcase its potential for integration with a smart refrigerator.
   - The app demonstrates real-world functionality by pairing internal camera data with weight measurements, simulating a working model for live dietary tracking.

 - **Handling Edge Cases:**
   - The app was rigorously tested to ensure accuracy under suboptimal conditions, such as:
     - Poor lighting.
     - Detecting multiple or partially obscured items.
   - While the prototype performs well in controlled conditions, further refinement is necessary to handle more complex real-world scenarios effectively.

**Challenges and Improvements**
 - **Challenges Faced:**
   - **Hardware Limitations:**
     - Training and running the model on a laptop presented challenges in terms of processing power and speed.
   - **Dataset Optimization:**
     - To improve speed and accuracy, the dataset size was minimized by removing unnecessary classes and focusing on core use-case items.
    - **Fruit-Specific Cases:**
     - Edge cases, such as differentiating between similar-looking fruits or vegetables, required additional adjustments to the model.
    - **Improvements Made:**
     - Continuous iteration during development led to enhanced understanding of the app's requirements, resulting in:
       - Better integration with fitness goals.
       - Improved visualization and usability for users.

**Comparison with Existing Solutions**
 - **Market Research:**
   - FreshLife's design and features were inspired by apps like RepCount and RunKeeper, which provided insight into competitive user-centric features.
   - While existing fitness apps focus on workouts and general tracking, FreshLife differentiates itself by offering automated food tracking integrated with a smart 
   refrigerator.
 - **Competitive Edge:**
   - FreshLife stands out by minimizing user effort while providing precise dietary insights, a feature not commonly available in comparable apps.

**User Impact**
 - **User-Centric Features:**
   - The app offers daily visualizations of calorie, protein, carbohydrate, and fat intake, empowering users to track their nutritional goals easily.
   - Features like goal updates dynamically adjust the user's target metrics, ensuring a tailored experience.
 - **Ease of Use:**
   - By automating food tracking through the fridge's internal camera and scale, FreshLife reduces the manual effort required from users, promoting long-term engagement.
 - **Potential Impact:**
   - The app is designed to help users achieve fitness goals such as bulking, maintenance, or weight loss, with minimal input, making it accessible to a wide range of users.

**Summary of Evaluation**
 - **Strengths:**
   - High prediction accuracy (97%).
   - Low latency (under 50 ms).
   - Modular and scalable architecture allows for future enhancements.
   - User-friendly interface with minimal manual input required.
 - **Areas for Improvement:**
   - Transitioning from a laptop-based prototype to a cloud-based platform for faster processing and scalability.
   - Expanding the dataset and refining the model to handle edge cases more effectively.
   - Conducting public user testing for broader feedback and usability insights.
   - The Evaluation & Analysis showcases FreshLife's potential as an innovative solution for automated food tracking and personalized nutrition guidance, laying the 
   foundation for its future development and real-world application.

***Conclusion***

**FreshLife** represents a forward-thinking approach to integrating smart technology with personalized nutrition and fitness guidance. By leveraging cutting-edge machine learning, real-time data from smart refrigerators, and user-centric design principles, the app aims to redefine how individuals track and manage their dietary habits.

**Throughout its development, FreshLife has demonstrated:**
 - High Accuracy: A CNN model with 97% accuracy ensures reliable food recognition and nutritional analysis.
 - Efficiency: Optimized processing speed and modular architecture allow for quick responses and easy scalability.
 - User-Focused Innovation: Features like automated food tracking, dynamic goal adjustment, and visual progress tracking minimize user effort while enhancing engagement.

While currently in its prototype stage, FreshLife showcases immense potential for real-world application. By automating food tracking and providing actionable dietary 
insights, the app empowers users to make informed choices, helping them achieve fitness goals such as weight loss, maintenance, or muscle gain.

**Future Prospects:**
 - Transitioning to cloud-based infrastructure to further improve processing speed and scalability.
 - Expanding datasets and refining models to handle a broader range of real-world scenarios.
 - Conducting public testing to gather valuable feedback and enhance usability.
 - Integrating additional features, such as compatibility with wearable devices or expanded recipe suggestions.

FreshLife bridges the gap between technology and healthy living, offering an intuitive, effective, and innovative tool for achieving fitness goals. With further development and refinement, it has the potential to become a market leader in automated nutritional tracking.
