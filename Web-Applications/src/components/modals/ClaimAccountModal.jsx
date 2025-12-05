import React, { useState } from "react";
import { getCookie } from "../../utils/csrf";

function ClaimAccountModal({ visible, verificationData, onClose, onSuccess }) {
  if (!visible) return null;

  const [otp, setOtp] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState(""); // "success" or "error"

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      setMessage("Passwords do not match!");
      setMessageType("error");
      return;
    }
    
    if (password.length < 8) {
      setMessage("Password must be at least 8 characters long!");
      setMessageType("error");
      return;
    }
    
    setLoading(true);
    setMessage("");
    
    try {
      const res = await fetch('/api/verify-claim-account/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') || ''
        },
        credentials: 'include',
        body: JSON.stringify({
          verification_id: verificationData.verification_id,
          otp: otp,
          password: password
        })
      });
      
      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.error || 'Verification failed');
      }
      
      setMessage(data.message);
      setMessageType("success");
      
      // Success - trigger parent callback
      setTimeout(() => {
        onSuccess();
      }, 2000);
      
    } catch (err) {
      setMessage(err.message);
      setMessageType("error");
    } finally {
      setLoading(false);
    }
  };

  const handleResendOTP = async () => {
    try {
      const res = await fetch('/api/check-existing-patient/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') || ''
        },
        body: JSON.stringify({ email: verificationData.patient_email || verificationData.email })
      });
      
      const data = await res.json();
      
      if (data.has_existing_record) {
        setMessage("New OTP sent to your email!");
        setMessageType("success");
        // Update verification ID if a new one was created
        if (data.verification_id) {
          verificationData.verification_id = data.verification_id;
        }
      } else {
        setMessage("Failed to resend OTP. Please try again.");
        setMessageType("error");
      }
    } catch (err) {
      setMessage("Failed to resend OTP.");
      setMessageType("error");
    }
  };

  return (
    <div className="modal" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <span className="close" onClick={onClose}>&times;</span>
        
        <div className="login-container">
          <h2>Claim Your Existing Records</h2>
          
          <div className="info-box" style={{
            backgroundColor: '#e8f5e9',
            padding: '15px',
            borderRadius: '8px',
            marginBottom: '20px'
          }}>
            <p>We found your existing records for:</p>
            <h3 style={{ margin: '10px 0' }}>{verificationData.patient_name}</h3>
            <p>Enter the verification code sent to your email to link your records.</p>
          </div>
          
          {message && (
            <div className={`message-box ${messageType}`} style={{
              padding: '10px',
              borderRadius: '4px',
              marginBottom: '15px',
              backgroundColor: messageType === 'success' ? '#d4edda' : '#f8d7da',
              color: messageType === 'success' ? '#155724' : '#721c24',
              border: `1px solid ${messageType === 'success' ? '#c3e6cb' : '#f5c6cb'}`
            }}>
              {message}
            </div>
          )}
          
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="otp">Verification Code</label>
              <input
                type="text"
                id="otp"
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
                placeholder="Enter 6-digit code"
                maxLength="6"
                required
                style={{ letterSpacing: '3px', fontSize: '20px', textAlign: 'center' }}
              />
              <div className="form-hint">
                <a href="#" onClick={handleResendOTP} style={{ fontSize: '14px' }}>
                  Resend OTP
                </a>
              </div>
            </div>
            
            <div className="form-group">
              <label htmlFor="password">Create Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Minimum 8 characters"
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Re-enter your password"
                required
              />
            </div>
            
            <div className="password-requirements" style={{
              fontSize: '12px',
              color: '#666',
              marginBottom: '15px'
            }}>
              Password must contain:
              <ul style={{ margin: '5px 0', paddingLeft: '20px' }}>
                <li>At least 8 characters</li>
                <li>One uppercase letter</li>
                <li>One number</li>
              </ul>
            </div>
            
            <button 
              type="submit" 
              className="login-submit-btn"
              disabled={loading}
              style={{ backgroundColor: '#4CAF50' }}
            >
              {loading ? 'Verifying...' : 'Verify & Create Account'}
            </button>
            
            <div className="signup-link" style={{ marginTop: '20px' }}>
              <p>
                Don't want to claim this record?{' '}
                <a href="#" onClick={onClose} style={{ color: '#666' }}>
                  Go back to signup
                </a>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default ClaimAccountModal;