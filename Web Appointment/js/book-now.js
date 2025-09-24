
// VANILA JS GINAMIT HERE HEHE



document.addEventListener('DOMContentLoaded', function() {
  // Buttons
  const continueBtn = document.querySelector('.continue-btn');
  const backBtn = document.querySelector('.back-btn');
  const continueScheduleBtn = document.querySelector('.continue-schedule-btn');
  const backScheduleBtn = document.querySelector('.back-schedule-btn');

  // Step containers
  const formStep = document.querySelector('.appointment-form');
  const scheduleStep = document.querySelector('.scheduling-step');
  const confirmationStep = document.querySelector('.confirmation-step');
  const steps = document.querySelectorAll('.step');

  // Step 1 Inputs
  const clientTypeInputs = document.querySelectorAll('input[name="clientType"]');

  // Step 2 Inputs
  const reasonSelect = document.getElementById('reason');
  const providerSelect = document.getElementById('provider');
  const dateInput = document.getElementById('appointmentDate');

  // HEADER ANIMATION
  const pageHeader = document.querySelector('.page-header');
  const logo = document.querySelector('.transition-logo');
  const loadingOverlay = document.getElementById('loadingOverlay');

  // Function to show loading screen
  function showLoading(duration = 5000) {
    loadingOverlay.style.display = 'flex';
    return new Promise(resolve => {
      setTimeout(() => {
        loadingOverlay.style.display = 'none';
        resolve();
      }, duration);
    });
  }

  // Hide loading function
  function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

  // Disable Continue buttons initially
  continueBtn.disabled = true;
  continueScheduleBtn.disabled = true;

  // Enable Continue for Step 1
  clientTypeInputs.forEach(input => {
    input.addEventListener('change', () => {
      continueBtn.disabled = false;
    });
  });

  // Validation ng Step 2 inputs
  function validateStep2() {
    if (
      reasonSelect.value &&
      providerSelect.value &&
      dateInput.value
    ) {
      continueScheduleBtn.disabled = false;
    } else {
      continueScheduleBtn.disabled = true;
    }
  }

  // Add listeners to Step 2 inputs
  reasonSelect.addEventListener('change', validateStep2);
  providerSelect.addEventListener('change', validateStep2);
  dateInput.addEventListener('input', validateStep2);

  // Flatpickr setup DATA AND TIME PICKER
  flatpickr("#appointmentDate", {
    enableTime: true,
    dateFormat: "Y-m-d h:i K",
    minDate: "today",
    minuteIncrement: 30,
    defaultHour: 9,
    defaultMinute: 0,
    inline: true,
    onChange: validateStep2 // ensure validation on date selection
  });




  // Step 1 -> Step 2
  continueBtn.addEventListener('click', async function() {
    // Show loading screen for 2 seconds
    await showLoading(2000);
    
    formStep.style.display = 'none';
    scheduleStep.style.display = 'block';
    steps[1].classList.add('active');
    window.scrollTo(0, 0);
    validateStep2(); // Ensure Step 2 button state is correct on show
  });

  // Step 2 -> Step 3
  continueScheduleBtn.addEventListener('click', async function() {
    // Show loading screen for 2 seconds
    await showLoading(2000);
    
    // Capture the selected values from Step 2
    const selectedReason = reasonSelect.value;
    const selectedProvider = providerSelect.options[providerSelect.selectedIndex].text;
    const selectedDateTime = dateInput.value;
    
    // Update the appointment summary in Step 3
    updateAppointmentSummary(selectedReason, selectedProvider, selectedDateTime);
    
    scheduleStep.style.display = 'none';
    confirmationStep.style.display = 'block';
    steps[2].classList.add('active');
    window.scrollTo(0, 0);
  });

  // Step 4: Confirmation Message
  const submitBtn = document.querySelector('.submit-btn');
  const confirmationMessage = document.querySelector('.confirmation-message');

  // Store booking ID globally
  let currentBookingId = '';

  submitBtn.addEventListener('click', async function (e) {
    e.preventDefault();

    // Show loading
    showLoading();

    // Get all form data
    const clientType = document.querySelector('input[name="clientType"]:checked')?.value;
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const emergencyContact = document.getElementById('emergencyContact').value;
    const province = document.getElementById('province').value;
    const city = document.getElementById('city').value;
    const barangay = document.getElementById('barangay').value;
    const detailedAddress = document.getElementById('detailed_address').value;
    const petName = document.getElementById('petName').value;
    const species = document.getElementById('species').value;
    const breed = document.getElementById('breed').value;
    const color = document.getElementById('color').value;
    const sex = document.getElementById('sex').value;
    const comments = document.getElementById('comments').value;
    const provider = document.getElementById('provider').value;
    const reason = document.getElementById('reason').value;
    const dateTime = document.getElementById('appointmentDate').value;

    // Validate required fields
    if (!clientType || !firstName || !lastName || !email || !phone || !petName) {
        hideLoading();
        alert('Please fill in all required fields.');
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/bookings/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                client_type: clientType,
                first_name: firstName,
                last_name: lastName,
                email: email,
                phone: phone,
                emergency_contact: emergencyContact,
                

                province: document.getElementById('province').options[document.getElementById('province').selectedIndex].text,
                city: document.getElementById('city').options[document.getElementById('city').selectedIndex].text,
                barangay: document.getElementById('barangay').options[document.getElementById('barangay').selectedIndex].text,
                detailed_address: detailedAddress,
                pet_name: petName,
                species: species,
                breed: breed,
                color: color,
                sex: sex,
                comments: comments,


                appointment_reason: reasonSelect.value,  
                provider: providerSelect.options[providerSelect.selectedIndex].text, 
                appointment_datetime: dateInput.value, 
            }),
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Booking saved successfully:", data);
            
            // Hide loading and show confirmation
            hideLoading();
            showConfirmation(data, clientType, firstName, lastName, 
                            providerSelect.options[providerSelect.selectedIndex].text, 
                            reasonSelect.value, 
                            dateInput.value,
                            petName); // sa showconfirmation function to
        } else {
            const errorData = await response.json();
            console.error('Error response:', errorData);
            alert('Failed to submit booking. Please check the console for details.');
        }
    } catch (error) {
        console.error("Error:", error);
        hideLoading();
        alert("Failed to submit booking. Please check your connection and try again.");
    }
  });

  // Function to show confirmation with all details
  function showConfirmation(data, clientType, firstName, lastName, provider, reason, dateTime, petName) {
    // Hide confirmation step and show confirmation message
    confirmationStep.style.display = 'none';
    confirmationMessage.style.display = 'block';

    // Update booking ID
    document.getElementById('booking-id-display').textContent = data.booking_id;

    // Update all other fields
    document.getElementById('client-type-display').textContent = capitalizeFirst(clientType) + ' Client';
    document.getElementById('provider-display-final').textContent = provider;
    document.getElementById('reason-display-final').textContent = capitalizeFirst(reason);
    document.getElementById('datetime-display-final').querySelector('span').textContent = formatDateTime(dateTime);
    document.getElementById('client-name-display').textContent = `${firstName} ${lastName}`;
    document.getElementById('pet-name-display').textContent = petName;

    // Scroll to top
    window.scrollTo(0, 0);
  }

  // Function to update confirmation message with dynamic data
  function updateConfirmationMessage(clientType, firstName, lastName, provider, reason, dateTime) {
    const confirmationBox = document.querySelector('.booking-confirmation-box');
    const formTitle = confirmationMessage.querySelector('.form-title');
    const formSubtitle = confirmationMessage.querySelector('.form-subtitle');
    
    // Update greeting with user's name
    formTitle.textContent = `Thanks for submitting a request`;
    formSubtitle.textContent = `We will contact you shortly to confirm your request, ${firstName}.`;
    

    // Update confirmation details
    confirmationBox.innerHTML = `
      <div class="confirmation-item">
        <label>Location:</label>
        <div class="info-box">
          <div><strong>PetMate Animal Clinic</strong></div>
          <div>NIA ROAD QUEL COMMERCIAL BUILDING, CARSADANG BAGO 2, IMUS, CAVITE</div>
        </div>
      </div>

      <div class="confirmation-item">
        <label>Client Type:</label>
        <div class="info-box">${capitalizeFirst(clientType)} Client</div>
      </div>

      <div class="confirmation-item">
        <label>Provider:</label>
        <div class="info-box">${provider}</div>
      </div>

      <div class="confirmation-item">
        <label>Reason for your visit:</label>
        <div class="info-box">${capitalizeFirst(reason)}</div>
      </div>

      <div class="confirmation-item">
        <label>Appointment Date & Time:</label>
        <div class="info-box">
          ${formatDateTime(dateTime)}
        </div>
      </div>

      <div class="confirmation-item">
        <label>Client Name:</label>
        <div class="info-box">${firstName} ${lastName}</div>
      </div>

    `;
  }

  // Function to update appointment summary
  function updateAppointmentSummary(reason, provider, dateTime) {
    // Get the appointment summary container
    const appointmentSummary = document.querySelector('.appointment-summary');
    
    // Format the date/time (you may want to customize this formatting)
    const formattedDateTime = formatDateTime(dateTime);
    
    // Update the HTML content
    appointmentSummary.innerHTML = `
      <h3>Appointment Information</h3>
      <p><strong>Location:</strong><br>Petmate Animal Clinic, Imus, Cavite</p>
      <p><strong>Provider:</strong><br>${provider}</p>
      <p><strong>Reason for Visit:</strong><br>${capitalizeFirst(reason)}</p>
      <p><strong>Appointment Date & Time:</strong><br>${formattedDateTime}</p>
    `;
  }

  // Helper function to format date/time
  function formatDateTime(dateTimeString) {
    if (!dateTimeString) return 'Not selected';
    
    try {
      const date = new Date(dateTimeString);
      const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      };
      return date.toLocaleDateString('en-US', options);
    } catch (error) {
      return dateTimeString; // Return original if formatting fails
    }
  }

  // Helper function to capitalize first letter
  function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  // Step 2 <- Back
  backBtn.addEventListener('click', function() {
    scheduleStep.style.display = 'none';
    formStep.style.display = 'block';
    steps[1].classList.remove('active');
    window.scrollTo(0, 0);
  });

  // Step 3 <- Back
  backScheduleBtn.addEventListener('click', function() {
    confirmationStep.style.display = 'none';
    scheduleStep.style.display = 'block';
    steps[2].classList.remove('active');
    window.scrollTo(0, 0);
    validateStep2(); // Re-check Step 2 when returning
  });

  // Address dropdown elements
  const provinceSelect = document.getElementById('province');
  const citySelect = document.getElementById('city');
  const barangaySelect = document.getElementById('barangay');
  
  let provincesData = [];
  let citiesData = [];
  let barangaysData = [];

  // Load JSON data
  async function loadAddressData() {
    try {
      // Load provinces
      const provincesResponse = await fetch('../data/provinces.json');
      provincesData = await provincesResponse.json();
      
      // Load cities
      const citiesResponse = await fetch('../data/cities.json');
      citiesData = await citiesResponse.json();
      
      // Load barangays
      const barangaysResponse = await fetch('../data/barangays.json');
      barangaysData = await barangaysResponse.json();
      
      populateProvinces();
    } catch (error) {
      console.error('Error loading address data:', error);
    }
  }

  // Populate provinces dropdown
