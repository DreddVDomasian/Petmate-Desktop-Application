import { useState, useEffect } from 'react'
import PetCard from './PetCard'
import AppointmentCard from './AppointmentCard'

const TabContent = ({ 
  activeTab,
  setActiveTab,
  pets, 
  appointments, 
  onOpenModal, 
  loading, 
  onRefresh,
  onViewPetDetails,
  onViewAppointmentDetails 
}) => {
  const [selectedPet, setSelectedPet] = useState(null)
  const [selectedAppointment, setSelectedAppointment] = useState(null)
  
  // User profile state with address fields
  const [userFirstName, setUserFirstName] = useState("");
  const [userMiddleName, setUserMiddleName] = useState("");
  const [userLastName, setUserLastName] = useState("");
  const [userEmail, setUserEmail] = useState("");
  const [userPhoneNumber, setUserPhoneNumber] = useState("");
  const [userSecondaryNumber, setUserSecondaryNumber] = useState("");
  const [userProvince, setUserProvince] = useState("");
  const [userCity, setUserCity] = useState("");
  const [userBarangay, setUserBarangay] = useState("");
  const [userDetailedAddress, setUserDetailedAddress] = useState("");

  // For address dropdowns
  const [provinces, setProvinces] = useState([]);
  const [cities, setCities] = useState([]);
  const [barangays, setBarangays] = useState([]);
  const [selectedProvince, setSelectedProvince] = useState("");
  const [selectedCity, setSelectedCity] = useState("");

  // For password change
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordMessage, setPasswordMessage] = useState("");
  const [passwordMessageType, setPasswordMessageType] = useState("");
  const [isEditingProfile, setIsEditingProfile] = useState(false);

  // Helper for CSRF cookie
  const getCookie = (name) => {
    const m = document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)");
    return m ? decodeURIComponent(m.pop()) : null;
  };

  // Load address data
  useEffect(() => {
    // Load provinces, cities, barangays data
    // You can import these or fetch from your API
    import('../../data/provinces.json').then(data => setProvinces(data.default || data));
    import('../../data/cities.json').then(data => setCities(data.default || data));
    import('../../data/barangays.json').then(data => setBarangays(data.default || data));
  }, []);

  // Filter cities and barangays based on selection
  const filteredCities = cities.filter(city => city.prov_code === selectedProvince);
  const filteredBarangays = barangays.filter(brgy => brgy.mun_code === selectedCity);

  // Fetch user profile data
  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const res = await fetch("/api/user/profile/", {
          credentials: "include",
          headers: {
            "X-CSRFToken": getCookie("csrftoken") || "",
          },
        });

        if (res.ok) {
          const data = await res.json();
          setUserFirstName(data.first_name || "");
          setUserMiddleName(data.middle_name || "");
          setUserLastName(data.last_name || "");
          setUserEmail(data.email || "");
          setUserPhoneNumber(data.phoneNumber || "");
          setUserSecondaryNumber(data.SecondaryNumber || "");
          setUserProvince(data.province || "");
          setUserCity(data.city || "");
          setUserBarangay(data.barangay || "");
          setUserDetailedAddress(data.detailedAddress || "");
          
          // Set selected province/city for dropdowns
          setSelectedProvince(data.province || "");
          setSelectedCity(data.city || "");
        }
      } catch (err) {
        console.error("Failed to fetch profile:", err);
      }
    };
    
    if (activeTab === 'profile') {
      fetchProfileData();
    }
  }, [activeTab]);

  // Handle profile update with address fields
