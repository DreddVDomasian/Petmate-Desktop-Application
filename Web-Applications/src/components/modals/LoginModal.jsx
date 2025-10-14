import React from "react";
import { useNavigate } from "react-router-dom";
import { getCookie } from "../../utils/csrf";

function LoginModal({ onClose, onOpenSignup, visible }) {
  const navigate = useNavigate(); // Hook for navigation

  if (!visible) return null; // Hides modal when not active

  const handleSubmit = (e) => {
    e.preventDefault();
    const email = e.target.email.value;
    const password = e.target.password.value;

    if (!email || !password) {
      alert("Please fill in all fields");
      return;
    }

    (async () => {
      try {
        const res = await fetch('/api/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') || ''
          },
          credentials: 'include',
          body: JSON.stringify({ email, password })
        });

        const text = await res.text();
        let data = {};
        try {
          data = text ? JSON.parse(text) : {};
        } catch (err) {
          // non-json response (HTML or empty), keep text in error
          data = { error: text || res.statusText };
        }

        if (!res.ok) throw new Error(data.error || res.statusText || 'Login failed');

        onClose();
        navigate('/dashboard');
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
          <h2>Login to PetMate</h2>
          <form id="loginForm" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="loginEmail">Email</label>
              <input type="email" id="loginEmail" name="email" required />
            </div>

            <div className="form-group">
              <label htmlFor="loginPassword">Password</label>
              <input type="password" id="loginPassword" name="password" required />
            </div>

            <div className="form-options">
              <label className="checkbox-container">
                <input type="checkbox" id="rememberMe" />
                <span className="checkmark"></span>
                Remember me
              </label>
              <a href="#" className="forgot-password">
                Forgot Password?
              </a>
            </div>

            <button type="submit" className="login-submit-btn">
              LOGIN
            </button>

            <div className="signup-link">
              <p>
                Don't have an account?{" "}
                <a href="#" onClick={onOpenSignup}>
                  Sign up here
                </a>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default LoginModal;
