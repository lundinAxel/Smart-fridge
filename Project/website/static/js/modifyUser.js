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
