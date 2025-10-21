import React, { useState, useEffect, useRef } from "react";
import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";
import { getCookie } from "../../utils/csrf";

export default function SetAppointment({ onNewAppointment }) {
  const [form, setForm] = useState({
    pet: "",
    service: "",
    preferredDate: "",
    preferredTime: "",
  });

  const [pets, setPets] = useState([]);
  const [loadingPets, setLoadingPets] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const dateRef = useRef(null);

  // time slots for selection
  const timeSlots = [
    { time: "09:30 AM", full: false },
    { time: "10:30 AM", full: false },
    { time: "11:30 AM", full: false },
    { time: "12:30 PM", full: false },
    { time: "01:30 PM", full: false },
    { time: "02:30 PM", full: false },
    { time: "03:30 PM", full: false },
    { time: "04:30 PM", full: false },
    { time: "05:30 PM", full: false },
  ];

  // Fetch pets
  useEffect(() => {
    const fetchPets = async () => {
      try {
        const res = await fetch("/api/pets/", {
          credentials: "include",
          headers: { "X-CSRFToken": getCookie("csrftoken") || "" },
        });
        if (res.ok) {
          const data = await res.json();
          setPets(data);
        } else {
          console.error("Failed to fetch pets");
        }
      } catch (error) {
        console.error("Error fetching pets:", error);
      } finally {
        setLoadingPets(false);
      }
    };
    fetchPets();
  }, []);

  // Date picker only (no more time picker)
  useEffect(() => {
    flatpickr(dateRef.current, {
      dateFormat: "M d, Y",
      minDate: "today",
      onChange: (selectedDates) => {
        if (selectedDates.length > 0) {
          const date = selectedDates[0];
          setForm((prev) => ({
            ...prev,
            preferredDate: date.toISOString().split("T")[0],
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
    setSubmitting(true);

    if (!form.pet || !form.service || !form.preferredDate || !form.preferredTime) {
      alert("Please fill all fields");
      setSubmitting(false);
      return;
    }

    try {
      const appointmentData = {
        pet_id: parseInt(form.pet),
        service_name: form.service,
        date: form.preferredDate,
        prefTime: form.preferredTime,
        request: "pending",
        status: "pending",
      };

      const res = await fetch("/api/walkIn/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken") || "",
        },
        body: JSON.stringify(appointmentData),
        credentials: "include",
      });

      if (res.status === 201) {
        const newAppointment = await res.json();
        alert("Appointment set successfully! Waiting for admin approval.");
        setForm({ pet: "", service: "", preferredDate: "", preferredTime: "" });

        if (onNewAppointment) {
          onNewAppointment(newAppointment);
        }
      } else {
        alert("Failed to set appointment. Please try again.");
      }
    } catch (error) {
      alert("Error setting appointment. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form className="appointment-form" onSubmit={handleSubmit}>
      <div className="form-header">
        <h2>Set Appointment</h2>
      </div>

      <h2>Appointment Details</h2>

      <div className="form-row">
        <select
          name="pet"
          required
          value={form.pet}
          onChange={handleChange}
          disabled={loadingPets}
        >
          <option value="" disabled>
            {loadingPets ? "Loading pets..." : "Select Pet"}
          </option>
          {pets.map((pet) => (
            <option key={pet.id} value={pet.id}>
              {pet.petName}
            </option>
          ))}
        </select>

        <select
          name="service"
          required
          value={form.service}
          onChange={handleChange}
        >
          <option value="" disabled>Select Service</option>
          <option value="Vaccination">Vaccination</option>
          <option value="Check-up">Check-up</option>
          <option value="Surgery">Surgery</option>
          <option value="Consultations">Consultations</option>
          <option value="Deworming">Deworming</option>
          <option value="Tick & Flea Prevention">Tick & Flea Prevention</option>
          <option value="Grooming">Grooming</option>
        </select>
      </div>

      <h2>Preferred Schedule</h2>
      <div className="form-row">
        <input ref={dateRef} type="text" placeholder="Preferred Date" readOnly />
        <select
          name="preferredTime"
          required
          value={form.preferredTime}
          onChange={handleChange}
        >
          <option value="" disabled>Select Time</option>
          {timeSlots.map((slot, index) => (
            <option key={index} value={slot.time} disabled={slot.full}>
              {slot.time} {slot.full ? "(FULL)" : ""}
            </option>
          ))}
        </select>
      </div>

      <div>
        <button type="submit" className="confirmbtn" disabled={submitting}>
          {submitting ? "Setting Appointment..." : "CONFIRM"}
        </button>
      </div>
    </form>
  );
}
