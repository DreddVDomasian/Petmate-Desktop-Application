document.addEventListener("DOMContentLoaded", () => {
  const clientForm = document.querySelector(".client-form");
  const petForm = document.querySelector(".pet-form");

  const addPetsBtn = document.getElementById("addpets");
  const settingsBtn = document.getElementById("settings");
  const logoutBtn = document.getElementById("logout");

  // Hide pet form by default
  petForm.style.display = "none";

  // Show Pet form
  addPetsBtn.addEventListener("click", () => {
    clientForm.style.display = "none";
    petForm.style.display = "block";
  });

  // Show Client form (Customer Details)
  settingsBtn.addEventListener("click", () => {
    petForm.style.display = "none";
    clientForm.style.display = "block";
  });

  // Logout (for now just alert)
  logoutBtn.addEventListener("click", () => {
    alert("You have logged out.");
    // You can redirect to login page later:
    // window.location.href = "login.html";
  });
});
