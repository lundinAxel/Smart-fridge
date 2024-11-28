// Function to handle option selection (similar to createUser.js)
const selections = {
    goal: null,
    activity: null
};

window.selectOption = function (type, value) {
    selections[type] = value;

    // Highlight the selected button
    document.querySelectorAll(`#${type}-group .select-button`).forEach(button => {
        button.classList.remove('selected'); // Remove the selected class from all buttons
    });

    const selectedButton = document.querySelector(`#${type}-group .select-button[onclick*="${value}"]`);
    if (selectedButton) {
        selectedButton.classList.add('selected'); // Add the selected class to the clicked button
    }

    // Update the hidden input field with the selected value
    const hiddenInput = document.getElementById(type);
    if (hiddenInput) {
        hiddenInput.value = value;
    }
};

// Submit form via AJAX to avoid page reload
window.submitUserDetails = async function () {
    const age = document.getElementById('age').value;
    const height = document.getElementById('height').value;
    const weight = document.getElementById('weight').value;

    if (age && height && weight && selections.goal && selections.activity) {
        try {
            const user = firebase.auth().currentUser;
            if (user) {
                const userId = user.uid;

                // Save user details to Firestore
                await db.collection("user").doc(userId).update({
                    age: parseInt(age),
                    height: parseInt(height),
                    weight: parseInt(weight),
                    goal: selections.goal,
                    activity_level: selections.activity
                });
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