function populateProvinces() {
  provinceSelect.innerHTML = '<option value="">Select Province*</option>';

  const sortedProvinces = [...provincesData].sort((a, b) => a.name.localeCompare(b.name));
  
  sortedProvinces.forEach(province => {
    const option = document.createElement('option');
    option.value = province.prov_code;
    option.textContent = province.name;
    provinceSelect.appendChild(option);
  });
}
  // Populate cities based on selected province
function populateCities(provinceCode) {
  citySelect.innerHTML = '<option value="">Select City/Municipality*</option>';
  barangaySelect.innerHTML = '<option value="">Select Barangay</option>';
  
  const filteredCities = citiesData.filter(city => city.prov_code === provinceCode);
  
  // Sort filtered cities alphabetically
  filteredCities.sort((a, b) => a.name.localeCompare(b.name));
  
  filteredCities.forEach(city => {
    const option = document.createElement('option'); // This line was missing!
    option.value = city.mun_code;
    option.textContent = city.name;
    citySelect.appendChild(option); // Now this will work correctly
  });
}

  // Populate barangays based on selected city (if you have barangay data)
function populateBarangays(cityCode) {
  barangaySelect.innerHTML = '<option value="">Select Barangay</option>';
  
  const filteredBarangays = barangaysData.filter(barangay => barangay.mun_code === cityCode);
  
  // Sort filtered barangays alphabetically
  filteredBarangays.sort((a, b) => a.name.localeCompare(b.name));
  
  filteredBarangays.forEach(barangay => {
    if (barangay.name) { // Check if name exists
      const option = document.createElement('option');
      option.value = barangay.brgy_code;
      option.textContent = barangay.name;
      barangaySelect.appendChild(option);
    }
  });
}

  // Event listeners for cascading dropdowns
  provinceSelect.addEventListener('change', function() {
    const selectedProvinceCode = this.value;
    if (selectedProvinceCode) {
      populateCities(selectedProvinceCode);
    } else {
      citySelect.innerHTML = '<option value="">Select City/Municipality*</option>';
      barangaySelect.innerHTML = '<option value="">Select Barangay</option>';
    }
  });

  citySelect.addEventListener('change', function() {
    const selectedCityCode = this.value;
    if (selectedCityCode) {
      populateBarangays(selectedCityCode);
    } else {
      barangaySelect.innerHTML = '<option value="">Select Barangay</option>';
    }
  });

  // Initialize address data
  loadAddressData();

  // Update form validation to include new fields
  function validateStep3Form() {
    const required = ['firstName', 'lastName', 'email', 'petName', 'species', 'breed', 'address', 'province', 'city', 'zipCode'];
    for (let field of required) {
      const element = document.getElementById(field);
      if (!element.value.trim()) {
        alert('Please fill in all required fields marked with *');
        return false;
      }
    }
    
    const email = document.getElementById('email').value;
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      alert('Please enter a valid email address');
      return false;
    }
    return true;
  }

  // Update confirmation modal to include complete address
  function getFullAddress() {
    const address = document.getElementById('address').value;
    const cityCode = document.getElementById('city').value;
    const provinceCode = document.getElementById('province').value;
    const zipCode = document.getElementById('zipCode').value;
    const country = document.getElementById('country').value;
    
    // Get city and province names
    const selectedCity = citiesData.find(city => city.mun_code === cityCode);
    const selectedProvince = provincesData.find(province => province.prov_code === provinceCode);
    
    const cityName = selectedCity ? selectedCity.name : '';
    const provinceName = selectedProvince ? selectedProvince.name : '';
    
    return `${address}, ${cityName}, ${provinceName} ${zipCode}, ${country}`;
  }

  // Header transition
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      pageHeader.classList.add('hide');
      logo.classList.add('pop');
    } else {
      pageHeader.classList.remove('hide');
      logo.classList.remove('pop');
    }
  });
});

// Function to copy booking ID (global scope)
function copyBookingId() {
    const bookingId = document.getElementById('booking-id-display').textContent;
    navigator.clipboard.writeText(bookingId).then(() => {
        // Show success message
        const copyBtn = document.querySelector('.copy-btn');
        const originalText = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
        copyBtn.style.background = '#4CAF50';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = '#ff8c00';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy: ', err);
        alert('Failed to copy booking ID');
    });
}







