import React, { useState, useEffect } from "react";
import axios from "axios";

export default function Settings() {
  const [activeTab, setActiveTab] = useState("details");

  const [userFirstName, setUserFirstName] = useState("");
  const [userMiddleName, setUserMiddleName] = useState("");
  const [userLastName, setUserLastName] = useState("");
  const [userEmail, setUserEmail] = useState("");
  const [userPhoneNumber, setUserPhoneNumber] = useState("");

  // For password change
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordMessage, setPasswordMessage] = useState("");
  const [passwordMessageType, setPasswordMessageType] = useState(""); // "success" or "error"

  // helper for CSRF cookie
  const getCookie = (name) => {
    const m = document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)");
    return m ? decodeURIComponent(m.pop()) : null;
  };

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        //  rely on cookies (withCredentials) and a simple GET
        const res = await axios.get(
          "http://localhost:8000/api/user/profile/",
          { withCredentials: true }
        );

        const data = res.data || {};

        const firstName = data.first_name || data.firstName || "";
        const middleName = data.middle_name || data.middleName || "";
        const lastName = data.last_name || data.lastName || "";
        const email = data.email || data.mail || "";
        const phone =
          data.phoneNumber ||
          data.phone ||
          (data.patient_profile && (data.patient_profile.phone || data.patient_profile.phoneNumber)) ||
          "";

        setUserFirstName(firstName);
        setUserMiddleName(middleName);
        setUserLastName(lastName);
        setUserEmail(email);
        setUserPhoneNumber(phone || "");
      } catch (err) {
        // Keep this minimal — inspect console for details
        console.error("Failed to fetch profile:", err);
      }
    };
    fetchProfile();
  }, []);

  const handlePasswordChange = async (e) => {
    e.preventDefault();

    if (newPassword !== confirmPassword) {
      setPasswordMessage("Passwords do not match.");
      setPasswordMessageType("error");
      return;
    }

    try {
      // only send CSRF header (no token header here)
      const csrf = getCookie("csrftoken") || getCookie("csrf") || getCookie("XSRF-TOKEN");
      const headers = {};
      if (csrf) headers["X-CSRFToken"] = csrf;

      const response = await axios.post(
        "http://localhost:8000/api/web-reset-password/",
        {
          current_password: currentPassword,
          new_password: newPassword,
        },
        { withCredentials: true, headers }
      );

      setPasswordMessage(response.data.message || "Password updated successfully!");
      setPasswordMessageType("success");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (error) {
      console.error("Error changing password:", error);
      setPasswordMessage(error.response?.data?.error || error.response?.data || "Failed to update password.");
      setPasswordMessageType("error");
    }
  };

  return (
    <div className="settings-container">
      <div className="settings-box">
        
        <div className="settings-header">
          <h2 className="settings-title">Settings</h2>
          <img src="/assets/images/logo/PETMATE LOGO.png" alt="PetMate Logo" />
        </div>

        <div className="button-group">
          <button
            className={`tab-btn ${activeTab === "details" ? "active" : ""}`}
            onClick={() => setActiveTab("details")}
          >
            Account Details
          </button>
          <button
            className={`tab-btn ${activeTab === "password" ? "active" : ""}`}
            onClick={() => setActiveTab("password")}
          >
            Change Password
          </button>
        </div>

        <div className="tab-content">
          {activeTab === "details" ? (
            <div className="details-section">
              <h3>Client Details</h3>
              <p>
                <strong>Name:</strong>{" "}
                {userFirstName || userMiddleName || userLastName
                  ? `${userFirstName}${userMiddleName ? " " + userMiddleName : ""}${userLastName ? " " + userLastName : ""}`
                  : "Not available"}
              </p>
              <p>
                <strong>Email:</strong> {userEmail || "Not available"}
              </p>
              <p>
                <strong>Phone Number:</strong> {userPhoneNumber || "Not available"}
              </p>
            </div>
          ) : (
            <div className="password-section">
              <h3>Change Password</h3>
              <form onSubmit={handlePasswordChange}>
                <input
                  type="password"
                  placeholder="Current Password"
                  className="input-box"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="New Password"
                  className="input-box"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="Confirm New Password"
                  className="input-box"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
                <button type="submit" className="submit-btn">
                  Update Password
                </button>
              </form>

              {passwordMessage && (
                <p
                  className={passwordMessageType === "error" ? "error-msg" : "success-msg"}
                  style={{ marginTop: 10, color: passwordMessageType === "error" ? "crimson" : "green" }}
                >
                  {passwordMessage}
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
