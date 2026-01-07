import { useState, useEffect, useRef } from 'react'
import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";
import { getCookie } from '../../utils/csrf';
import { apiFetch } from '../../config/api';

const AddPetModal = ({ isOpen, onClose, onPetAdded }) => {
  
  const [form, setForm] = useState({
    name: "",
    color: "",
    breed: "",
    species: "",
    customSpecies: "",
    birthday: "", 
    age: "", 
    sex: "",
    remarks: "",
  });

  const birthdayRef = useRef(null);

  
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

  
  useEffect(() => {
    if (isOpen) {
      flatpickr(birthdayRef.current, {
        dateFormat: "M d, Y", 
        maxDate: "today",
        onChange: (selectedDates) => {
          if (selectedDates.length > 0) {
            const birthday = selectedDates[0];
            const calculatedAge = calculateAge(birthday);

            setForm((prev) => ({
              ...prev,
              birthday: birthday.toLocaleDateString("en-CA"), 
              age: calculatedAge, 
            }));
          } else {
            
            setForm((prev) => ({
              ...prev,
              birthday: "",
            }));
          }
        },
      });
    }
  }, [isOpen]);

  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.birthday && !form.age.trim()) {
      alert("Please provide either Birthday or Age");
      return;
    }

    
    let speciesValue = form.species;
    if (speciesValue === "others") {
      if (!form.customSpecies.trim()) {
        alert("Please specify the species name");
        return;
      }
      speciesValue = form.customSpecies.trim();
    }

    try {
      const payload = {
        petName: form.name,
        petColor: form.color,
        breed: form.breed,
        species: speciesValue,
        birthDay: form.birthday || null,
        stored_age: form.age.trim() || null,
        sex: form.sex,
        remarks: form.remarks,
      };

      console.log("Sending payload:", payload);

      const res = await apiFetch("/api/pets/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken") || "",
        },
        body: JSON.stringify(payload),
      });

      const text = await res.text();
      let data = {};
      try {
        data = text ? JSON.parse(text) : {};
      } catch (err) {
        data = { error: text || res.statusText };
      }

      if (!res.ok) throw new Error(data.error || res.statusText || "Save failed");

      alert("Pet saved successfully");

      
      setForm({
        name: "",
        color: "",
        breed: "",
        species: "",
        customSpecies: "",
        birthday: "",
        age: "",
        sex: "",
        remarks: "",
      });

      
      if (birthdayRef.current && birthdayRef.current._flatpickr) {
        birthdayRef.current._flatpickr.clear();
      }

      
      onClose();
      if (onPetAdded) onPetAdded();
      
    } catch (err) {
      console.error("Error details:", err);
      alert(`Error: ${err.message}`);
    }
  };

  if (!isOpen) return null

  return (
    <div className="modal active" id="addPetModal">
      <div className="new-modal-content">
        <div className="new-modal-header">
          <h3 className="modal-title">Add New Pet</h3>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>
        <div className="modal-body">
          <form onSubmit={handleSubmit}>
            <div className="new-form-group">
              <label htmlFor="petName">Pet Name</label>
              <input 
                name="name"
                type="text" 
                className="form-control" 
                placeholder="Enter pet name"
                value={form.name}
                onChange={handleChange}
                required
              />
            </div>
            
            <div className="new-form-row">
              <div className="new-form-group">
                <label htmlFor="species">Species</label>
                <select 
                  name="species"
                  className="form-control"
                  value={form.species}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select Species</option>
                  <option value="dog">Dog</option>
                  <option value="cat">Cat</option>
                  <option value="others">Others</option>
                </select>
              </div>
              <div className="new-form-group">
                <label htmlFor="breed">Breed</label>
                <input 
                  name="breed"
                  type="text" 
                  className="form-control" 
                  placeholder="Enter breed"
                  value={form.breed}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            {}
            {form.species === "others" && (
              <div className="new-form-group">
                <label htmlFor="customSpecies">Specify Species</label>
                <input 
                  name="customSpecies"
                  type="text" 
                  className="form-control" 
                  placeholder="Type specific species (e.g., Hamster)"
                  value={form.customSpecies}
                  onChange={handleChange}
                  required
                />
              </div>
            )}
            
            <div className="new-form-row">
              <div className="new-form-group">
                <label htmlFor="birthday">Birthday</label>
                <input 
                  ref={birthdayRef}
                  type="text"
                  className="form-control"
                  placeholder="Birthday (Optional)"
                  readOnly
                />
              </div>
              <div className="new-form-group">
                <label htmlFor="age">Age</label>
                <input 
                  name="age"
                  type="text" 
                  className="form-control" 
                  placeholder="Age (Auto from birthday or type estimated)"
                  value={form.age}
                  onChange={handleChange}
                />
              </div>
            </div>
            
            <div className="new-form-row">
              <div className="new-form-group">
                <label htmlFor="color">Color</label>
                <input 
                  name="color"
                  type="text" 
                  className="form-control" 
                  placeholder="Enter color"
                  value={form.color}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="new-form-group">
                <label htmlFor="sex">Sex</label>
                <select 
                  name="sex"
                  className="form-control"
                  value={form.sex}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select Sex</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                </select>
              </div>
            </div>
            
            <div className="new-form-group">
              <label htmlFor="remarks">Remarks</label>
              <textarea 
                name="remarks"
                className="form-control" 
                placeholder="Any additional information about your pet" 
                rows="3"
                value={form.remarks}
                onChange={handleChange}
              ></textarea>
            </div>
            
            <div className="new-form-group modal-actions">
              <button type="submit" className="btn new-btn-primary">Add Pet</button>
              <button type="button" className="btn" onClick={onClose}>Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default AddPetModal