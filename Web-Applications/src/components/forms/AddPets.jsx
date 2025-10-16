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
    birthday: "",
    age: "",
    sex: "",
    remarks: "",
  });

  const birthdayRef = useRef(null);     //... na nakikita ay common for copy all old properties

  // Initialize Flatpickr once
  useEffect(() => {
    flatpickr(birthdayRef.current, {
      dateFormat: "Y-m-d",
      maxDate: "today", // disable future dates
      onChange: (selectedDates) => {
        if (selectedDates.length > 0) {
          const birthday = selectedDates[0];
          const age = calculateAge(birthday);
          setForm((prev) => ({
            ...prev,
            birthday: birthday.toISOString().split("T")[0],
            age: age.toString(),
          }));
        }
      },
    });
  }, []);

  // Function to compute age
  const calculateAge = (birthday) => {
    const today = new Date();
    let age = today.getFullYear() - birthday.getFullYear();
    const monthDiff = today.getMonth() - birthday.getMonth();
    const dayDiff = today.getDate() - birthday.getDate();

    if (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)) {
      age--;
    }
    return age >= 0 ? age : 0;
  };

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

    try {
      const res = await fetch('/api/reactpets/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') || ''
        },
        credentials: 'include',
        body: JSON.stringify(form)
      });

      const text = await res.text();
      let data = {};
      try { data = text ? JSON.parse(text) : {}; } catch (err) { data = { error: text || res.statusText }; }

      if (!res.ok) throw new Error(data.error || res.statusText || 'Save failed');

      alert('Pet saved successfully');
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
    } catch (err) {
      alert(err.message);
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
          <option value="" disabled>
            Species
          </option>
          <option value="dog">Dog</option>
          <option value="cat">Cat</option>
          <option value="others">Others</option>
        </select>
      </div>

      <h2>Other Information</h2>
      <div className="form-row">
        {/* Birthday using Flatpickr */}
        <input
          ref={birthdayRef}       // connected sa useRef() para magamit si flatpickr
          name="birthday"
          type="text"
          placeholder="Birthday"
          className="bday"
          value={form.birthday}
          readOnly
        />

        <input
          name="age"
          type="text"
          placeholder="Age (Auto)"
          required
          value={form.age}
          readOnly
        />

        <select
          name="sex"
          required
          value={form.sex}
          onChange={handleChange}
        >
          <option value="" disabled>
            Sex
          </option>
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
