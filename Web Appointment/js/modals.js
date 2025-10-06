document.addEventListener("DOMContentLoaded", () => {
  // === Elements ===
  const editPet = document.getElementById("editPet");
  const petModal = document.getElementById("petModal");
  const closeModal = document.getElementById("closeModal");

  const deletePet = document.getElementById("deletePet");
  const deleteModal = document.getElementById("deletePetModal");
  const closeDeleteModal = document.getElementById("closeDeleteModal");
  const yesBtn = document.getElementById("confirmDelete");
  const cancelBtn = document.getElementById("cancelDelete");

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
    dateFormat: "h:i K" });

  // ==========================
  // EDIT PET MODAL
  // ==========================
  editPet.addEventListener("click", () => {
    petModal.style.display = "block";
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

  yesBtn.addEventListener("click", () => {
    alert("Pet deleted!");
    deleteModal.style.display = "none";
  });

  cancelBtn.addEventListener("click", () => {
    deleteModal.style.display = "none";
  });
});
