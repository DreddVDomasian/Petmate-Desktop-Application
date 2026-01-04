'use strict';

// Import Firebase SDK
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.1.0/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/12.1.0/firebase-auth.js";
import { getFirestore, doc, getDoc,setDoc } from "https://www.gstatic.com/firebasejs/12.1.0/firebase-firestore.js";

const firebaseConfig = {
    apiKey: "AIzaSyAubnoJNXMp0eJ9A2bQM1FaOfMlk6X0Les",
    authDomain: "woodworks-dc7b3.firebaseapp.com",
    projectId: "woodworks-dc7b3",
    storageBucket: "woodworks-dc7b3.firebasestorage.app",
    messagingSenderId: "355879129478",
    appId: "1:355879129478:web:35abd92fa5ebb5c60d1c07"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

//Validates email format
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(String(email).toLowerCase());
}

//Handles login with Firebase
function login() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;


    if (!email || !validateEmail(email)) {
        showAlert("Please enter a valid email address.");
        return;
    }
    if (!password) {
        showAlert("Please enter your password.");
        return;
    }

    function showAlert(message, callback = null) {
        const alertBox = document.getElementById("customAlert");
        const alertMessage = document.getElementById("alertMessage");
        const okBtn = document.getElementById("alertOk");
        const closeBtn = document.getElementById("alertClose");

        alertMessage.textContent = message;
        alertBox.style.display = "flex";

        // clear old listeners
        const newOkBtn = okBtn.cloneNode(true);
        okBtn.parentNode.replaceChild(newOkBtn, okBtn);

        const newCloseBtn = closeBtn.cloneNode(true);
        closeBtn.parentNode.replaceChild(newCloseBtn, closeBtn);

        // OK button → close + callback
        newOkBtn.addEventListener("click", () => {
            closeAlert();
            if (callback) callback();
        });

        // X button → close lang
        newCloseBtn.addEventListener("click", closeAlert);
    }

    function closeAlert() {
        document.getElementById("customAlert").style.display = "none";
    }

    function showLoadingModal(title, message) {
        const modal = document.getElementById("loadingModal");
        const titleEl = document.getElementById("loading-title");
        const messageEl = document.getElementById("loading-message");
        
        if (!modal) {
            // Fallback if modal doesn't exist - create a simple one
            const backdrop = document.createElement('div');
            backdrop.id = 'loadingModal';
            backdrop.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);display:flex;justify-content:center;align-items:center;z-index:9999;';
            backdrop.innerHTML = `
                <div style="background:white;border-radius:12px;padding:30px;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,0.15);">
                    <div style="width:50px;height:50px;border:4px solid #ddd;border-top-color:#552106;border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 20px;" id="spinner"></div>
                    <h3 style="margin:0 0 10px;color:#552106;">${title}</h3>
                    <p style="margin:0;color:#666;">${message}</p>
                </div>
                <style>
                    @keyframes spin { to { transform: rotate(360deg); } }
                </style>
            `;
            document.body.appendChild(backdrop);
        } else {
            if (titleEl) titleEl.textContent = title;
            if (messageEl) messageEl.textContent = message;
            modal.style.display = "flex";
        }
    }

    function hideLoadingModal() {
        const modal = document.getElementById("loadingModal");
        if (modal) modal.style.display = "none";
    }

// Firebase login - Show loading modal IMMEDIATELY when login starts
    // Show loading modal right away
    showLoadingModal("Authenticating", "Verifying your credentials...");
    
    signInWithEmailAndPassword(auth, email, password)
        .then(async (userCredential) => {
            const user = userCredential.user;
            console.log("Logged in:", user.email);

            // Update loading message while fetching user data
            const titleEl = document.getElementById("loading-title");
            const messageEl = document.getElementById("loading-message");
            if (titleEl) titleEl.textContent = "Setting up your account";
            if (messageEl) messageEl.textContent = "Please wait...";

            const ref = doc(db, "users", user.uid);
            const snapshot = await getDoc(ref);

            let role = "student";
            let username = "";
            let firstName = "";
            let lastName = "";

            if (snapshot.exists()) {
                const data = snapshot.data();
                role = data.role || "student";
                username = data.username || user.email.split("@")[0];
                firstName = data.firstName || username;
                lastName = data.lastName || "";

                // ✅ unarchive if previously deleted
                if (data.archived === true) {
                    await setDoc(ref, { archived: false }, { merge: true });
                }

            } else {
                // ✅ recreate profile if it was deleted
                await setDoc(ref, {
                    role: "student",
                    username: user.email.split("@")[0],
                    firstName: user.email.split("@")[0],
                    lastName: "",
                    archived: false,
                    createdAt: new Date()
                });
                username = user.email.split("@")[0];
                firstName = username;
                lastName = "";
            }

            // ✅ Save user info locally
            localStorage.setItem("username", username);
            localStorage.setItem("role", role);
            sessionStorage.setItem("userEmail", email);
            sessionStorage.setItem("userRole", role);

            // Update to success message
            if (titleEl) titleEl.textContent = "Login Successful";
            if (messageEl) messageEl.textContent = `Welcome ${username || role}!`;
            
            // Redirect after brief delay
            setTimeout(() => {
                if (role === "teacher") {
                    window.location.href = "teacher.html";
                } else {
                    window.location.href = "students.html";
                }
            }, 1000);
        })
    .catch(error => {
        console.error("Login error:", error.message);
        hideLoadingModal();
        showAlert(`Error: ${error.message}`);
    });

}

document.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.getElementById('submit');
    const togglePassword = document.getElementById('togglePassword');

    togglePassword.onclick = function() {
        const passwordField = document.getElementById('password');
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        this.src = type === 'password' ? 'Images/eye.png' : 'Images/hide.png';
    }

    if (loginBtn) {
        loginBtn.addEventListener("click", function(event) {
            event.preventDefault();
            login();
        });
    }

    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                login();
            }
        });
    });

    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            const email = this.value.trim();
            this.style.borderColor = (email && !validateEmail(email)) ? '#e74c3c' : '#b68d5e';
        });

        emailInput.focus();
    }


});