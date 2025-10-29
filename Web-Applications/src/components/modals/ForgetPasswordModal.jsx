import React, { useState } from "react";

export default function ForgotPasswordModal({ onClose, onBack }) {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");


    //HINDI PA ITO NAGAGAWANG FUNCTIONAL, FRONTEND PALANG, NEED DAPAT MAGSEND NG OTP SA EMAIL NG USER
  const handleSubmit = (e) => {
    e.preventDefault();
    setMessage("Password reset link has been sent to your email!");
    setEmail("");
  };

  return (
    <div className="modal" onClick={onClose}>
      <div className="modal-content forgot" onClick={(e) => e.stopPropagation()}>
        <span className="close" onClick={onClose}>
          &times;
        </span>

        <div className="forgot-container">
          <a className="back-link" onClick={onBack}>
            ← Back to Login
          </a>

          <h2>Forgot Password</h2>
          <p className="subtitle">
            Enter your registered email address and we’ll send you a link to reset your password.
          </p>

          <form onSubmit={handleSubmit}>
            <label>Email</label>
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <button type="submit" className="reset-btn">
              Send Reset Link
            </button>

            {message && <p className="success-msg">{message}</p>}
          </form>
        </div>
      </div>
    </div>
  );
}