const handleProfileUpdate = async (e) => {
  e.preventDefault();
  
  if (!userFirstName.trim()) {
    alert("First name is required");
    return;
  }

  try {
    const csrf = getCookie("csrftoken");
    
    // Prepare the data
    const updateData = {
      first_name: userFirstName.trim(),
      middle_name: userMiddleName.trim(),
      last_name: userLastName.trim(),
      email: userEmail.trim(),
      phoneNumber: userPhoneNumber.trim(),
      SecondaryNumber: userSecondaryNumber.trim(),
      province: userProvince.trim(),
      city: userCity.trim(),
      barangay: userBarangay.trim(),
      detailedAddress: userDetailedAddress.trim(),
    };

    console.log("=== FRONTEND DEBUG: Sending update data ===", updateData);

    const response = await fetch("/api/user/profile/", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf,
      },
      credentials: "include",
      body: JSON.stringify(updateData),
    });

    console.log("=== FRONTEND DEBUG: Response status ===", response.status);

    if (response.ok) {
      const updatedData = await response.json();
      console.log("=== FRONTEND DEBUG: Update successful ===", updatedData);
      alert("Profile updated successfully!");
      setIsEditingProfile(false);
      
      // Update local state
      setUserFirstName(updatedData.first_name || userFirstName);
      setUserLastName(updatedData.last_name || userLastName);
      setUserEmail(updatedData.email || userEmail);
      setUserPhoneNumber(updatedData.phoneNumber || userPhoneNumber);
      setUserSecondaryNumber(updatedData.SecondaryNumber || userSecondaryNumber);
      setUserProvince(updatedData.province || userProvince);
      setUserCity(updatedData.city || userCity);
      setUserBarangay(updatedData.barangay || userBarangay);
      setUserDetailedAddress(updatedData.detailedAddress || userDetailedAddress);
    } else {
      const errorText = await response.text();
      console.log("=== FRONTEND DEBUG: Update failed ===", response.status, errorText);
      throw new Error(`Failed with status: ${response.status}`);
    }
  } catch (error) {
    console.error("Error updating profile:", error);
    alert(`Error updating profile: ${error.message}`);
  }
};

  // Password change handler from old Settings.jsx
  const handlePasswordChange = async (e) => {
    e.preventDefault();

    if (newPassword !== confirmPassword) {
      setPasswordMessage("Passwords do not match.");
      setPasswordMessageType("error");
      return;
    }

    try {
      const csrf = getCookie("csrftoken") || getCookie("csrf") || getCookie("XSRF-TOKEN");
      const headers = {};
      if (csrf) headers["X-CSRFToken"] = csrf;

      const response = await fetch("/api/web-reset-password/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...headers,
        },
        credentials: "include",
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setPasswordMessage(data.message || "Password updated successfully!");
        setPasswordMessageType("success");
        setCurrentPassword("");
        setNewPassword("");
        setConfirmPassword("");
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || errorData.detail || "Failed to update password");
      }
    } catch (error) {
      console.error("Error changing password:", error);
      setPasswordMessage(error.message || "Failed to update password.");
      setPasswordMessageType("error");
    }
  };


  // Handle pet card click - open details modal
  const handlePetClick = (pet) => {
    setSelectedPet(pet)
    if (onViewPetDetails) {
      onViewPetDetails(pet)
    }
  }

  // Handle appointment details view
  const handleAppointmentDetails = (appointment) => {
    setSelectedAppointment(appointment)
    if (onViewAppointmentDetails) {
      onViewAppointmentDetails(appointment)
    }
  }

  // Loading state component
  const LoadingState = () => (
    <div className="loading">
      <p>Loading...</p>
    </div>
  )

  // Empty state component for pets
  const EmptyPetsState = () => (
    <div className="empty-state">
      <img src="/assets/icons/dog-walking.gif" alt="No pets" className="empty-icon" />
      <h3>No Pets Yet</h3>
      <p>Add your first pet to get started</p>
      <button 
        className="btn new-btn-primary" 
        onClick={() => onOpenModal('addPet')}
        style={{ marginTop: '15px' }}
      >
        <i className="fas fa-plus"></i> Add Your First Pet
      </button>
    </div>
  )

  // Empty state component for appointments
  const EmptyAppointmentsState = () => (
    <div className="empty-state">
      <img src="/assets/icons/dog-walking.gif" alt="No appointments" className="empty-icon" />
      <h3>No Appointments Yet</h3>
      <p>Schedule your first appointment to get started</p>
      <button 
        className="btn new-btn-primary" 
        onClick={() => onOpenModal('bookAppointment')}
        style={{ marginTop: '15px' }}
      >
        <i className="fas fa-calendar-plus"></i> Book Your First Appointment
      </button>
    </div>
  )

  // Format full name
  const getFullName = () => {
    return `${userFirstName}${userMiddleName ? ' ' + userMiddleName : ''}${userLastName ? ' ' + userLastName : ''}`.trim() || 'Not available';
  };

  return (
    <>
      {/* My Pets Tab */}
      <div className={`tab-content ${activeTab === 'pets' ? 'active' : ''}`} id="pets-tab">
        <div className="profile-card">
          <h3><i className="fas fa-paw"></i> My Pets</h3>
          <p>Manage your pets' information and view their medical history.</p>
     
          <div style={{ height: '12px', marginBottom: '20px' }} />
          {loading ? (
            <LoadingState />
          ) : pets.length === 0 ? (
            <EmptyPetsState />
          ) : (
            <div className="pets-grid">
              {pets.map(pet => (
                <PetCard 
                  key={pet.id} 
                  pet={pet} 
                  onClick={() => handlePetClick(pet)}
                />
              ))}
            </div>
          )}
        </div>
      </div>
      
      {/* Appointments Tab */}
      <div className={`tab-content ${activeTab === 'appointments' ? 'active' : ''}`} id="appointments-tab">
        <div className="profile-card">
          <div className="appointment-card-header">
            <h3><i className="fas fa-calendar-alt"></i> My Appointments</h3>
            <button 
              className="btn new-btn-primary" 
              onClick={() => onOpenModal('bookAppointment')}
            >
              <i className="fas fa-calendar-plus"></i> Book New Appointment
            </button>
          </div>

          {/* Refresh Button */}
          <div style={{ marginBottom: '20px' }}>
            <button 
              className="btn" 
              onClick={onRefresh}
              disabled={loading}
            >
              <i className="fas fa-sync-alt"></i> Refresh Appointments
            </button>
          </div>

          {loading ? (
            <LoadingState />
          ) : appointments.length === 0 ? (
            <EmptyAppointmentsState />
          ) : (
            <div className="appointments-list">
              {appointments.map(appointment => (
                <AppointmentCard 
                  key={appointment.id} 
                  appointment={appointment} 
                  onViewDetails={() => handleAppointmentDetails(appointment)}
                />
              ))}
            </div>
          )}
        </div>
      </div>
      
      {/* Profile Info Tab */}
      <div className={`tab-content ${activeTab === 'profile' ? 'active' : ''}`} id="profile-tab">
        {/* Personal Information Card */}
        <div className="profile-card">
          <div className="profile-card-header">
            <h3><i className="fas fa-user"></i> Personal Information</h3>
            <button 
              className="btn new-btn-primary" 
              onClick={() => setIsEditingProfile(!isEditingProfile)}
            >
              <i className="fas fa-edit"></i> {isEditingProfile ? 'Cancel Edit' : 'Edit Profile'}
            </button>
          </div>
          
          {isEditingProfile ? (
            <form onSubmit={handleProfileUpdate}>
              <div className="profile-edit-grid">
                {/* Basic Info Row */}
                <div className="form-row">
                  <div className="form-group">
                    <label>First Name *</label>
                    <input 
                      type="text" 
                      className="form-control"
                      value={userFirstName}
                      onChange={(e) => setUserFirstName(e.target.value)}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Middle Name</label>
                    <input 
                      type="text" 
                      className="form-control"
                      value={userMiddleName}
                      onChange={(e) => setUserMiddleName(e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label>Last Name *</label>
                    <input 
                      type="text" 
                      className="form-control"
                      value={userLastName}
                      onChange={(e) => setUserLastName(e.target.value)}
                      required
                    />
                  </div>
                </div>

                {/* Contact Info Row */}
                <div className="form-row">
                  <div className="form-group">
                    <label>Email *</label>
                    <input 
                      type="email" 
                      className="form-control"
                      value={userEmail}
                      onChange={(e) => setUserEmail(e.target.value)}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Phone Number *</label>
                    <input 
                      type="tel" 
                      className="form-control"
                      value={userPhoneNumber}
                      onChange={(e) => setUserPhoneNumber(e.target.value)}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Secondary Number</label>
                    <input 
                      type="tel" 
                      className="form-control"
                      value={userSecondaryNumber}
                      onChange={(e) => setUserSecondaryNumber(e.target.value)}
                    />
                  </div>
                </div>

                {/* Address Row - Province & City */}
                <div className="form-row">
                  <div className="form-group">
                    <label>Province</label>
                    <select 
                      className="form-control"
                      value={userProvince}
                      onChange={(e) => {
                        setUserProvince(e.target.value);
                        setSelectedProvince(e.target.value);
                        setUserCity(""); // Reset city when province changes
                        setUserBarangay(""); // Reset barangay when province changes
                      }}
                    >
                      <option value="">Select Province</option>
                      {provinces.map(province => (
                        <option key={province.prov_code} value={province.prov_name}>
                          {province.prov_name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="form-group">
                    <label>City/Municipality</label>
                    <select 
                      className="form-control"
                      value={userCity}
                      onChange={(e) => {
                        setUserCity(e.target.value);
                        setSelectedCity(e.target.value);
                        setUserBarangay(""); // Reset barangay when city changes
                      }}
                      disabled={!userProvince}
                    >
                      <option value="">Select City</option>
                      {filteredCities.map(city => (
                        <option key={city.mun_code} value={city.mun_name}>
                          {city.mun_name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Barangay</label>
                    <select 
                      className="form-control"
                      value={userBarangay}
                      onChange={(e) => setUserBarangay(e.target.value)}
                      disabled={!userCity}
                    >
                      <option value="">Select Barangay</option>
                      {filteredBarangays.map(barangay => (
                        <option key={barangay.brgy_code} value={barangay.brgy_name}>
                          {barangay.brgy_name}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Detailed Address Row */}
                <div className="form-row">
                  <div className="form-group full-width">
                    <label>Detailed Address</label>
                    <input 
                      type="text" 
                      className="form-control"
                      placeholder="House number, street, subdivision, etc."
                      value={userDetailedAddress}
                      onChange={(e) => setUserDetailedAddress(e.target.value)}
                    />
                  </div>
                </div>

                <div className="form-actions">
                  <button type="submit" className="btn new-btn-primary">
                    <i className="fas fa-save"></i> Save Changes
                  </button>
                </div>
              </div>
            </form>
          ) : (
            <div className="profile-info-grid">
              <div className="info-row">
                <div className="info-item">
                  <div className="info-label">Full Name</div>
                  <div className="info-value">
                    {`${userFirstName} ${userMiddleName ? userMiddleName + ' ' : ''}${userLastName}`.trim() || 'Not available'}
                  </div>
                </div>
                <div className="info-item">
                  <div className="info-label">Email</div>
                  <div className="info-value">{userEmail || 'Not available'}</div>
                </div>
              </div>
              <div className="info-row">
                <div className="info-item">
                  <div className="info-label">Phone Number</div>
                  <div className="info-value">{userPhoneNumber || 'Not available'}</div>
                </div>
                <div className="info-item">
                  <div className="info-label">Secondary Number</div>
                  <div className="info-value">{userSecondaryNumber || 'Not available'}</div>
                </div>
              </div>
              <div className="info-row">
                <div className="info-item full-width">
                  <div className="info-label">Address</div>
                  <div className="info-value">
                    {userDetailedAddress ? `${userDetailedAddress}, ${userBarangay}, ${userCity}, ${userProvince}` : 'Not available'}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
        
        {/* Change Password Card */}
        <div className="profile-card">
          <h3><i className="fas fa-shield-alt"></i> Account Security</h3>
          <form onSubmit={handlePasswordChange}>
            <div className="profile-info">
              <div className="form-group">
                <label>Current Password</label>
                <input 
                  type="password" 
                  className="form-control"
                  placeholder="Enter current password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label>New Password</label>
                <input 
                  type="password" 
                  className="form-control"
                  placeholder="Enter new password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label>Confirm New Password</label>
                <input 
                  type="password" 
                  className="form-control"
                  placeholder="Confirm new password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>
            </div>
            
            {passwordMessage && (
              <div className={`message ${passwordMessageType === 'error' ? 'error-message' : 'success-message'}`}>
                {passwordMessage}
              </div>
            )}
            
            <button type="submit" className="btn new-btn-primary">
              <i className="fas fa-key"></i> Change Password
            </button>
          </form>
        </div>
      </div>
    </>
  )
}

export default TabContent