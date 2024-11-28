document.getElementById('fileUpload').addEventListener('change', function () {
    const uploadMessage = document.getElementById('uploadMessage');
    alert("running this");
    
    // Check if a file is selected
    if (this.files && this.files.length > 0) {
        uploadMessage.textContent = `File "${this.files[0].name}" uploaded successfully!`;
        uploadMessage.style.display = 'block'; // Show the message
    } else {
        uploadMessage.textContent = '';
        uploadMessage.style.display = 'none'; // Hide the message
    }
});