import { useState, useEffect, useRef } from "react";
import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";
import { getCookie } from '../../utils/csrf';

const BookAppointmentModal = ({ isOpen, onClose, onAppointmentBooked }) => {
  // COPY STATE FROM OLD SetAppointment.jsx
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

  // COPY timeSlots FROM OLD SetAppointment.jsx
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

  // COPY fetchPets FROM OLD SetAppointment.jsx
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
    
    if (isOpen) {
      fetchPets();
    }
  }, [isOpen]);

  // COPY checkAllTimeSlots FROM OLD SetAppointment.jsx
  const checkAllTimeSlots = async (date) => {
    setCheckingAvailability(true);

    try {
      const updatedSlots = await Promise.all(
        timeSlots.map(async (slot) => {
          const slotDetails = await checkTimeSlotAvailability(date, slot.value);
          return {
            ...slot,
            available: slotDetails.available,
            isPast: slotDetails.is_past,
            isFull: slotDetails.is_full,
            message: slotDetails.message
          };
        })
      );

      setAvailableTimes(updatedSlots);
    } catch (error) {
      console.error("Error checking time slots:", error);
      // If error, show all as available
      setAvailableTimes(timeSlots.map(slot => ({
        ...slot,
        available: true,
        isPast: false,
        isFull: false,
        message: 'Available'
      })));
    } finally {
      setCheckingAvailability(false);
    }
  };

  // COPY checkTimeSlotAvailability FROM OLD SetAppointment.jsx
  const checkTimeSlotAvailability = async (date, time) => {
    try {
      const response = await fetch(`/api/check-time-slot/?date=${date}&time=${time}`, {
        credentials: "include",
        headers: { "X-CSRFToken": getCookie("csrftoken") || "" },
      });

      if (response.ok) {
        const data = await response.json();
        return data;
      }
      return {
        available: true,
        is_past: false,
        is_full: false,
        message: 'Available'
      };
    } catch (error) {
      console.error("Error checking time slot:", error);
      return {
        available: true,
        is_past: false,
        is_full: false,
        message: 'Available'
      };
    }
  };

  // COPY Flatpickr initialization FROM OLD SetAppointment.jsx
  useEffect(() => {
    if (isOpen && dateRef.current) {
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
    }
  }, [isOpen]);

  // COPY handleChange FROM OLD SetAppointment.jsx
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  // COPY handleSubmit FROM OLD SetAppointment.jsx (with modal adjustments)
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
      const slotDetails = await checkTimeSlotAvailability(form.preferredDate, form.preferredTime);

      if (!slotDetails.available) {
        if (slotDetails.is_past) {
          alert("This time slot has already passed. Please choose a future time.");
        } else {
          alert("This time slot is no longer available. Please choose another time.");
        }
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
        
        // Reset form
        setForm({ pet: "", service: "", preferredDate: "", preferredTime: "" });
        setAvailableTimes([]);
        
        // Close modal and callback
        onClose();
        if (onAppointmentBooked) {
          onAppointmentBooked(newAppointment);
        }
      } else {
        alert("Failed to set appointment. Please try again.");
      }
    } catch (error) {
      console.error("Error setting appointment:", error);
      alert("Error setting appointment. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  // COPY getTimeSlotStyle FROM OLD SetAppointment.jsx
  const getTimeSlotStyle = (slot) => {
    if (slot.isPast) {
      return {
        color: '#ccc',
        fontStyle: 'italic',
        textDecoration: 'line-through'
      };
    }
    if (!slot.available && slot.isFull) {
      return {
        color: '#999',
        fontStyle: 'italic'
      };
    }
    return {
      color: 'inherit',
      fontStyle: 'normal'
    };
  };

  // Check availability when date changes
  useEffect(() => {
    if (form.preferredDate) {
      checkAllTimeSlots(form.preferredDate);
    } else {
      setAvailableTimes([]);
    }
  }, [form.preferredDate]);

  if (!isOpen) return null;

  return (
    <div className="modal active">
      <div className="new-modal-content">
        <div className="new-modal-header">
          <h3 className="modal-title">Book Appointment</h3>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>
        <div className="modal-body">
          <form onSubmit={handleSubmit}>
            <div className="new-form-group">
              <label htmlFor="appointmentPet">Select Pet</label>
              <select
                name="pet"
                className="form-control"
                value={form.pet}
                onChange={handleChange}
                disabled={loadingPets}
                required
              >
                <option value="">
                  {loadingPets ? "Loading pets..." : "Select Pet"}
                </option>
                {pets.map((pet) => (
                  <option key={pet.id} value={pet.id}>
                    {pet.petName}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="new-form-group">
              <label htmlFor="appointmentService">Service</label>
              <select
                name="service"
                className="form-control"
                value={form.service}
                onChange={handleChange}
                required
              >
                <option value="">Select Service</option>
                <option value="Vaccination">Vaccination</option>
                <option value="Grooming">Grooming</option>
                <option value="Check-up">Check-up</option>
                <option value="Consultations">Consultations</option>
                <option value="Deworming">Deworming</option>
                <option value="Tick & Flea Prevention">Tick & Flea Prevention</option>
              </select>
            </div>
            
            <div className="new-form-row">
              <div className="new-form-group">
                <label htmlFor="appointmentDate">Preferred Date</label>
                <input 
                  ref={dateRef}
                  type="text" 
                  className="form-control" 
                  placeholder="Preferred Date"
                  readOnly
                />
              </div>
              <div className="form-group">
                <label htmlFor="appointmentTime">Preferred Time</label>
                <select
                  name="preferredTime"
                  className="form-control"
                  value={form.preferredTime}
                  onChange={handleChange}
                  disabled={!form.preferredDate || checkingAvailability}
                  required
                >
                  <option value="">
                    {checkingAvailability ? "Checking availability..." : "Select Time"}
                  </option>
                  {availableTimes.map((slot, index) => (
                    <option
                      key={index}
                      value={slot.value}
                      disabled={!slot.available || slot.isPast}
                      style={getTimeSlotStyle(slot)}
                    >
                      {slot.label}
                      {slot.isPast && ' (PASSED)'}
                      {!slot.available && slot.isFull && !slot.isPast && ' (FULL)'}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {availableTimes.length > 0 && availableTimes.every(slot => !slot.available || slot.isPast) && (
              <div style={{
                color: '#ff6b6b',
                textAlign: 'center',
                margin: '10px 0',
                fontSize: '14px',
                fontWeight: 'bold'
              }}>
                {availableTimes.every(slot => slot.isPast)
                  ? "All time slots for today have already passed. Please choose another date."
                  : "All time slots are fully booked for this date. Please choose another date."
                }
              </div>
            )}
            
            <div className="new-form-group bookBtns">
              <button 
                type="submit" 
                className="btn new-btn-primary" 
                disabled={submitting || checkingAvailability}
              >
                {submitting ? "Booking Appointment..." : "Book Appointment"}
              </button>
              <button type="button" className="btn" onClick={onClose}>Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default BookAppointmentModal;