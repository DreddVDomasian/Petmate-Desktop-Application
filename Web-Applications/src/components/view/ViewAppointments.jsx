import React, { useState, useEffect } from "react";
import { getCookie } from "../../utils/csrf";

export default function ViewAppointments() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [timeSlotAvailability, setTimeSlotAvailability] = useState({});

  const fetchAppointments = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/walkIn/", {
        method: "GET",
        credentials: "include",
        headers: {
          Accept: "application/json",
          "X-CSRFToken": getCookie("csrftoken") || "",
        },
      });

      const text = await res.text();
      const data = text ? JSON.parse(text) : [];

      if (!res.ok) {
        throw new Error(data.error || data.detail || JSON.stringify(data));
      }

      const list = Array.isArray(data) ? data : data.results || data.appointments || [];
      setAppointments(list);
    } catch (err) {
      setError(err.message || "Failed to load appointments");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAppointments();
  }, []);

  const formatDate = (dateString) => {
    if (!dateString) return "Not specified";
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const formatTime = (timeString) => {
    if (!timeString) return "Not specified";
    if (timeString.includes(":")) {
      const [hours, minutes] = timeString.split(":");
      const date = new Date();
      date.setHours(parseInt(hours), parseInt(minutes));
      return date.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      });
    }
    return timeString;
  };
  // New function to check time slot availability
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

  // Check availability for all declined appointments
  useEffect(() => {
    const checkDeclinedAppointments = async () => {
      const declinedAppointments = appointments.filter(appt => appt.request === 'declined');

      const availabilityMap = {};

      for (const appointment of declinedAppointments) {
        const date = appointment.date;
        const time = appointment.prefTime;

        if (date && time) {
          const key = `${date}-${time}`;
          const isAvailable = await checkTimeSlotAvailability(date, time);
          availabilityMap[key] = isAvailable;
        }
      }

      setTimeSlotAvailability(availabilityMap);
    };

    if (appointments.length > 0) {
      checkDeclinedAppointments();
    }
  }, [appointments]);

  // Updated badge system - only show relevant badges based on request status

  const getAppointmentBadges = (appointment) => {
    const { request, status, date, prefTime } = appointment;
    const badges = [];

    const key = `${date}-${prefTime}`;
    const isCurrentlyAvailable = timeSlotAvailability[key];

    // Request status badges
    const requestConfig = {
      'pending': { class: 'request-pending', text: 'Under Review', icon: '⏳' },
      'accepted': { class: 'request-accepted', text: 'Approved', icon: '✅' },
      'declined': {
        class: 'request-declined',
        text: isCurrentlyAvailable === false ? 'Time Slot Full' : 'Declined',
        icon: '❌'
      }
    };

    const requestInfo = requestConfig[request] || { class: 'request-pending', text: request, icon: '❓' };

    badges.push(
      <span key="request" className={`status-badge ${requestInfo.class}`}>
        {requestInfo.icon} {requestInfo.text}
      </span>
    );

    // Only show appointment status if request is accepted
    if (request === 'accepted') {
      const statusConfig = {
        'pending': { class: 'status-scheduled', text: 'Scheduled', icon: '📅' },
        'completed': { class: 'status-completed', text: 'Completed', icon: '✅' },
        'overdue': { class: 'status-overdue', text: 'Overdue', icon: '⚠️' },
        'cancelled': { class: 'status-cancelled', text: 'Cancelled', icon: '❌' }
      };

      const statusInfo = statusConfig[status] || { class: 'status-scheduled', text: status, icon: '📅' };

      badges.push(
        <span key="status" className={`status-badge ${statusInfo.class}`}>
          {statusInfo.icon} {statusInfo.text}
        </span>
      );
    }

    return badges;
  };

