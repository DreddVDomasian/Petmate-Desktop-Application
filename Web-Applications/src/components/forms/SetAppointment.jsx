import React, { useState, useEffect, useRef } from "react";
import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";
import { getCookie } from "../../utils/csrf";

export default function SetAppointment() {
  const [form, setForm] = useState({
    pet: "",
    service: "",
    preferredDate: "",
    preferredTime: "",
  });

  const [pets, setPets] = useState([]);       //  store pets here
  const [loadingPets, setLoadingPets] = useState(true);

  const dateRef = useRef(null);
  const timeRef = useRef(null);

  // ✅ Fetch pets from Django backend
  useEffect(() => {
    const fetchPets = async () => {
      try {
        const res = await fetch("/api/pets/", {
          credentials: "include",
          headers: {
            "X-CSRFToken": getCookie("csrftoken") || "",
          },
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

  // ✅ Date & time pickers
  useEffect(() => {
    flatpickr(dateRef.current, {
      dateFormat: "M d, Y",
      minDate: "today",
      onChange: (dates) => {
        if (dates.length > 0) {
          const date = dates[0].toISOString().split("T")[0];
          setForm((prev) => ({ ...prev, preferredDate: date }));
        }
      },
    });

    flatpickr(timeRef.current, {
      enableTime: true,
      noCalendar: true,
      dateFormat: "h:i K",
      time_24hr: false,
      onChange: (dates) => {
        if (dates.length > 0) {
          const time = dates[0].toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          });
          setForm((prev) => ({ ...prev, preferredTime: time }));
        }
      },
    });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Appointment Data:", form);
    alert("Appointment set successfully!"); //wala pang backend integration
  };

  //  dynamic pet list
  return (
    <form className="appointment-form" onSubmit={handleSubmit}>
      <div className="form-header">
        <h2>Set Appointment</h2>
      </div>

      <h2>Appointment Details</h2>

      <div className="form-row">
        {/* --- dito yung drop down na dynamic--- */}
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
            <option key={pet.id} value={pet.petName}>
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
          <option value="vaccination">Vaccination</option>
          <option value="checkup">Check-up</option>
          <option value="surgery">Surgery</option>
          <option value="consultations">Consultations</option>
          <option value="deworming">Deworming</option>
        </select>
      </div>

      <h2>Preferred Schedule</h2>
      <div className="form-row">
        <input ref={dateRef} type="text" placeholder="Preferred Date" readOnly />
        <input ref={timeRef} type="text" placeholder="Preferred Time" readOnly />
      </div>

      <div>
        <button type="submit" className="confirmbtn">
          CONFIRM
        </button>
      </div>
    </form>
  );
}
