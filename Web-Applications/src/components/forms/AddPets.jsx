import React, { useState, useEffect, useRef } from "react";
import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";
import { getCookie } from '../../utils/csrf';

export default function AddPets({ onSubmit }) {
  const [form, setForm] = useState({
    name: "",
    color: "",
    breed: "",
    species: "",
    birthday: "", // Stores "2025-10-09" for backend
    age: "", // Calculated age OR manual age
    sex: "",
    remarks: "",
  });

  const birthdayRef = useRef(null);

  // Function to calculate age like desktop (days, weeks, months, years)
  const calculateAge = (birthday) => {
    const today = new Date();
    const birthDate = new Date(birthday);
    const days = Math.floor((today - birthDate) / (1000 * 60 * 60 * 24));

    if (days < 0) return "0 days old";

    if (days < 7) {
      return `${days} day${days !== 1 ? 's' : ''} old`;
    } else if (days < 30) {
      const weeks = Math.floor(days / 7);
      return `${weeks} week${weeks !== 1 ? 's' : ''} old`;
    } else if (days < 365) {
      const months = Math.floor(days / 30);
      return `${months} month${months !== 1 ? 's' : ''} old`;
    } else {
      const years = Math.floor(days / 365);
      return `${years} year${years !== 1 ? 's' : ''} old`;
    }
  };

  // Initialize Flatpickr once
  useEffect(() => {
    flatpickr(birthdayRef.current, {
      dateFormat: "M d, Y", // Display format like "Oct 9, 2025"
      maxDate: "today",
      onChange: (selectedDates) => {
        if (selectedDates.length > 0) {
          const birthday = selectedDates[0];
          const calculatedAge = calculateAge(birthday);

          setForm((prev) => ({
            ...prev,
            birthday: birthday.toISOString().split("T")[0], // "2025-10-09" for database
            age: calculatedAge, // Auto-fill calculated age
          }));
        } else {
          // Clear when no date selected
          setForm((prev) => ({
            ...prev,
            birthday: "",
            // Don't clear age - user might want to type estimated age
          }));
        }
      },
    });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // If parent provided onSubmit, keep that behavior
    if (onSubmit) {
      onSubmit(form);
      return;
    }

    // Validation: Either birthday OR age must be provided
    if (!form.birthday && !form.age.trim()) {
      alert("Please provide either Birthday or Age");
      return;
    }


    try {
         const payload = {
          petName: form.name,
          petColor: form.color,
          breed: form.breed,
          species: form.species,
          birthDay: form.birthday || null,
          stored_age: form.age.trim() || null,
          sex: form.sex,
          remarks: form.remarks
        };

        console.log("Sending payload:", payload);

      const res = await fetch('/api/pets/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') || ''
        },
        credentials: 'include',
        body: JSON.stringify({
          petName: form.name,
          petColor: form.color,
          breed: form.breed,
          species: form.species,
          birthDay: form.birthday || null, // Send null if empty
          stored_age: form.age.trim() || null, // Send calculated OR manual age
          sex: form.sex,
          remarks: form.remarks
        })
      });

      const text = await res.text();
      let data = {};
      try { data = text ? JSON.parse(text) : {}; } catch (err) { data = { error: text || res.statusText }; }

      if (!res.ok) throw new Error(data.error || res.statusText || 'Save failed');

      alert('Pet saved successfully');

      // Reset form
      setForm({
        name: "",
        color: "",
        breed: "",
        species: "",
        birthday: "",
        age: "",
        sex: "",
        remarks: "",
      });

      // Clear the flatpickr
      if (birthdayRef.current && birthdayRef.current._flatpickr) {
        birthdayRef.current._flatpickr.clear();
      }
    } catch (err) {
        console.error("Error details:", err);
        alert(`Error: ${err.message}`);
    }
  };

  return (
    <form className="pet-form" onSubmit={handleSubmit}>
      <div className="form-header">
        <h2>Pet Details</h2>
      </div>

      <h2>Basic Information</h2>
      <div className="form-row">
        <input
          name="name"
          type="text"
          placeholder="Pet name"
          required
          value={form.name}
          onChange={handleChange}
        />
        <input
          name="color"
          type="text"
          placeholder="Color"
          required
          value={form.color}
          onChange={handleChange}
        />
      </div>

      <div className="form-row">
        <input
          name="breed"
          type="text"
          placeholder="Breed"
          required
          value={form.breed}
          onChange={handleChange}
        />
        <select
          name="species"
          required
          value={form.species}
          onChange={handleChange}
        >
          <option value="" disabled>Species</option>
          <option value="dog">Dog</option>
          <option value="cat">Cat</option>
          <option value="others">Others</option>
        </select>
      </div>

      <h2>Other Information</h2>
      <div className="form-row">
        {/* Birthday - Optional */}
        <input
          ref={birthdayRef}
          type="text"
          placeholder="Birthday (Optional)"
          className="bday"
          value={form.birthday ? new Date(form.birthday).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
          }) : ""}
          readOnly
        />

        {/* Age - Auto-calculated OR manual input */}
        <input
          name="age"
          type="text"
          placeholder="Age (Auto from birthday or type estimated)"
          value={form.age}
          onChange={handleChange}
        />

        <select
          name="sex"
          required
          value={form.sex}
          onChange={handleChange}
        >
          <option value="" disabled>Sex</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
        </select>

        <input
          name="remarks"
          type="text"
          placeholder="Remarks (Optional)"
          value={form.remarks}
          onChange={handleChange}
        />
      </div>

      <div>
        <button type="submit" className="confirmbtn">
          CONFIRM
        </button>
      </div>
    </form>
  );
}