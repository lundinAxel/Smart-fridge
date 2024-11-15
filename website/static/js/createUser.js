// static/js/userDetails.js

const db = firebase.firestore();
const selections = {
    gender: null,
    goal: null,
    activity: null
};

// Function to handle option selection
window.selectOption = function(type, value) {
    selections[type] = value;

    // Highlight the selected button
    document.querySelectorAll(`#${type}-group .select-button`).forEach(button => {
        button.classList.remove('selected');
    });
    const selectedButton = [...document.querySelectorAll(`#${type}-group .select-button`)].find(btn => btn.textContent.toLowerCase() === value);
    selectedButton.classList.add('selected');
}

// Function to submit user details
window.submitUserDetails = async function () {
    const age = document.getElementById('age').value;
    const height = document.getElementById('height').value;
    const weight = document.getElementById('weight').value;

    if (age && height && weight && selections.gender && selections.goal && selections.activity) {
        try {
            const user = firebase.auth().currentUser;
            if (user) {
                const userId = user.uid;

                // Save user details to Firestore
                await db.collection("users").doc(userId).update({
                    age: parseInt(age),
                    height: parseInt(height),
                    weight: parseInt(weight),
                    gender: selections.gender,
                    goal: selections.goal,
                    activity_level: selections.activity
                });

                alert("User details saved successfully!");
                window.location.href = "/base"; // Redirect to the main app page
            } else {
                alert("No user is logged in.");
            }
        } catch (error) {
            console.error("Error saving user details:", error);
            alert("Failed to save user details. Please try again.");
        }
    } else {
        alert("Please fill in all fields.");
    }
}
