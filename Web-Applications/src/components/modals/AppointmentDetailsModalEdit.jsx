import React, { useState, useEffect, useRef } from 'react';
import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css";
import { getCookie } from '../../utils/csrf';
import { apiFetch, readJsonSafe, normalizeList } from '../../config/api';

const AppointmentDetailsModalEdit = ({ isOpen, onClose, appointment, onSuccess }) => {

  // --- 1. STATE INITIALIZATION (Combined Logic) ---
  const [formData, setFormData] = useState({
    pet: "",
    service: "",
    preferredDate: "",
    preferredTime: "",
  });

  // Loading states
  const [isLoading, setIsLoading] = useState(false); // For saving
  const [loadingPets, setLoadingPets] = useState(true);
  const [loadingServices, setLoadingServices] = useState(true);
  const [loadingHours, setLoadingHours] = useState(true);
  const [checkingAvailability, setCheckingAvailability] = useState(false);

  // Data states
  const [pets, setPets] = useState([]);
  const [services, setServices] = useState([]);
  const [availableTimes, setAvailableTimes] = useState([]);
  const [officeHours, setOfficeHours] = useState({});
  
  // Refs
  const dateRef = useRef(null);

  // --- 2. HELPER FUNCTIONS ---

  const getDayName = (dateString) => {
    try {
      const date = new Date(dateString);
      const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
      return days[date.getDay()];
    } catch (error) {
      console.error("Error in getDayName:", error);
      return '';
    }
  };

  const parseTimeString = (timeStr) => {
    if (!timeStr) return null;
    const [hours, minutes] = timeStr.split(':').map(Number);
    const date = new Date();
    date.setHours(hours, minutes, 0, 0);
    return date;
  };

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

  const getTimeSlotsForDay = (dateString) => {
    const dayName = getDayName(dateString);
    const dayHours = officeHours[dayName];

    if (!dayHours || dayHours.status === 'closed' || dayHours.status === 'appointment_only') {
      return [];
    }
    if (dayHours.start_time && dayHours.end_time) {
      return generateTimeSlots(dayHours.start_time, dayHours.end_time);
    }
    return [];
  };

  const checkTimeSlotAvailability = async (date, time) => {
    try {
      const response = await apiFetch(`/api/check-time-slot/?date=${date}&time=${time}`);
      if (response.ok) return await response.json();
      return { available: true, is_past: false, is_full: false, message: 'Available' };
    } catch (error) {
      console.error("Error checking time slot:", error);
      return { available: true, is_past: false, is_full: false, message: 'Available' };
    }
  };

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
      // Fallback: show all as available
      setAvailableTimes(timeSlotsForDay.map(slot => ({
        ...slot, available: true, isPast: false, isFull: false, message: 'Available'
      })));
    } finally {
      setCheckingAvailability(false);
    }
  };

  const getTimeSlotStyle = (slot) => {
    if (slot.isPast) return { color: '#ccc', fontStyle: 'italic', textDecoration: 'line-through' };
    if (!slot.available && slot.isFull) return { color: '#999', fontStyle: 'italic' };
    return { color: 'inherit', fontStyle: 'normal' };
  };


  // --- 3. EFFECTS (Fetching Data) ---

  // Pre-fill Appointment Data
  useEffect(() => {
    if (appointment) {
      const petId = appointment.pet_id || (appointment.pet && appointment.pet.id) || "";
      const serviceId = appointment.service_type_id || ""; 
      
      setFormData({
        pet: petId, 
        service: serviceId,
        preferredDate: appointment.date || '',
        preferredTime: appointment.prefTime || ''
      });
    }
  }, [appointment]);

  // Fetch Pets
  useEffect(() => {
    const fetchPets = async () => {
      setLoadingPets(true);
      try {
        const res = await apiFetch("/api/pets/", {
          headers: { "X-CSRFToken": getCookie("csrftoken") || "" },
        });

        if (!res.ok) {
          console.error("Failed to fetch pets", res.status);
          setPets([]);
          return;
        }

        const data = await readJsonSafe(res);
        setPets(normalizeList(data));
      } catch (err) {
        console.error("Error fetching pets:", err);
        setPets([]);
      } finally {
        setLoadingPets(false);
      }
    };

    if (isOpen) fetchPets();
  }, [isOpen]);

  // Fetch Services
  useEffect(() => {
    if (isOpen) {
      apiFetch("/api/service-types/?is_active=true&no_pagination=true")
        .then(res => res.json())
        .then(data => {
            const list = Array.isArray(data) ? data : (data.results || []);
            const active = list.filter(s => s.is_active !== false);
            setServices(active);
        })
        .catch(err => console.error(err))
        .finally(() => setLoadingServices(false));
    }
  }, [isOpen]);

  // Fetch Office Hours
  useEffect(() => {
    if (isOpen) {
      apiFetch("/api/office-hours/")
        .then(res => res.json())
        .then(data => {
            const hoursObj = {};
            data.forEach(h => hoursObj[h.day] = h);
            setOfficeHours(hoursObj);
        })
        .catch(err => console.error(err))
        .finally(() => setLoadingHours(false));
    }
  }, [isOpen]);

  // Flatpickr Logic
  useEffect(() => {
    if (isOpen && dateRef.current && !loadingHours && Object.keys(officeHours).length > 0) {

      const toDateObject = (ymd) => {
        if (!ymd || typeof ymd !== 'string') return null;
        const trimmed = ymd.trim();
        const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(trimmed);
        if (!match) return null;
        return new Date(`${match[1]}-${match[2]}-${match[3]}T00:00:00`);
      };
      
      // Destroy existing instance
      if (dateRef.current._flatpickr) dateRef.current._flatpickr.destroy();

      flatpickr(dateRef.current, {
        dateFormat: "M d, Y",
        // `formData.preferredDate` is stored as YYYY-MM-DD; Flatpickr would try to parse it
        // using `dateFormat` and throw "Invalid date provided". Use a Date object instead.
        defaultDate: toDateObject(formData.preferredDate) || "today",
        minDate: "today",
        disable: [
          function(date) {
             const dayName = date.toLocaleDateString('en-US', { weekday: 'long' }).toLowerCase();
             const hours = officeHours[dayName];
             if (!hours) return false; // Allow if no data
             // Disable if closed or missing times
             if (hours.status !== 'open' || !hours.start_time || !hours.end_time) return true;
             return false;
          }
        ],
        onChange: (selectedDates) => {
          if (selectedDates.length > 0) {
            const dateStr = selectedDates[0].toLocaleDateString("en-CA");
            setFormData(prev => ({ ...prev, preferredDate: dateStr, preferredTime: "" }));
          }
        }
      });
    }
  }, [isOpen, loadingHours, officeHours, appointment?.id]); // re-init when switching appointments

  // Update Available Times when Date Changes
  useEffect(() => {
    if (formData.preferredDate && !loadingHours) {
      const slots = getTimeSlotsForDay(formData.preferredDate);
      if (slots.length > 0) {
        checkAllTimeSlots(formData.preferredDate, slots);
      } else {
        setAvailableTimes([]);
      }
    } else {
      setAvailableTimes([]);
    }
  }, [formData.preferredDate, loadingHours]); // removed officeHours dependency to avoid loop


  // --- 4. HANDLERS ---

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    const canEdit = appointment?.request === 'pending' && appointment?.status !== 'overdue';
    if (!canEdit) {
      alert('This appointment can only be edited while it is under review.');
      setIsLoading(false);
      return;
    }
    
    // Basic validation
    if (!formData.pet || !formData.service || !formData.preferredDate || !formData.preferredTime) {
        alert("Please fill all fields");
        setIsLoading(false);
        return;
    }

    try {
      // Re-check slot availability before saving
      const slotDetails = await checkTimeSlotAvailability(formData.preferredDate, formData.preferredTime);

      if (!slotDetails.available) {
        if (slotDetails.is_past) {
          alert("This time slot has already passed. Please choose a future time.");
        } else {
          alert(slotDetails.message || "This time slot is no longer available. Please choose another time.");
        }
        setIsLoading(false);
        return;
      }

      const payload = {
        pet_id: formData.pet,
        service_type_id: formData.service,
        date: formData.preferredDate,
        prefTime: formData.preferredTime,
      };

      const res = await apiFetch(`/api/walkIn/${appointment.id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
          'X-CSRFToken': getCookie('csrftoken') || '',
        },
        body: JSON.stringify(payload),
      });

      const data = await readJsonSafe(res);

      if (!res.ok) {
        const msg = (data && (data.detail || data.error)) || 'Failed to update appointment.';
        throw new Error(msg);
      }

      setIsLoading(false);
      if (onSuccess) onSuccess(data);
      onClose();

    } catch (error) {
      console.error("Error updating:", error);
      alert(error.message || 'Error updating appointment. Please try again.');
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  const canEdit = appointment?.request === 'pending' && appointment?.status !== 'overdue';
  if (!canEdit) {
    return (
      <div className="modal active" onClick={onClose} style={{ zIndex: 1050 }}>
        <div className="new-modal-content" onClick={(e) => e.stopPropagation()}>
          <div className="new-modal-header">
            <h3 className="modal-title">Edit Appointment</h3>
            <button className="modal-close" onClick={onClose}>&times;</button>
          </div>
          <div className="modal-body">
            <div style={{ padding: '10px 0' }}>
              This appointment can only be edited while it is under review.
            </div>
          </div>
          <div className="modal-actions close-appointment-details" style={{ gap: '15px' }}>
            <button type="button" className="btn-btn" onClick={onClose} style={{ minWidth: '120px' }}>
              Close
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="modal active" onClick={onClose} style={{ zIndex: 1050 }}>
      <div className="new-modal-content" onClick={(e) => e.stopPropagation()}>
        
        <div className="new-modal-header">
          <h3 className="modal-title">Edit Appointment</h3>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>

        <div className="modal-body">
          <form id="editForm" onSubmit={handleSave}>
            
            <div className="detail-section">
              <div className="detail-grid">
                
                {/* 1. PET SELECT */}
                <div className="detail-item">
                  <span className="detail-label">Pet:</span>
                  <select
                    name="pet"
                    className="form-control"
                    value={formData.pet}
                    onChange={handleChange}
                    disabled={loadingPets}
                    required
                    style={{ marginTop: '5px' }}
                  >
                    <option value="">{loadingPets ? "Loading..." : "Select Pet"}</option>
                    {pets.map(pet => (
                        <option key={pet.id} value={pet.id}>{pet.petName || pet.pet_name || 'Unnamed Pet'}</option>
                    ))}
                  </select>
                </div>

                {/* 2. SERVICE SELECT */}
                <div className="detail-item">
                  <span className="detail-label">Service:</span>
                  <select 
                    name="service" 
                    value={formData.service} 
                    onChange={handleChange}
                    className="form-control"
                    disabled={loadingServices}
                    style={{ marginTop: '5px' }}
                    required
                  >
                    <option value="">{loadingServices ? "Loading..." : "Select Service"}</option>
                    {services.map(s => (
                        <option key={s.id} value={s.id}>{s.name}</option>
                    ))}
                  </select>
                </div>

                {/* 3. DATE PICKER (Flatpickr) */}
                <div className="detail-item">
                  <span className="detail-label">Date:</span>
                  <input 
                    ref={dateRef}
                    type="text" 
                    className="form-control"
                    placeholder="Select Date"
                    defaultValue={formData.preferredDate} // Use defaultValue for uncontrolled component (handled by flatpickr)
                    style={{ marginTop: '5px' }}
                    readOnly
                  />
                </div>

                {/* 4. TIME SELECT (Dynamic) */}
                <div className="detail-item">
                  <span className="detail-label">Time:</span>
                  <select 
                    name="preferredTime" 
                    value={formData.preferredTime}
                    onChange={handleChange}
                    className="form-control"
                    disabled={!formData.preferredDate || checkingAvailability || loadingHours}
                    required
                    style={{ marginTop: '5px' }}
                  >
                    <option value="">
                        {checkingAvailability ? "Checking..." : 
                         !formData.preferredDate ? "Select Date First" : "Select Time"}
                    </option>
                    {availableTimes.map((slot, idx) => (
                        <option 
                            key={idx} 
                            value={slot.value} 
                            disabled={!slot.available || slot.isPast}
                            style={getTimeSlotStyle(slot)}
                        >
                            {slot.label} 
                            {slot.isPast ? '' : ''}
                            {!slot.available && slot.isFull && !slot.isPast ? ' (FULL)' : ''}
                        </option>
                    ))}
                  </select>
                </div>

              </div>
            </div>
            
            <div style={{ marginTop: '20px', fontSize: '0.9rem', color: '#666', fontStyle: 'italic' }}>
              <i className="fas fa-info-circle"></i> Modifying these details may require re-approval.
            </div>

          </form>
        </div>

        <div className="modal-actions close-appointment-details" style={{ gap: '15px' }}>
          <button 
            type="submit" 
            form="editForm" 
            className="btn-edit" 
            disabled={isLoading}
            style={{ minWidth: '120px' }}
          >
            {isLoading ? 'Saving...' : 'Save Changes'}
          </button>

          <button 
            type="button" 
            className="btn-btn" 
            onClick={onClose}
            disabled={isLoading}
            style={{ minWidth: '120px' }}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

export default AppointmentDetailsModalEdit;