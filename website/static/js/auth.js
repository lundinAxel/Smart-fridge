// Firebase Configuration
console.log(firebase ? "Firebase loaded" : "Firebase not loaded");

const firebaseConfig = {
    apiKey: "AIzaSyA9mMUpDJIh4yPGU4mx_0U4Xqtq4yb2haQ",
    authDomain: "freshlife-87d9a.firebaseapp.com",
    projectId: "freshlife-87d9a",
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();


// Function for login
window.login = function() {
    console.log("Login function called");

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    auth.signInWithEmailAndPassword(email, password)
        .then((userCredential) => {
            const user = userCredential.user; // Get the user object
            const uid = user.uid; // Fetch the UID
            console.log("Logged-in user UID:", uid);

            // Send UID to the server
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ uid: uid })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = "/base";
                } else {
                    alert("Error: " + data.error);
                }
            })
            .catch(error => console.error("Error sending UID to the server:", error));
        })
        .catch((error) => {
            console.error("Error during login:", error);
            alert("Error: " + error.message);
        });
};

function autoLogin(){
    
}


function logout() {
    auth.signOut().then(() => {
        sessionStorage.clear();
        window.location.href = "/login";
        window.location.reload();
    }).catch((error) => {
        console.error("Error logging out:", error);
        alert("Failed to log out: " + error.message);
    });
}


// Function for user registration
window.createAccount = function() {
    console.log("Register function called");
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const passwordRepeat = document.getElementById('password-repeat').value;

    if (password !== passwordRepeat) {
        console.log("Passwords do not match");
        document.getElementById('message').textContent = "Passwords do not match.";
        return;
    }

    console.log("Attempting to register user with email:", email);

    auth.createUserWithEmailAndPassword(email, password)
        .then((userCredential) => {
            const user = userCredential.user; // Get the user object
            const uid = user.uid; // Fetch the UID
            console.log("Logged-in user UID:", uid);
            console.log("User registered successfully:", userCredential.user);
            return auth.signInWithEmailAndPassword(email, password);
        })
        .then((userCredential) => {
            const user = userCredential.user;
            const uid = user.uid;
            console.log("User auto-logged in successfully, UID:", uid);

            // Send the UID to the backend to store it in the session
            return fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ uid: uid })
            });
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("UID stored in session successfully.");
                window.location.href = "/createUser";
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch((error) => {
            console.error("Error during registration:", error);
            alert("Error: " + error.message);
        });
};
