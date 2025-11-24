import { useState, useEffect } from 'react'

const AppointmentCard = ({ appointment, onViewDetails }) => {
  const [timeSlotAvailability, setTimeSlotAvailability] = useState({})

  // Status badge system from old ViewAppointments
  const getAppointmentBadges = (appointment) => {
    const { request, status, date, prefTime } = appointment;
    const badges = [];

    const key = `${date}-${prefTime}`;
    const isCurrentlyAvailable = timeSlotAvailability[key];

    // Request status badges
    const requestConfig = {
      'pending': { class: 'request-pending', text: 'Under Review', icon: 'fas fa-hourglass-half' },
      'accepted': { class: 'request-accepted', text: 'Approved', icon: 'fas fa-thumbs-up' },
      'declined': {
        class: 'request-declined',
        text: isCurrentlyAvailable === false ? 'Time Slot Full' : 'Declined',
        icon: 'fas fa-times-circle'
      }
    };

    const requestInfo = requestConfig[request] || { class: 'request-pending', text: request, icon: 'fas fa-question-circle' };
    badges.push(
      <span key="request" className={`status-badge ${requestInfo.class}`}>
        <i className={requestInfo.icon}></i> {requestInfo.text}
      </span>
    );

    // Only show appointment status if request is accepted
    if (request === 'accepted') {
      const statusConfig = {
        'pending': { class: 'status-scheduled', text: 'Scheduled', icon: 'fas fa-calendar-alt' },
        'completed': { class: 'status-completed', text: 'Completed', icon: 'fas fa-check-double' },
        'overdue': { class: 'status-overdue', text: 'Overdue', icon: 'fas fa-exclamation-triangle' },
        'cancelled': { class: 'status-cancelled', text: 'Cancelled', icon: 'fas fa-ban' }
      };

      const statusInfo = statusConfig[status] || { class: 'status-scheduled', text: status, icon: '📅' };

      badges.push(
        <span key="status" className={`status-badge ${statusInfo.class}`}>
          <i className={statusInfo.icon}></i> {statusInfo.text}
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

  const petName = appointment.pet_name ||
    (appointment.pet && (appointment.pet.petName || appointment.pet.pet_name)) ||
    "Unknown Pet";

  const service = appointment.appointment_reason ||
    appointment.service_name ||
    "General Consultation";

  return (
    <div className="appointment-card">
      <div className="appointment-header">
        <div className="appointment-pet">{petName} - {service}</div>
        <div className="badges-container">
          {getAppointmentBadges(appointment)}
        </div>
      </div>
      
      <div className="status-explanation">
        {getStatusExplanation(appointment)}
      </div>

      <div className="appointment-details">
        <div>
          <div className="info-label">Date</div>
          <div className="info-value">{formatDate(appointment.date)}</div>
        </div>
        <div>
          <div className="info-label">Time</div>
          <div className="info-value">{formatTime(appointment.prefTime)}</div>
        </div>
        <div>
          <div className="info-label">Service</div>
          <div className="info-value">{service}</div>
        </div>
      </div>

      <div className="pet-actions">
        <button className="btn btn-small" onClick={() => onViewDetails(appointment)}>
          View Details
        </button>
        {appointment.comments && (
          <button 
            className="btn btn-small btn-secondary" 
            onClick={(e) => {
              e.stopPropagation();
              alert(`Staff Comments:\n\n${appointment.comments}`);
            }}
          >
            View Remarks
          </button>
        )}
      </div>
    </div>
  )
}

export default AppointmentCard