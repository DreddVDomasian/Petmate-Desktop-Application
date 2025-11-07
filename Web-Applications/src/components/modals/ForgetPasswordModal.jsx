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

  const sendOtp = async (e) => {
    e.preventDefault();
    if (isSending) return; //  prevents sa pag multiple API calls
    setIsSending(true);

    try {
      await axios.post("http://127.0.0.1:8000/api/send-reset-otp/", { email }, { withCredentials: true });
      setMessage(" OTP sent to your email!");
      setMessageType("success");
      setStep(2);
    } catch (error) {
      console.error("sendOtp error:", error.response?.status, error.response?.data);
      setMessage(error.response?.data?.error || " Failed to send OTP");
      setMessageType("error");
    } finally {
      setIsSending(false);
    }
  };

  const verifyOtp = async (e) => {
    e.preventDefault();

    // client-side confirm password check
    if (newPassword !== confirmPassword) {
      setMessage("Passwords do not match.");
      setMessageType("error");
      return;
    }

    try {
      await axios.post("http://127.0.0.1:8000/api/verify-reset-otp/", {
        email,
        otp,
        new_password: newPassword,
      }, { withCredentials: true });
      setMessage(" Password reset successfully!");
      setMessageType("success");
      setStep(3);
    } catch (error) {
      console.error("verifyOtp error:", error.response?.status, error.response?.data);
      setMessage(error.response?.data?.error || " Failed to reset password ");
      setMessageType("error");
    }
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

          {step === 1 && (
            <>
              <h2>Forgot Password</h2>
              <p>Enter your registered email to receive an OTP.</p>
              <form onSubmit={sendOtp}>
                <label>Email</label>
                <input
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
                <button type="submit" className="reset-btn">
                  Send OTP
                </button>
              </form>
            </>
          )}

          {step === 2 && (
            <>
              <h2>Reset Password</h2>
              <form onSubmit={verifyOtp}>
                <label>OTP Code</label>
                <input
                  type="text"
                  placeholder="Enter OTP"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  required
                />

                <label>New Password</label>
                <input
                  type="password"
                  placeholder="Enter new password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                />

                <label>Confirm New Password</label>
                <input
                  type="password"
                  placeholder="Confirm new password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />

                <button type="submit" className="reset-btn">
                  Verify & Reset
                </button>
              </form>
            </>
          )}

          {step === 3 && (
            <div>
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
