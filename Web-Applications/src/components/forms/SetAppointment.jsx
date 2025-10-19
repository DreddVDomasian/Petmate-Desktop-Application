import React, { useState, useEffect, useRef } from "react";
import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";
import { getCookie } from "../../utils/csrf";


export default function SetAppointment({ onNewAppointment }) {
  const [form, setForm] = useState({
    pet: "", // This will store pet ID
    service: "",
    preferredDate: "",
    preferredTime: "",
  });

  const [pets, setPets] = useState([]);
  const [loadingPets, setLoadingPets] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const dateRef = useRef(null);
  const timeRef = useRef(null);


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

  // Date & time pickers
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

    flatpickr(timeRef.current, {
      enableTime: true,
      noCalendar: true,
      dateFormat: "h:i K",
      time_24hr: false,
      onChange: (selectedDates) => {
        if (selectedDates.length > 0) {
          const time = selectedDates[0];
          const hh = String(time.getHours()).padStart(2, "0");
          const mm = String(time.getMinutes()).padStart(2, "0");
          const formattedTime = `${hh}:${mm}:00`;
          setForm((prev) => ({ ...prev, preferredTime: formattedTime }));
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

      console.log("Sending appointment data:", appointmentData);

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
        const newAppointment = await res.json(); // return created appointment from backend
        alert("Appointment set successfully! Waiting for admin approval.");

        // Reset form
        setForm({
          pet: "",
          service: "",
          preferredDate: "",
          preferredTime: "",
        });

        // 🔹 Add appointment to parent state so it shows immediately
        if (onNewAppointment) {
          onNewAppointment(newAppointment);
        }
      } else {
        const errorData = await res.json();
        console.error("Failed to create appointment:", errorData);
        alert("Failed to set appointment. Please try again.");
      }
    } catch (error) {
      console.error("Error setting appointment:", error);
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
          <option value="" disabled>
            Select Service
          </option>
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
        <input ref={timeRef} type="text" placeholder="Preferred Time" readOnly />
      </div>

      <div>
        <button type="submit" className="confirmbtn" disabled={submitting}>
          {submitting ? "Setting Appointment..." : "CONFIRM"}
        </button>
      </div>
    </form>
  );
}
