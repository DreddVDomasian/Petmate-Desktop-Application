import React, { useState, useEffect, useRef } from "react";
import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";

export default function SetAppointment() {
  const [form, setForm] = useState({
    pet: "",
    service: "",
    preferredDate: "",
    preferredTime: "",
  });

  const dateRef = useRef(null);
  const timeRef = useRef(null);

  useEffect(() => {
    // Date Picker
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

    // Time Picker
    flatpickr(timeRef.current, {
      enableTime: true,
      noCalendar: true,
      dateFormat: "h:i K",
      time_24hr: false,
      onChange: (selectedDates) => {
        if (selectedDates.length > 0) {
          const time = selectedDates[0];
          const formattedTime = time.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          });
          setForm((prev) => ({
            ...prev,
            preferredTime: formattedTime,
          }));
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
    alert("Appointment Saved! (UI only)");
  };

  return (
    <form className="appointment-form">
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
        >
          <option value="" disabled>Select Pet</option>
          <option value="Buddy">Buddy</option>
          <option value="Milo">Milo</option>
        </select>

        <select
          name="service"
          required
          value={form.service}
          onChange={handleChange}
        >
          <option value="" disabled>Select Service</option>
          <option value="Grooming">Grooming</option>
          <option value="Vet Visit">Vet Visit</option>
          <option value="Walking">Walking</option>
        </select>
      </div>

      <h2>Preferred Schedule</h2>
      <div className="form-row">
        <input
          ref={dateRef}
          type="text"
          placeholder="Preferred Date"
          readOnly
        />
        <input
          ref={timeRef}
          type="text"
          placeholder="Preferred Time"
          readOnly
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