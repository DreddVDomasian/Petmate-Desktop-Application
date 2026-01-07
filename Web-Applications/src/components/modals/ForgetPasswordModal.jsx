import React, { useState } from "react";
import { apiFetch, readJsonSafe } from "../../config/api";

export default function ForgotPasswordModal({ onClose, onBack }) {
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
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
      const res = await apiFetch(
        "/api/send-reset-otp/",
        {
          method: 'POST',
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, source: 'web' })
        }
      );

      if (!res.ok) {
        const data = await readJsonSafe(res);
        const msg = data?.error || data?.detail || `Failed to send OTP (${res.status})`;
        throw new Error(msg);
      }

      setMessage("OTP sent to your email!");
      setMessageType("success");
      setStep(2);
    } catch (error) {
      console.error("sendOtp error:", error);
      setMessage(error?.message || "Failed to send OTP");
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
      const res = await apiFetch(
        "/api/verify-reset-otp/",
        {
          method: 'POST',
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, otp, new_password: newPassword })
        }
      );

      if (!res.ok) {
        const data = await readJsonSafe(res);
        const msg = data?.error || data?.detail || `Failed to reset password (${res.status})`;
        throw new Error(msg);
      }

      setMessage("Password reset successfully!");
      setMessageType("success");
      setStep(3);
    } catch (error) {
      console.error("verifyOtp error:", error);
      setMessage(error?.message || "Failed to reset password");
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
                  <div className="password-input-wrapper">
                    <input 
                      type={showNewPassword ? "text" : "password"}
                      placeholder="Enter new password"
                      value={newPassword}
                      onChange={(e) => {
                        setNewPassword(e.target.value);
                        validatePassword(e.target.value);
                      }}
                      required
                    />
                    <img
                      src={showNewPassword ? "/assets/icons/hide.png" : "/assets/icons/eye.png"}
                      alt={showNewPassword ? "Hide Password" : "Show Password"}
                      className="toggle-password-icon"
                      onClick={() => setShowNewPassword(!showNewPassword)}
                    />
                  </div>
                </div>



                <div className="form-group">
                  <label>Confirm New Password</label>
                  <div className="password-input-wrapper">
                    <input 
                      type={showConfirmPassword ? "text" : "password"}
                      placeholder="Confirm new password"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      required
                    />
                    <img
                      src={showConfirmPassword ? "/assets/icons/hide.png" : "/assets/icons/eye.png"}
                      alt={showConfirmPassword ? "Hide Password" : "Show Password"}
                      className="toggle-password-icon"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    />
                  </div>
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
