import provinces from "../../data/provinces.json";
import cities from "../../data/cities.json";
import barangays from "../../data/barangays.json";
import React, { useState } from "react";
import { getCookie } from "../../utils/csrf";

function SignupModal({ onClose, onOpenLogin, visible }) {
  if (!visible) return null;
  const [selectedProvince, setSelectedProvince] = useState("");
  const [selectedCity, setSelectedCity] = useState("");

  const filteredCities = cities.filter(city => city.prov_code === selectedProvince);
  const filteredBarangays = barangays.filter(brgy => brgy.mun_code === selectedCity);

const handleSubmit = (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());

  if (data.password !== data.confirmPassword) {
    alert("Passwords do not match!");
    return;
  }

  // Remove confirmPassword before sending to backend
  const { confirmPassword, ...submitData } = data;

  (async () => {
    try {
      const res = await fetch('/api/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') || ''
        },
        credentials: 'include',
        body: JSON.stringify(submitData)
      });

      const text = await res.text();
      let data = {};
      try {
        data = text ? JSON.parse(text) : {};
      } catch (err) {
        data = { error: text || res.statusText };
      }

      if (!res.ok) throw new Error(data.error || res.statusText || 'Register failed');

      alert('Account created successfully!');
      onClose();
    } catch (err) {
      alert(err.message);
    }
  })();
};

  return (
    <div className="modal">
      <div className="modal-content signupModal" onClick={(e) => e.stopPropagation()}>
        <span className="close" onClick={onClose}>
          &times;
        </span>
        <div className="login-container">
          <h2>Create Account</h2>
          <form id="signupForm" onSubmit={handleSubmit}>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="signupFirstName">First Name</label>
                <input type="text" id="signupFirstName" name="firstName" required />
              </div>

              <div className="form-group">
                <label htmlFor="signupLastName">Last Name</label>
                <input type="text" id="signupLastName" name="lastName" required />
              </div>

              <div className="form-group">
                <label htmlFor="signupMiddleName">Middle Name</label>
                <input type="text" id="signupMiddleName" name="middleName" placeholder="Optional"/>
              </div>
            </div>

            <div className="form-row">

                <div className="form-group">
                  <label htmlFor="signupEmail">Phone number</label>
                  <input type="text" id="phoneNum" name="phoneNum" required />
                </div>

                <div className="form-group">
                  <label htmlFor="signupEmail">Secondary phone</label>
                  <input type="text" id="phoneNum2" name="phoneNum2" placeholder="Optional" />
                </div>
            </div>

            <p className="addressTitle" >Address</p>

            <div className="form-row">
              <div className="form-group">
                <label>Province</label>
                <select className="addressSelect"
                  name="province"
                  required
                  value={selectedProvince}
                  onChange={(e) => {
                    setSelectedProvince(e.target.value);
                    setSelectedCity(""); // reset city when selecting a new province
                  }}
                >
                  <option value="">Select Province</option>
                  {provinces.map((prov) => (
                    <option key={prov.prov_code} value={prov.prov_code}>
                      {prov.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>City/Municipality</label>
                <select className="addressSelect"
                  name="city"
                  required
                  value={selectedCity}
                  disabled={!selectedProvince}
                  onChange={(e) => setSelectedCity(e.target.value)}
                >
                  <option value="">Select City</option>
                  {filteredCities.map((city) => (
                    <option key={city.mun_code} value={city.mun_code}>
                      {city.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Barangay</label>
                <select className="addressSelect" name="barangay" required disabled={!selectedCity}>
                  <option value="">Select Barangay</option>
                  {filteredBarangays.map((brgy, index) => (
                    <option key={index} value={brgy.name}>
                      {brgy.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-group">
                <label htmlFor="signupEmail">Detailed Address</label>
                <input type="text" id="signupDetailedAdd" name="detailedAdd" placeholder="Subdivision/Ph/Blk-L/Street"  required />
            </div>

             <div className="form-group">
                 <label htmlFor="signupEmail">Email</label>
                 <input type="email" id="signupEmail" name="email" required />
            </div>

            <div className="form-row">
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
