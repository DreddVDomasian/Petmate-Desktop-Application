import React from "react";

function SignupModal({ onClose, onOpenLogin, visible }) {
  if (!visible) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    const name = e.target.name.value;
    const email = e.target.email.value;
    const password = e.target.password.value;
    const confirmPassword = e.target.confirmPassword.value;

    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    alert("Account created successfully!");
    onClose();
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
            <div className="form-group">
              <label htmlFor="signupName">Full Name</label>
              <input type="text" id="signupName" name="name" required />
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
