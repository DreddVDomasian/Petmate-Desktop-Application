import { useState, useEffect, useRef } from "react";
import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";
import { getCookie } from '../../utils/csrf';
import { apiFetch, readJsonSafe, normalizeList } from '../../config/api';

const BookAppointmentModal = ({ isOpen, onClose, onAppointmentBooked }) => {
  const [form, setForm] = useState({
    pet: "",
    service: "",
    preferredDate: "",
    preferredTime: "",
  });

  const [pets, setPets] = useState([]);
  const [services, setServices] = useState([]);
  const [loadingPets, setLoadingPets] = useState(true);
  const [loadingServices, setLoadingServices] = useState(true);
  const [servicesError, setServicesError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const [availableTimes, setAvailableTimes] = useState([]);
  const [checkingAvailability, setCheckingAvailability] = useState(false);

  const [officeHours, setOfficeHours] = useState({});
  const [loadingHours, setLoadingHours] = useState(true);

  const dateRef = useRef(null);

  
  const generateTimeSlots = (startTime, endTime) => {
    if (!startTime || !endTime) return [];

    const slots = [];
    let current = parseTimeString(startTime);
    const end = parseTimeString(endTime);

    
    const maxEndTime = new Date(end.getTime() - 30 * 60000);

    
    while (current <= maxEndTime) {
      const hours = current.getHours();
      const minutes = current.getMinutes();
      const timeValue = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:00`;

      
      const ampm = hours >= 12 ? 'PM' : 'AM';
      const displayHours = hours % 12 || 12;
      const displayMinutes = minutes.toString().padStart(2, '0');
      const label = `${displayHours}:${displayMinutes} ${ampm}`;

      slots.push({ label, value: timeValue });

      
      current = new Date(current.getTime() + 30 * 60000);
    }

    return slots;
  };

  const parseTimeString = (timeStr) => {
    if (!timeStr) return null;
    const [hours, minutes] = timeStr.split(':').map(Number);
    const date = new Date();
    date.setHours(hours, minutes, 0, 0);
    return date;
  };

  
  useEffect(() => {
    const fetchPets = async () => {
      try {
        const res = await apiFetch("/api/pets/", {
          headers: { "X-CSRFToken": getCookie("csrftoken") || "" },
        });
        if (res.ok) {
          const data = await readJsonSafe(res);
          setPets(normalizeList(data));
        } else {
          console.error("Failed to fetch pets");
          setPets([]);
        }
      } catch (error) {
        console.error("Error fetching pets:", error);
        setPets([]);
      } finally {
        setLoadingPets(false);
      }
    };

    if (isOpen) {
      fetchPets();
    }
  }, [isOpen]);
  useEffect(() => {
    const fetchServices = async () => {
      if (!isOpen) return;

      try {
        setLoadingServices(true);
        setServicesError(null);

        
        const res = await apiFetch("/api/service-types/?is_active=true&no_pagination=true", {
          headers: { "X-CSRFToken": getCookie("csrftoken") || "" },
        });

        if (res.ok) {
          const data = await res.json();
          console.log("Services API response:", data); 

          
          const servicesData = Array.isArray(data) ? data : (data.results || []);
          console.log("Parsed services:", servicesData); 

          
          const activeServices = servicesData.filter(service =>
            service.is_active !== false && service.name
          );

          console.log("Active services:", activeServices); 

          if (activeServices.length === 0) {
            setServicesError("No services available at the moment.");
            
            setServices([]);
          } else {
            setServices(activeServices);
          }

        } else {
          console.error("Failed to fetch services:", res.status);
          setServicesError("Failed to load services. Please try again.");
          
          setServices([
            { id: 1, name: "Vaccination" },
            { id: 2, name: "Grooming" },
            { id: 3, name: "Check-up" },
            { id: 4, name: "Consultation" },
            { id: 5, name: "Deworming" },
            { id: 6, name: "Tick & Flea Prevention" },
          ]);
        }
      } catch (error) {
        console.error("Error fetching services:", error);
        setServicesError("Network error. Please check your connection.");
        
        setServices([
          { id: 1, name: "Vaccination" },
          { id: 2, name: "Grooming" },
          { id: 3, name: "Check-up" },
          { id: 4, name: "Consultation" },
          { id: 5, name: "Deworming" },
          { id: 6, name: "Tick & Flea Prevention" },
        ]);
      } finally {
        setLoadingServices(false);
      }
    };

    if (isOpen) {
      fetchServices();
    }
  }, [isOpen]);
  
  useEffect(() => {
    const fetchOfficeHours = async () => {
      try {
        setLoadingHours(true);
        const res = await apiFetch("/api/office-hours/", {
          headers: { "X-CSRFToken": getCookie("csrftoken") || "" },
        });
        if (res.ok) {
          const data = await res.json();
          
          const hoursObj = {};
          data.forEach(hour => {
            hoursObj[hour.day] = {
              status: hour.status,
              start_time: hour.start_time,
              end_time: hour.end_time
            };
          });
          setOfficeHours(hoursObj);
        } else {
          console.error("Failed to fetch office hours");
        }
      } catch (error) {
        console.error("Error fetching office hours:", error);
      } finally {
        setLoadingHours(false);
      }
    };

    if (isOpen) {
      fetchOfficeHours();
    }
  }, [isOpen]);

  
  const checkAllTimeSlots = async (date, timeSlotsForDay) => {
    setCheckingAvailability(true);

    try {
      const updatedSlots = await Promise.all(
        timeSlotsForDay.map(async (slot) => {
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
      
      setAvailableTimes(timeSlotsForDay.map(slot => ({
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

  
  const checkTimeSlotAvailability = async (date, time) => {
    try {
      const response = await apiFetch(`/api/check-time-slot/?date=${date}&time=${time}`, {
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

  const getDayName = (dateString) => {
    try {
      const date = new Date(dateString);
      const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
      const dayIndex = date.getDay(); 
      console.log("getDayName input:", dateString, "output:", days[dayIndex]); 
      return days[dayIndex];
    } catch (error) {
      console.error("Error in getDayName:", error);
      return '';
    }
  };
  
  const getTimeSlotsForDay = (dateString) => {
    const dayName = getDayName(dateString);
    const dayHours = officeHours[dayName];

    if (!dayHours) return [];

    if (dayHours.status === 'closed' || dayHours.status === 'appointment_only') {
      return [];
    }

    if (dayHours.start_time && dayHours.end_time) {
      return generateTimeSlots(dayHours.start_time, dayHours.end_time);
    }

    return [];
  };

  
  useEffect(() => {
    if (isOpen && dateRef.current && !loadingHours && Object.keys(officeHours).length > 0) {
      console.log("Office hours loaded:", officeHours); 

      
      const enableDates = (date) => {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const selectedDate = new Date(date);
        selectedDate.setHours(0, 0, 0, 0);

        console.log("Checking date:", date, "vs today:", today); 

        
        if (selectedDate < today) {
          console.log("Disabling - date is in past"); 
          return false;
        }

        
        const dayName = date.toLocaleDateString('en-US', { weekday: 'long' }).toLowerCase();
        const dayHours = officeHours[dayName];

        console.log("Day name:", dayName, "Office hours:", dayHours); 

        if (!dayHours) {
          console.log("No office hours data - enabling by default"); 
          return true; 
        }

        
        const isEnabled = dayHours.status === 'open' &&
          dayHours.start_time &&
          dayHours.end_time;

        console.log("Day enabled status:", isEnabled); 
        return isEnabled;
      };

      
      if (dateRef.current._flatpickr) {
        dateRef.current._flatpickr.destroy();
      }

      flatpickr(dateRef.current, {
        dateFormat: "M d, Y",
        minDate: "today",
        disable: [
          function (date) {
            const result = !enableDates(date);
            console.log("Flatpickr disable check for", date, ":", result); 
            return result;
          }
        ],
        onChange: (selectedDates) => {
          if (selectedDates.length > 0) {
            const date = selectedDates[0];
            const dateString = date.toLocaleDateString("en-CA");
            console.log("Date selected:", dateString); 
            setForm((prev) => ({
              ...prev,
              preferredDate: dateString,
              preferredTime: "" 
            }));
          }
        },
      });
    }
  }, [isOpen, officeHours, loadingHours]);

  
  useEffect(() => {
    return () => {
      if (window.flatpickrInstances && window.flatpickrInstances.datePicker) {
        window.flatpickrInstances.datePicker.destroy();
        delete window.flatpickrInstances.datePicker;
      }
    };
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

    
    const dayName = getDayName(form.preferredDate);
    const dayHours = officeHours[dayName];

    if (!dayHours || dayHours.status !== 'open') {
      alert("This day is not available for appointments. Please choose another day.");
      setSubmitting(false);
      return;
    }

    try {
      
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
      const serviceTypeId = form.service; 
      const appointmentData = {
        pet_id: parseInt(form.pet),
        service_type_id: serviceTypeId,  
        date: form.preferredDate,
        prefTime: form.preferredTime,
        request: "pending",
        status: "pending",
      };

      const res = await apiFetch("/api/walkIn/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken") || "",
        },
        body: JSON.stringify(appointmentData),
      });

      if (res.status === 201) {
        const newAppointment = await res.json();
        alert("Appointment set successfully! Waiting for admin approval.");

        
        setForm({ pet: "", service: "", preferredDate: "", preferredTime: "" });
        setAvailableTimes([]);

        
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

  
  useEffect(() => {
    if (form.preferredDate && !loadingHours) {
      const timeSlotsForDay = getTimeSlotsForDay(form.preferredDate);
      if (timeSlotsForDay.length > 0) {
        checkAllTimeSlots(form.preferredDate, timeSlotsForDay);
      } else {
        setAvailableTimes([]);
      }
    } else {
      setAvailableTimes([]);
    }
  }, [form.preferredDate, loadingHours]);

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
                value={form.service}
                className="form-control"
                onChange={handleChange}
                disabled={loadingServices}
                required
              >
                <option value="">
                  {loadingServices ? "Loading services..." : "Select Service"}
                </option>
                {services.map((service) => (
                  <option key={service.id} value={service.id}>  {}
                    {service.name}
                  </option>
                ))}
              </select>
              {services.length === 0 && !loadingServices && (
                <div className="form-text" style={{ color: '#ff6b6b', fontSize: '12px' }}>
                  No services available. Please contact the clinic.
                </div>
              )}
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
                  disabled={!form.preferredDate || checkingAvailability || loadingHours}
                  required
                >
                  <option value="">
                    {loadingHours ? "Loading hours..." :
                      checkingAvailability ? "Checking availability..." :
                        !form.preferredDate ? "Select date first" :
                          "Select Time"}
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

            {}
            {form.preferredDate && !loadingHours && (
              (() => {
                const dayName = getDayName(form.preferredDate);
                const dayHours = officeHours[dayName];

                if (!dayHours || dayHours.status === 'closed') {
                  return (
                    <div className="day-status-message closed">
                      <i className="fas fa-times-circle"></i>
                      <span>Closed on {dayName.charAt(0).toUpperCase() + dayName.slice(1)}</span>
                    </div>
                  );
                }

                if (dayHours.status === 'appointment_only') {
                  return (
                    <div className="day-status-message appointment-only">
                      <i className="fas fa-calendar-check"></i>
                      <span>Appointment Only on {dayName.charAt(0).toUpperCase() + dayName.slice(1)}</span>
                    </div>
                  );
                }

                if (dayHours.status === 'open' && availableTimes.length === 0) {
                  return (
                    <div className="day-status-message no-slots">
                      <i className="fas fa-clock"></i>
                      <span>No available time slots for {dayName.charAt(0).toUpperCase() + dayName.slice(1)}</span>
                    </div>
                  );
                }

                return null;
              })()
            )}

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

            <div className="new-form-group bookBtns modal-actions">
              <button
                type="submit"
                className="btn new-btn-primary"
                disabled={submitting || checkingAvailability || loadingHours ||
                  (form.preferredDate && (!officeHours[getDayName(form.preferredDate)] ||
                    officeHours[getDayName(form.preferredDate)].status !== 'open'))}
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