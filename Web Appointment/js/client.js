document.addEventListener("DOMContentLoaded", () => {
  const clientForm = document.querySelector(".client-form");
  const petForm = document.querySelector(".pet-form");
  const appointmentForm = document.querySelector(".appointment-form");

  // Navigation buttons
  const addPetsBtn = document.getElementById("addpets");
  const viewPetsBtn = document.getElementById("viewpets");
  const addClientBtn = document.getElementById("addclient");
  const appointmentsBtn = document.getElementById("appointments");
  const settingsBtn = document.getElementById("settings");
  const logoutBtn = document.getElementById("logout");

  // Navigation items for active state
  const navItems = document.querySelectorAll(".nav-item");

  // Hide all forms initially
  function hideAllForms() {
    if (clientForm) clientForm.style.display = "none";
    if (petForm) petForm.style.display = "none";
    if (appointmentForm) appointmentForm.style.display = "none";
  }

  // Remove active class from all nav items
  function removeActiveClass() {
    navItems.forEach(item => item.classList.remove("active"));
  }

  // Set active navigation item
  function setActiveNav(activeBtn) {
    removeActiveClass();
    if (activeBtn) {
      activeBtn.closest(".nav-item").classList.add("active");
    }
  }

  // Initialize - show client form by default
  hideAllForms();
  if (clientForm) {
    clientForm.style.display = "block";
  }
  if (addClientBtn) {
    setActiveNav(addClientBtn);
  }

  // Show Pet form
  if (addPetsBtn) {
    addPetsBtn.addEventListener("click", (e) => {
      e.preventDefault();
      hideAllForms();
      if (petForm) {
        petForm.style.display = "block";
      }
      setActiveNav(addPetsBtn);
    });
  }

  // Show Client form (Customer Details)
  if (addClientBtn) {
    addClientBtn.addEventListener("click", (e) => {
      e.preventDefault();
      hideAllForms();
      if (clientForm) {
        clientForm.style.display = "block";
      }
      setActiveNav(addClientBtn);
    });
  }

  // View Pets (placeholder)
  if (viewPetsBtn) {
    viewPetsBtn.addEventListener("click", (e) => {
      e.preventDefault();
      hideAllForms();
      // TODO: Create and show pets list view
      alert("View Pets feature coming soon!");
      setActiveNav(viewPetsBtn);
    });
  }

  // View Appointments (placeholder)
  if (appointmentsBtn) {
    appointmentsBtn.addEventListener("click", (e) => {
      e.preventDefault();
      hideAllForms();
      // TODO: Create and show appointments view
      alert("View Appointments feature coming soon!");
      setActiveNav(appointmentsBtn);
    });
  }

  // Settings (placeholder)
  if (settingsBtn) {
    settingsBtn.addEventListener("click", (e) => {
      e.preventDefault();
      hideAllForms();
      // TODO: Create and show settings form
      alert("Settings feature coming soon!");
      setActiveNav(settingsBtn);
    });
  }

  // Logout
  if (logoutBtn) {
    logoutBtn.addEventListener("click", (e) => {
      e.preventDefault();
      if (confirm("Are you sure you want to logout?")) {
        // Clear any stored data
        localStorage.clear();
        sessionStorage.clear();
        
        // Redirect to login/home page
        window.location.href = "index.html";
      }
    });
  }

  // Form submissions
  if (clientForm) {
    clientForm.addEventListener("submit", (e) => {
      e.preventDefault();
      // TODO: Handle client form submission
      alert("Customer details saved successfully!");
    });
  }

  if (petForm) {
    petForm.addEventListener("submit", (e) => {
      e.preventDefault();
      // TODO: Handle pet form submission
      alert("Pet details saved successfully!");
    });
  }

  if (appointmentForm) {
    appointmentForm.addEventListener("submit", (e) => {
      e.preventDefault();
      // TODO: Handle appointment form submission
      alert("Appointment saved successfully!");
    });
  }
});
