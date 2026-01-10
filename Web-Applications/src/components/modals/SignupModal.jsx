import provinces from "../../data/provinces.json";
import cities from "../../data/cities.json";
import barangays from "../../data/barangays.json";
import React, { useState, useEffect, useRef } from "react";
import ReCAPTCHA from "react-google-recaptcha";
import { getCookie } from "../../utils/csrf";
import { apiFetch } from "../../config/api";
import ClaimAccountModal from "./ClaimAccountModal";

function SignupModal({ onClose, onOpenLogin, visible }) {
  if (!visible) return null;
  const [selectedProvince, setSelectedProvince] = useState("");
  const [selectedCity, setSelectedCity] = useState("");

  const filteredCities = cities.filter(city => city.prov_code === selectedProvince);
  const filteredBarangays = barangays.filter(brgy => brgy.mun_code === selectedCity);

  const [phoneNum, setPhoneNum] = useState("");   // primary phone number
  const [phoneNum2, setPhoneNum2] = useState(""); // secondary phone number
  const [showClaimModal, setShowClaimModal] = useState(false);
  const [verificationData, setVerificationData] = useState(null);
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [passwordValid, setPasswordValid] = useState({
    length: false,
    uppercase: false,
    lowercase: false,
    number: false,
    special: false
  });

  const [passwordStrength, setPasswordStrength] = useState(0);
  const [passwordsMatch, setPasswordsMatch] = useState(true);

  const recaptchaRef = useRef(null);
  const [pendingSignupData, setPendingSignupData] = useState(null);

  const RECAPTCHA_SITE_KEY =
    (typeof import.meta !== "undefined" &&
      import.meta.env &&
      import.meta.env.VITE_RECAPTCHA_SITE_KEY) ||
    "";

  console.log(
    "reCAPTCHA key:",
    RECAPTCHA_SITE_KEY ? "SET" : "MISSING"
  );

  useEffect(() => {
    let score = 0;
    if (/[A-Z]/.test(password)) score += 20;
    if (/[0-9]/.test(password)) score += 20;
    if (password.length >= 8) score += 20;
    if (/[!@#$%^&*()_\-+=\[\]{};:'",.<>\/?\\|`~]/.test(password)) score += 20;
    if (/[a-z]/.test(password)) score += 20;
    
    // Only show full strength if ALL requirements are met
    const allValid = password.length >= 8 && /[A-Z]/.test(password) && /[a-z]/.test(password) && /[0-9]/.test(password) && /[!@#$%^&*()_\-+=\[\]{};:'",.<>\/?\\|`~]/.test(password);
    setPasswordStrength(allValid ? 100 : score);
  }, [password]);

  useEffect(() => {
    setPasswordsMatch(password === confirmPassword);
  }, [password, confirmPassword]);

  const validatePassword = (pwd) => {
    setPasswordValid({
      length: pwd.length >= 8,
      uppercase: /[A-Z]/.test(pwd),
      lowercase: /[a-z]/.test(pwd),
      number: /\d/.test(pwd),
      // allow a wide set of commonly used special characters including underscore and hyphen
      special: /[!@#$%^&*()_\-+=\[\]{};:'",.<>\/?\\|`~]/.test(pwd)
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!RECAPTCHA_SITE_KEY) {
      alert("Missing reCAPTCHA site key. Check Web-Applications/.env and restart dev server.");
      return;
    }

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    data.email = data.email.toLowerCase().trim();

    // Trigger reCAPTCHA on CREATE ACCOUNT
    setPendingSignupData(data);
    recaptchaRef.current?.execute();
  };

  const onRecaptchaChange = (token) => {
    if (!token) return;

    const data = pendingSignupData;
    setPendingSignupData(null);

    if (!data) return;

    (async () => {
      try {
        const checkRes = await apiFetch("/api/check-existing-patient/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken") || "",
          },
          body: JSON.stringify({ email: data.email }),
        });

        const checkData = await checkRes.json();

        if (checkData.has_account) {
          alert("An account already exists with this email. Please login instead.");
          onClose();
          onOpenLogin();
          return;
        }

        if (checkData.has_existing_record) {
          setVerificationData(checkData);
          setShowClaimModal(true);
          return;
        }

        proceedWithRegistration(data, token);
      } catch (err) {
        console.error("Error checking existing patient:", err);
        proceedWithRegistration(data, token);
      } finally {
        recaptchaRef.current?.reset();
      }
    })();
  };

  const proceedWithRegistration = async (data, recaptchaToken) => {
    // Process phone numbers
    data.phoneNum = "+63" + data.phoneNum;
    if (data.phoneNum2 && data.phoneNum2.trim() !== "") {
      data.phoneNum2 = "+63" + data.phoneNum2;
    }
    
    // Password validation
    if (data.password !== data.confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    
    const allValid = Object.values(passwordValid).every(v => v === true);
    if (!allValid) {
      alert("Your password does not meet the required strength.");
      return;
    }
    
    data.recaptchaToken = recaptchaToken;

    // Remove confirmPassword before sending
    const { confirmPassword, ...submitData } = data;
    
    try {
      const res = await apiFetch('/api/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') || ''
        },
        body: JSON.stringify(submitData)
      });
      
      const text = await res.text();
      let data = {};
      try {
        data = text ? JSON.parse(text) : {};
      } catch {
        data = { error: text || res.statusText };
      }
      
      if (!res.ok) throw new Error(data.error || res.statusText || 'Register failed');
      
      alert('Account created successfully!');
      onClose();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleClaimSuccess = () => {
    setShowClaimModal(false);
    setVerificationData(null);
    onClose();
    alert('Account created successfully! Your existing records have been linked.');
  };


  // Helper function to get province name by code
  const getProvinceName = (code) => {
    return provinces.find(prov => prov.prov_code === code)?.name || "";
  };

  // Helper function to get city name by code
  const getCityName = (code) => {
    return cities.find(city => city.mun_code === code)?.name || "";
  };

  const handlePhoneChange = (setter) => (e) => {
    let digits = e.target.value.replace(/\D/g, ""); // keep digits only
    digits = digits.replace(/^0+/, ""); // remove leading zeros
    setter(digits.slice(0, 10)); // enforce max length
  };

  return (
    <>
      {!showClaimModal ? (
      <div className="modal">
        <div className="modal-content signupModal" onClick={(e) => e.stopPropagation()}>
          <span className="close" onClick={onClose}>
            &times;
          </span>
          <div className="login-container">
            <h2>Create Account</h2>
            <form id="signupForm" onSubmit={handleSubmit}>

              <div className="form-row owner-details">
                <div className="form-group">
                  <label htmlFor="signupFirstName">First Name</label>
                  <input type="text" id="signupFirstName" name="firstName" placeholder="Ex: Juan" required />
                </div>

                <div className="form-group">
                  <label htmlFor="signupLastName">Last Name</label>
                  <input type="text" id="signupLastName" name="lastName" placeholder="Ex: Cruz" required />
                </div>

                <div className="form-group">
                  <label htmlFor="signupMiddleName">Middle Name</label>
                  <input type="text" id="signupMiddleName" name="middleName" placeholder="Optional" />
                </div>
              </div>

              <div className="owner-contact">
                <div className="form-group">
                  <label htmlFor="signupEmail">Phone number</label>
                  <div className="phone-input">
                    <span className="prefix">+63</span>
                    <input
                      type="text"
                      id="phoneNum"
                      name="phoneNum"
                      required
                      placeholder="9123456789"
                      value={phoneNum}
                      onChange={handlePhoneChange(setPhoneNum)}
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="phoneNum2">Secondary Phone (Optional)</label>
                  <div className="phone-input">
                    <span className="prefix">+63</span>
                    <input
                      type="text"
                      id="phoneNum2"
                      name="phoneNum2"
                      placeholder="9123456789"
                      value={phoneNum2}
                      onChange={handlePhoneChange(setPhoneNum2)}
                    />
                  </div>
                </div>
              </div>

              <p className="addressTitle" >Address</p>

              <div className="form-row address1">
                <div className="form-group">
                  <label>Province</label>
                  <select
                    className="addressSelect"
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
                  {/* Hidden input to send province name */}
                  <input
                    type="hidden"
                    name="province"
                    value={getProvinceName(selectedProvince)}
                  />
                </div>

                <div className="form-group">
                  <label>City/Municipality</label>
                  <select
                    className="addressSelect"
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
                  {/* Hidden input to send city name */}
                  <input
                    type="hidden"
                    name="city"
                    value={getCityName(selectedCity)}
                  />
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

              <div className="form-group address2">
                <label htmlFor="signupDetailedAdd">Detailed Address</label>
                <input type="text" id="signupDetailedAdd" name="detailedAdd" placeholder="Subdivision/Ph/Blk-L/Street" required />
              </div>

              <div className="form-group email-row">
                <label htmlFor="signupEmail">Email</label>
                <input type="email" id="signupEmail" name="email" placeholder="Ex: Juan_Cruz@gmail.com" required />
              </div>

              <div className="form-group password-pair">
                <div className="form-group">
                  <label htmlFor="signupPassword">Password</label>
                  <div className="password-input-wrapper">
                    <input
                      id="signupPassword"
                      type={showPassword ? "text" : "password"}
                      name="password"
                      value={password}
                      onChange={(e) => {
                        const v = e.target.value;
                        setPassword(v);
                        validatePassword(v);
                      }}
                      required
                    />
                    <img
                      src={showPassword ? "/assets/icons/hide.png" : "/assets/icons/eye.png"}
                      alt={showPassword ? "Hide Password" : "Show Password"}
                      className="toggle-password-icon"
                      onClick={() => setShowPassword(!showPassword)}
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="signupConfirm">Confirm Password</label>
                    <div className="password-input-wrapper">
                      <input
                        id="signupConfirm"
                        type={showConfirmPassword ? "text" : "password"}
                        name="confirmPassword"
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

                  <div className="password-strength-wrapper">
                    <div className="password-bar" aria-hidden>
                      <div
                        className={
                          "password-bar-fill " +
                          (passwordStrength === 100 ? "fill-strong" :
                            passwordStrength >= 60 ? "fill-medium" :
                              passwordStrength >= 30 ? "fill-weak" :
                                "fill-very-weak")
                        }
                        style={{ width: `${passwordStrength}%` }}
                      />
                    </div>
                    <div className="password-label">
                      {passwordStrength === 100 ? "Strong password." : passwordStrength >= 60 ? "Medium password." : "Weak password. Must contain:"}
                    </div>

                    <div className={`password-match-indicator ${passwordsMatch && confirmPassword ? "match" : confirmPassword && !passwordsMatch ? "no-match" : ""}`}>
                      {confirmPassword && (
                        <>
                          <span className="icon">{passwordsMatch ? "✔" : "✖"}</span>
                          {passwordsMatch ? "Passwords match" : "Passwords do not match"}
                        </>
                      )}
                    </div>

                    <ul className="password-checklist vertical">
                      <li className={passwordValid.uppercase ? "valid" : ""}><span className="icon">{passwordValid.uppercase ? "✔" : "✖"}</span> At least 1 uppercase</li>
                      <li className={passwordValid.number ? "valid" : ""}><span className="icon">{passwordValid.number ? "✔" : "✖"}</span> At least 1 number</li>
                      <li className={passwordValid.length ? "valid" : ""}><span className="icon">{passwordValid.length ? "✔" : "✖"}</span> At least 8 characters</li>
                      <li className={passwordValid.special ? "valid" : ""}><span className="icon">{passwordValid.special ? "✔" : "✖"}</span> Special character</li>
                    </ul>
                  </div>
                </div>


              </div>

              <button type="submit" className="login-submit-btn">
                CREATE ACCOUNT
              </button>

              {/* Avoid crash when sitekey is missing */}
              {RECAPTCHA_SITE_KEY ? (
                <ReCAPTCHA
                  ref={recaptchaRef}
                  sitekey={RECAPTCHA_SITE_KEY}
                  size="invisible"
                  onChange={onRecaptchaChange}
                />
              ) : null}

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
      ) : (
        <ClaimAccountModal
          visible={showClaimModal}
          verificationData={verificationData}
          onClose={() => {
            setShowClaimModal(false);
            setVerificationData(null);
          }}
          onSuccess={handleClaimSuccess}
        />
      )}
    </>
  );
}

export default SignupModal;