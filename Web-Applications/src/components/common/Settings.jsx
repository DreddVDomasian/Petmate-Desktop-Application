import React, { useState } from "react";


export default function Settings() {
  const [activeTab, setActiveTab] = useState("details");

  const [userFirstName, setUserFirstName] = useState('');

  return (
    <div className="settings-container">
      <div className="settings-box">
        <h2 className="settings-title">Settings</h2>

        {/* Buttons */}
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

        {/* Content */}
        <div className="tab-content">
          {activeTab === "details" ? (
            <div className="details-section">
              <h3>Client Details</h3>
              <p><strong>Name:</strong>{userFirstName || ' NOT CONNECTED'}</p>
              <p><strong>Email:</strong> juan@example.com</p>
              <p><strong>Contact:</strong> +63 912 345 6789</p>
            </div>
          ) : (
            <div className="password-section">
              <h3>Change Password</h3>
              <form>
                <input
                  type="password"
                  placeholder="Current Password"
                  className="input-box"
                />
                <input
                  type="password"
                  placeholder="New Password"
                  className="input-box"
                />
                <input
                  type="password"
                  placeholder="Confirm New Password"
                  className="input-box"
                />
                <button type="submit" className="submit-btn">
                  Update Password
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
