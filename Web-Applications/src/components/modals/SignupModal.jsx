import React from "react";
import { getCookie } from "../../utils/csrf";

function SignupModal({ onClose, onOpenLogin, visible }) {
  if (!visible) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    const firstName = e.target.firstName.value;
    const lastName = e.target.lastName.value;
    const email = e.target.email.value;
    const password = e.target.password.value;
    const confirmPassword = e.target.confirmPassword.value;

    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    (async () => {
      try {
        const res = await fetch('/api/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') || ''
          },
          credentials: 'include',
          body: JSON.stringify({
            first_name: firstName,
            last_name: lastName,
            email,
            password
          })
        });

        const text = await res.text();
        let data = {};
        try {
          data = text ? JSON.parse(text) : {};
        } catch (err) {
          data = { error: text || res.statusText };
        }

        if (!res.ok) throw new Error(data.error || res.statusText || 'Register failed');

        alert('Account created successfully!');
        onClose();
      } catch (err) {
        alert(err.message);
      }
    })();
  };

  return (
    <div className="modal" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <span className="close" onClick={onClose}>
          &times;
        </span>
        <div className="login-container">
          <h2>Create Account</h2>
          <form id="signupForm" onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="signupFirstName">First Name</label>
                <input type="text" id="signupFirstName" name="firstName" required />
              </div>

              <div className="form-group">
                <label htmlFor="signupLastName">Last Name</label>
                <input type="text" id="signupLastName" name="lastName" required />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="signupEmail">Email</label>
              <input type="email" id="signupEmail" name="email" required />
            </div>

            <div className="form-group">
              <label htmlFor="signupPassword">Password</label>
              <input type="password" id="signupPassword" name="password" required />
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                required
              />
            </div>

            <button type="submit" className="login-submit-btn">
              CREATE ACCOUNT
            </button>

            <div className="signup-link">
              <p>
                Already have an account?{" "}
                <a href="#" onClick={onOpenLogin}>
                  Login here
                </a>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default SignupModal;
