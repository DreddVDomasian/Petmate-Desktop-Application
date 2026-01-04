import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getCookie } from "../../utils/csrf";
import { apiFetch } from "../../config/api";
import ForgotPasswordModal from "../modals/ForgetPasswordModal";

function LoginModal({ onClose, onOpenSignup, visible }) {
  const [showForgot, setShowForgot] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  if (!visible) return null;

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
        const res = await apiFetch("/api/login/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken") || "",
          },
          body: JSON.stringify({ email, password }),
        });

        const text = await res.text();
        let data = {};
        try {
          data = text ? JSON.parse(text) : {};
        } catch {
          data = { error: text || res.statusText };
        }

        if (!res.ok) throw new Error(data.error || res.statusText || "Login failed");

        onClose();
        navigate("/dashboard");
      } catch (err) {
        alert(err.message);
      }
    })();
  };

  return (
    <>
      {!showForgot && (
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
                  <div className="password-input-wrapper">
                    <input
                      type={showPassword ? "text" : "password"}
                      id="loginPassword"
                      name="password"
                      required
                    />
                    <img
                      src={showPassword ? "/assets/icons/hide.png" : "/assets/icons/eye.png"}
                      alt={showPassword ? "Hide Password" : "Show Password"}
                      className="toggle-password-icon"
                      onClick={() => setShowPassword(!showPassword)}
                    />
                  </div>
                </div>

                <div className="form-options">
                  <label className="checkbox-container">
                    <input type="checkbox" id="rememberMe" />
                    <span className="checkmark"></span>
                    Remember me
                  </label>
                  <a className="forgot-link" onClick={() => setShowForgot(true)}>
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
      )}

      {showForgot && (
        <ForgotPasswordModal
          onClose={onClose}
          onBack={() => setShowForgot(false)}
        />
      )}
    </>
  );
}

export default LoginModal;
