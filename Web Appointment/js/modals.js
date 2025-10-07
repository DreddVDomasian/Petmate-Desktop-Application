document.addEventListener("DOMContentLoaded", () => {
  // FOR EDIT AND DELETE PET MODALS 
  const editPet = document.getElementById("editPet");
  const petModal = document.getElementById("petModal");
  const closeModal = document.getElementById("closeModal");
  const savePetsBtn = document.getElementById("savePet")

  const deletePet = document.getElementById("deletePet");
  const deleteModal = document.getElementById("deletePetModal");
  const closeDeleteModal = document.getElementById("closeDeleteModal");
  const yesPetBtn = document.getElementById("confirmPet");
  const cancelPetBtn = document.getElementById("cancelPet");
  

  // FOR EDIT AND DELETE CLIENT MODALS 
  const editProfile = document.getElementById("editProfile");
  const clientModal = document.getElementById("clientModal");
  const closeClientModal = document.getElementById("ccloseModal");
  const saveClientsBtn = document.getElementById("saveClient");
  
  const deleteProfile = document.getElementById("deleteProfile");
  const deleteClientModal = document.getElementById("deleteClientModal");
  const closeClientDeleteModal = document.getElementById("closeClient");
  const yesClientBtn = document.getElementById("confirmClient");
  const cancelClientBtn = document.getElementById("cancelClient");

  // EDIT AND DELETE CUSTOMER'S ACCOUNT
  const editAccount = document.getElementById("editAccount");
  const accountModal = document.getElementById("clientAccount");
  const closeAccountModal = document.getElementById("closeAccount");
  const saveAccountBtn = document.getElementById("saveAccount");

  const deleteAccount = document.getElementById("deleteAccount");
  const deleteAccountModal = document.getElementById("deleteAccountModal");
  const closeAccountDeleteModal = document.getElementById("closeAccountClient");
  const yesAccountBtn = document.getElementById("confirmAccount");
  const cancelAccountBtn = document.getElementById("cancelAccount");

  flatpickr(".bday", {
    dateFormat: "m/d/Y",  // MM/DD/YYYY
    maxDate: "today"      // disable future dates
  });

  flatpickr("#prefdate", {
    dateFormat: "m/d/Y",  // MM/DD/YYYY
    minDate: "today"      // disable past dates
  });

  flatpickr("#preftime", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "h:i K" 
   });

  // ==========================
  // EDIT PET MODAL
  // ==========================
    editPet.addEventListener("click", () => {
      petModal.style.display = "block";
    });
    
    savePetsBtn.addEventListener("click", () => {
      alert("Changes saved!");
      petModal.style.display = "none";
    });

    closeModal.addEventListener("click", () => {
      petModal.style.display = "none";
    });

    window.addEventListener("click", (event) => {
      if (event.target === petModal) {
      petModal.style.display = "none";
    }
    });

  // ==========================
  // DELETE PET MODAL
  // ==========================
  deletePet.addEventListener("click", () => {
    deleteModal.style.display = "block";
  });

  closeDeleteModal.addEventListener("click", () => {
    deleteModal.style.display = "none";
  });

  window.addEventListener("click", (event) => {
    if (event.target === deleteModal) {
      deleteModal.style.display = "none";
    }
  });

  yesPetBtn.addEventListener("click", () => {
    alert("Pet deleted!");
    deleteModal.style.display = "none";
  });

  cancelPetBtn.addEventListener("click", () => {
    deleteModal.style.display = "none";
  });


    // ==========================
    // EDIT CLIENT MODAL
    // ==========================
  editProfile.addEventListener("click", () => {
    clientModal.style.display = "block";
  });
    
  saveClientsBtn.addEventListener("click", () => {
    alert("Changes saved!");
    clientModal.style.display = "none";
  });

  closeClientModal.addEventListener("click", () => {
    clientModal.style.display = "none";
  });
  window.addEventListener("click", (event) => {
    if (event.target === clientModal) {
    clientModal.style.display = "none";
    }
  });
    // ==========================
    // DELETE CLIENT MODAL
    // ==========================
  deleteProfile.addEventListener("click", () => {
    deleteClientModal.style.display = "block";
  });

  closeClientDeleteModal.addEventListener("click", () => {    
    deleteClientModal.style.display = "none";
  });
  
  window.addEventListener("click", (event) => {
    if (event.target === deleteClientModal) {
      deleteClientModal.style.display = "none";
    }
  });

  yesClientBtn.addEventListener("click", () => {  
    alert("Client deleted!");
    deleteClientModal.style.display = "none";
  });

  cancelClientBtn.addEventListener("click", () => {  
    deleteClientModal.style.display = "none";
    });


    // ==========================
    // EDIT ACCOUNT MODAL
    // ==========================
  editAccount.addEventListener("click", () => {
    accountModal.style.display = "block";
  });

  saveAccountBtn.addEventListener("click", () => {
    alert("Changes saved!");
    accountModal.style.display = "none";
  });

  closeAccountModal.addEventListener("click", () => {
    accountModal.style.display = "none";
  });

  window.addEventListener("click", (event) => {
    if (event.target === accountModal) {
      accountModal.style.display = "none";
    } 
  });


    // ==========================
    // DELETE ACCOUNT MODAL
    // ==========================
  deleteAccount.addEventListener("click", () => {
    deleteAccountModal.style.display = "block";
  });

  closeAccountDeleteModal.addEventListener("click", () => {
    deleteAccountModal.style.display = "none";
  });

  window.addEventListener("click", (event) => {
    if (event.target === deleteAccountModal) {
      deleteAccountModal.style.display = "none";
    }
  });

    yesAccountBtn.addEventListener("click", () => {
        alert("Account deleted!");
        deleteAccountModal.style.display = "none";
    });

    cancelAccountBtn.addEventListener("click", () => {
        deleteAccountModal.style.display = "none";
    });
});