const getStatusExplanation = (appointment) => {
    const { request, status, date, prefTime } = appointment;

    if (request === 'pending') return 'Your appointment request is under review by our staff.';

    if (request === 'declined') {
      const key = `${date}-${prefTime}`;
      const isCurrentlyAvailable = timeSlotAvailability[key];

      if (isCurrentlyAvailable === false) {
        return 'Please reschedule for available time.';
      }
      return 'Your appointment request was not approved.';
    }

    if (request === 'accepted' && status === 'pending') return 'Your appointment has been approved and is scheduled.';
    if (request === 'accepted' && status === 'completed') return 'Your appointment has been successfully completed.';
    if (request === 'accepted' && status === 'overdue') return 'Your appointment was missed or needs rescheduling.';
    if (request === 'accepted' && status === 'cancelled') return 'Your appointment was cancelled.';
    return 'Status information not available.';
  };

  const openDetailsModal = (appointment) => {
    setSelectedAppointment(appointment);
    setShowDetailsModal(true);
  };

  const closeDetailsModal = () => {
    setSelectedAppointment(null);
    setShowDetailsModal(false);
  };

  return (
    <div className="appointments-container">
      <div className="page-header">
        <h2 className="page-title">My Appointments</h2>
        <p className="page-subtitle">Track your appointment requests and status</p>
      </div>

      <button
        onClick={fetchAppointments}
        disabled={loading}
        className="refresh-btn"
      >
        {loading ? "Loading…" : "Refresh Appointments"}
      </button>

      {loading && <div className="loading">Loading appointments…</div>}
      {error && <div className="error-message">Error: {error}</div>}

      {!loading && !error && (
        <div className="appointments-card-grid">
          {appointments.length === 0 ? (
          <div className="empty-state">
            <img src="/assets/icons/dog-walking.gif" alt="No pets" className="empty-icon" />
            <h3>No Appointment Yet</h3>
            <p>Schedule your appointment to get started.</p>
          </div>
          ) : (
            appointments.map((appointment) => {
              const petName = appointment.pet_name ||
                (appointment.pet && (appointment.pet.petName || appointment.pet.pet_name)) ||
                "Unknown Pet";

              const service = appointment.appointment_reason ||
                appointment.service_name ||
                "General Consultation";

              const date = appointment.date ||
                appointment.appointment_datetime?.split(" ")[0] || "Not specified";

              const time = appointment.prefTime ||
                (appointment.appointment_datetime?.includes(" ")
                  ? appointment.appointment_datetime.split(" ")[1]
                  : null) || "Not specified";

              const requestStatus = appointment.request || "pending";
              const appointmentStatus = appointment.status || "pending";

              return (
                <div key={appointment.id} className="appointment-card">
                  <div className="card-header">
                    <h3 className="pet-name">{petName}</h3>
                    <div className="badges-container">
                      {getAppointmentBadges(appointment)}
                    </div>
                  </div>

                  <div className="status-explanation">
                    {getStatusExplanation(appointment)}
                  </div>

                  <div className="card-divider" />

                  <div className="appointment-details">
                    <div className="detail-row">
                      <span className="detail-label">Service:</span>
                      <span className="detail-value">{service}</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Date:</span>
                      <span className="detail-value">{formatDate(date)}</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Time:</span>
                      <span className="detail-value">{formatTime(time)}</span>
                    </div>
                  </div>

                  <div className="card-actions">
                    <button
                      className="view-btn"
                      onClick={() => openDetailsModal(appointment)}
                    >
                      View Details
                    </button>
                    {appointment.comments && (
                      <button
                        className="comments-btn"
                        onClick={() => alert(`Staff Comments:\n\n${appointment.comments}`)}
                      >
                        View Remarks
                      </button>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>
      )}

      {/* Details Modal */}
      {showDetailsModal && selectedAppointment && (
        <div className="modal-overlay" onClick={closeDetailsModal}>
          <div className="details-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Appointment Details</h2>
              <button className="close-btn" onClick={closeDetailsModal}>×</button>
            </div>

            <div className="appointment-details-modal">
              <div className="detail-section">
                <div className="detail-grid">
                  <div className="detail-item">
                    <span className="detail-label">Pet:</span>
                    <span className="detail-value">
                      {selectedAppointment.pet_name ||
                       (selectedAppointment.pet && (selectedAppointment.pet.petName || selectedAppointment.pet.pet_name)) ||
                       "Unknown Pet"}
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Service:</span>
                    <span className="detail-value">
                      {selectedAppointment.appointment_reason || selectedAppointment.service_name || "General Consultation"}
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Date:</span>
                    <span className="detail-value">{formatDate(selectedAppointment.date)}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Time:</span>
                    <span className="detail-value">{formatTime(selectedAppointment.prefTime)}</span>
                  </div>
                </div>
              </div>

              <div className="detail-section">
                <h3>Status Information</h3>
                <div className="status-display">
                  <div className="status-item">
                    <span className="status-label">Request Status:</span>
                    <div className="badges-container">
                      {getAppointmentBadges(selectedAppointment.request || "pending", selectedAppointment.status || "pending")}
                    </div>
                  </div>
                  <div className="status-explanation-full">
                    {getStatusExplanation(selectedAppointment.request, selectedAppointment.status)}
                  </div>
                </div>
              </div>

              {selectedAppointment.comments && (
                <div className="detail-section">
                  <h3>Staff Remarks</h3>
                  <div className="comments-box">
                    {selectedAppointment.comments}
                  </div>
                </div>
              )}
            </div>

            <div className="modal-actions">
              <button className="close-modal-btn" onClick={closeDetailsModal}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}