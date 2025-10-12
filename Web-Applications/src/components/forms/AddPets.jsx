import React, { useState } from "react";

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

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSubmit) {
      onSubmit(form);
    } else {
      // fallback: log and clear form
      console.log("Pet form submitted:", form);
      alert("Pet details saved.");
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
        <input
          name="birthday"
          type="date"
          placeholder="Birthday"
          className="bday"
          value={form.birthday}
          onChange={handleChange}
        />
        <input
          name="age"
          type="text"
          placeholder="Age (Estimated)"
          required
          value={form.age}
          onChange={handleChange}
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