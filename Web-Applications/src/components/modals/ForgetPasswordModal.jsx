import React, { useState } from "react";
import axios from "axios";

export default function ForgotPasswordModal({ onClose, onBack }) {
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [step, setStep] = useState(1);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState(""); // 'success' or 'error'
  const [isSending, setIsSending] = useState(false);

  // Password validation states
  const [passwordValid, setPasswordValid] = useState({
    length: false,
    uppercase: false,
    lowercase: false,
    number: false,
    special: false
  });

  const validatePassword = (pwd) => {
    setPasswordValid({
      length: pwd.length >= 8,
      uppercase: /[A-Z]/.test(pwd),
      lowercase: /[a-z]/.test(pwd),
      number: /\d/.test(pwd),
      special: /[!@#$%^&*()_\-+=\[\]{};:'",.<>\/?\\|`~]/.test(pwd)
    });
  };

  const sendOtp = async (e) => {
    e.preventDefault();
    if (isSending) return;
    setIsSending(true);

    try {
      await axios.post(
        "http://127.0.0.1:8000/api/send-reset-otp/",
        { email, source: 'web' },
        { withCredentials: true }
      );
      setMessage("OTP sent to your email!");
      setMessageType("success");
      setStep(2);
    } catch (error) {
      console.error("sendOtp error:", error.response?.status, error.response?.data);
      setMessage(error.response?.data?.error || "Failed to send OTP");
      setMessageType("error");
    } finally {
      setIsSending(false);
    }
  };

  const verifyOtp = async (e) => {
    e.preventDefault();

    if (newPassword !== confirmPassword) {
      setMessage("Passwords do not match.");
      setMessageType("error");
      return;
    }

    // Check full password restrictions
    const allValid = Object.values(passwordValid).every(v => v === true);
    if (!allValid) {
      setMessage("Your password does not meet the required strength.");
      setMessageType("error");
      return;
    }

    try {
      await axios.post(
        "http://127.0.0.1:8000/api/verify-reset-otp/",
        { email, otp, new_password: newPassword },
        { withCredentials: true }
      );
      setMessage("Password reset successfully!");
      setMessageType("success");
      setStep(3);
    } catch (error) {
      console.error("verifyOtp error:", error.response?.status, error.response?.data);
      setMessage(error.response?.data?.error || "Failed to reset password");
      setMessageType("error");
    }
  };

  return (
    <div className="modal" onClick={onClose}>
      <div className="modal-content forgot" onClick={(e) => e.stopPropagation()}>
        <span className="close" onClick={onClose}>&times;</span>
        <div className="forgot-container">
          <a className="back-link" onClick={onBack}>← Back to Login</a>

          {step === 1 && (
            <>
              <h2>Forgot Password</h2>
              <p className="subtitle">Enter your registered email to receive an OTP.</p>
              <form onSubmit={sendOtp}>
                <div className="form-group">
                  <label>Email</label>
                  <input 
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <button type="submit" className="reset-btn">Send OTP</button>
              </form>
            </>
          )}

          {step === 2 && (
            <>
              <h2>Reset Password</h2>
              <p className="otp-notice">OTP sent to your email!</p>
              <form onSubmit={verifyOtp}>
                <div className="form-group">
                  <label>OTP Code</label>
                  <input 
                    type="text"
                    placeholder="Enter OTP"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>New Password</label>
                  <input 
                    type="password"
                    placeholder="Enter new password"
                    value={newPassword}
                    onChange={(e) => {
                      setNewPassword(e.target.value);
                      validatePassword(e.target.value);
                    }}
                    required
                  />
                </div>



                <div className="form-group">
                  <label>Confirm New Password</label>
                  <input 
                    type="password"
                    placeholder="Confirm new password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                  />
                </div>

                                {/* Password checklist UI */}
                <ul className="password-checklist vertical">
                  <li className={passwordValid.uppercase ? "valid" : ""}>
                    <span className="icon">{passwordValid.uppercase ? "✔" : "✖"}</span> At least 1 uppercase
                  </li>
                  <li className={passwordValid.lowercase ? "valid" : ""}>
                    <span className="icon">{passwordValid.lowercase ? "✔" : "✖"}</span> At least 1 lowercase
                  </li>
                  <li className={passwordValid.number ? "valid" : ""}>
                    <span className="icon">{passwordValid.number ? "✔" : "✖"}</span> At least 1 number
                  </li>
                  <li className={passwordValid.special ? "valid" : ""}>
                    <span className="icon">{passwordValid.special ? "✔" : "✖"}</span> Special character
                  </li>
                  <li className={passwordValid.length ? "valid" : ""}>
                    <span className="icon">{passwordValid.length ? "✔" : "✖"}</span> Minimum 8 characters
                  </li>
                </ul>

                <button type="submit" className="reset-btn">Verify & Reset</button>
              </form>
            </>
          )}


          {step === 3 && (
            <div className="success-container">
              <h2>Success!</h2>
              <p>Your password has been reset. You can now log in.</p>
            </div>
          )}

          {message && (
            <p className={messageType === "error" ? "error-msg" : "success-msg"}>
              {message}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
