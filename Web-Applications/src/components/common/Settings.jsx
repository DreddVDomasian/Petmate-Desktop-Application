import React, { useState, useEffect } from "react";
import axios from "axios";

export default function Settings() {
  const [activeTab, setActiveTab] = useState("details");

  const [userFirstName, setUserFirstName] = useState('');
  const [userMiddleName, setUserMiddleName] = useState('');
  const [userLastName, setUserLastName] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const [userPhoneNumber, setUserPhoneNumber] = useState('');

  // debug / error states
  const [rawProfile, setRawProfile] = useState(null);
  const [fetchError, setFetchError] = useState(null);

  // small helper to read cookie by name
  const getCookie = (name) => {
    const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return m ? decodeURIComponent(m.pop()) : null;
  };

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        // build headers: include Bearer token if you store it, and CSRF if present
        const token = localStorage.getItem("token"); // adjust key if different
        const csrf = getCookie("csrftoken") || getCookie("csrf") || getCookie("XSRF-TOKEN");

        const headers = {};
        if (token) headers["Authorization"] = `Bearer ${token}`;
        if (csrf) headers["X-CSRFToken"] = csrf;

        const res = await axios.get("http://localhost:8000/api/user/profile/", { // changed 127.0.0.1 -> localhost
          withCredentials: true,
          headers,
        });
        console.log("document.cookie:", document.cookie);
        console.log("Profile Data:", res.data);
        setRawProfile(res.data);
        setFetchError(null);

        // Normalize different possible API response shapes:
        let data = res.data || {};
        if (data.current_user) data = data.current_user;
        else if (data.user) data = data.user;
        else if (data.data) data = data.data;

        const firstName = data.first_name || data.firstName || '';
        const middleName =
          data.middle_name ||
          data.middleName ||
          (data.patient_profile && (data.patient_profile.middle_name || data.patient_profile.middleName)) ||
          '';
        const lastName = data.last_name || data.lastName || '';
        const email = data.email || data.mail || '';
        let phone = '';
        if (data.patient_profile) {
          phone = data.patient_profile.phoneNumber || data.patient_profile.phone || '';
        }
        phone = phone || data.phoneNumber || data.phone || '';

        setUserFirstName(firstName);
        setUserMiddleName(middleName);
        setUserLastName(lastName);
        setUserEmail(email);
        setUserPhoneNumber(phone);
      } catch (err) {
        console.error("Failed to fetch profile:", err);
        // capture response if present
        const info = {
          message: err.message,
          status: err.response?.status,
          data: err.response?.data,
          headers: err.response?.headers,
        };
        setFetchError(info);
        setRawProfile(err.response?.data || null);
      }
    };
    fetchProfile();
  }, []);

  return (
    <div className="settings-container">
      <div className="settings-box">
        <h2 className="settings-title">Settings</h2>

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
              {fetchError && (
                <div style={{ color: "crimson", marginBottom: 12 }}>
                  Error fetching profile:
                  <div>Status: {fetchError.status || "n/a"}</div>
                  <div>Message: {fetchError.message}</div>
                </div>
              )}
              <p>
                <strong>Name:</strong>{" "}
                {(userFirstName || userMiddleName || userLastName)
                  ? `${userFirstName}${userMiddleName ? ' ' + userMiddleName : ''}${userLastName ? ' ' + userLastName : ''}`
                  : "Not available"}
              </p>
              <p><strong>Email:</strong> {userEmail || "Not available"}</p>
              <p><strong>Phone Number:</strong> {userPhoneNumber || "Not available"}</p>

              {/* ETO ANG GAMIT KO PANG DEBUG HEHEHE
                <div style={{ marginTop: 12 }}>
                  <strong>Debug: raw profile JSON / response</strong>
                  <pre style={{ maxHeight: 240, overflow: 'auto', background: '#f6f8fa', padding: 8 }}>
                    {rawProfile ? JSON.stringify(rawProfile, null, 2) : 'No response body'}
                  </pre>
                </div>*/}

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
