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
  const [availableTimes, setAvailableTimes] = useState([]);
  const [checkingAvailability, setCheckingAvailability] = useState(false);

  const dateRef = useRef(null);

  // time slots for selection
  const timeSlots = [
    { label: "09:30 AM", value: "09:30:00" },
    { label: "10:30 AM", value: "10:30:00" },
    { label: "11:30 AM", value: "11:30:00" },
    { label: "12:30 PM", value: "12:30:00" },
    { label: "01:30 PM", value: "13:30:00" },
    { label: "02:30 PM", value: "14:30:00" },
    { label: "03:30 PM", value: "15:30:00" },
    { label: "04:30 PM", value: "16:30:00" },
    { label: "05:30 PM", value: "17:30:00" },
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

  // Check availability when date changes
  useEffect(() => {
    if (form.preferredDate) {
      checkAllTimeSlots(form.preferredDate);
    } else {
      setAvailableTimes([]);
    }
  }, [form.preferredDate]);

  // Check all time slots for availability
  const checkAllTimeSlots = async (date) => {
    setCheckingAvailability(true);

    try {
      const updatedSlots = await Promise.all(
        timeSlots.map(async (slot) => {
          const isAvailable = await checkTimeSlotAvailability(date, slot.value);
          return {
            ...slot,
            available: isAvailable
          };
        })
      );

      setAvailableTimes(updatedSlots);
    } catch (error) {
      console.error("Error checking time slots:", error);
      // If error, show all as available
      setAvailableTimes(timeSlots.map(slot => ({ ...slot, available: true })));
    } finally {
      setCheckingAvailability(false);
    }
  };

  // Check single time slot availability
  const checkTimeSlotAvailability = async (date, time) => {
    try {
      const response = await fetch(`/api/check-time-slot/?date=${date}&time=${time}`, {
        credentials: "include",
        headers: { "X-CSRFToken": getCookie("csrftoken") || "" },
      });

      if (response.ok) {
        const data = await response.json();
        return data.available;
      }
      return true; // Default to available if API fails
    } catch (error) {
      console.error("Error checking time slot:", error);
      return true; // Default to available if there's an error
    }
  };

  // Date picker
  useEffect(() => {
    flatpickr(dateRef.current, {
      dateFormat: "M d, Y",
      minDate: "today",
      onChange: (selectedDates) => {
        if (selectedDates.length > 0) {
          const date = selectedDates[0];
          setForm((prev) => ({
            ...prev,
            preferredDate: date.toLocaleDateString("en-CA"),
            preferredTime: "" // Reset time when date changes
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
      // Double-check availability before submitting
      const isAvailable = await checkTimeSlotAvailability(form.preferredDate, form.preferredTime);
      if (!isAvailable) {
        alert("This time slot is no longer available. Please choose another time.");
        setSubmitting(false);
        return;
      }

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
        setAvailableTimes([]); // Reset availability

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
          <option value="Grooming">Grooming</option>
          <option value="Check-up">Check-up</option>
          <option value="Consultations">Consultations</option>
          <option value="Deworming">Deworming</option>
          <option value="Tick & Flea Prevention">Tick & Flea Prevention</option>
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
          disabled={!form.preferredDate || checkingAvailability}
        >
          <option value="" disabled>
            {checkingAvailability ? "Checking availability..." : "Select Time"}
          </option>
          {availableTimes.map((slot, index) => (
            <option
              key={index}
              value={slot.value}
              disabled={!slot.available}
              style={{
                color: slot.available ? 'inherit' : '#999',
                fontStyle: slot.available ? 'normal' : 'italic'
              }}
            >
              {slot.label} {!slot.available && '(FULL)'}
            </option>
          ))}
        </select>
      </div>

      {availableTimes.length > 0 && availableTimes.every(slot => !slot.available) && (
        <div style={{
          color: '#ff6b6b',
          textAlign: 'center',
          margin: '10px 0',
          fontSize: '14px',
          fontWeight: 'bold'
        }}>
          All time slots are fully booked for this date. Please choose another date.
        </div>
      )}

      <div>
        <button
          type="submit"
          className="confirmbtn"
          disabled={submitting || checkingAvailability}
        >
          {submitting ? "Setting Appointment..." : "CONFIRM"}
        </button>
      </div>

    </form>
  );
}