const AppointmentCard = ({ appointment, onViewDetails }) => {
  // COPY getStatusClass and other logic from old ViewAppointments.jsx
  const getStatusClass = (status) => {
    switch(status) {
      case 'pending': return 'status-pending'
      case 'confirmed': return 'status-confirmed'
      case 'completed': return 'status-completed'
      case 'cancelled': return 'status-cancelled'
      default: return ''
    }
  }

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
        <div className={`appointment-status ${getStatusClass(appointment.status)}`}>
          {appointment.status ? appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1) : 'Pending'}
        </div>
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
          <div className="info-label">Status</div>
          <div className="info-value">{appointment.request || 'pending'}</div>
        </div>
      </div>
      <div className="appointment-service">Service: {service}</div>
      <div className="pet-actions">
        <button className="btn btn-small" onClick={() => onViewDetails(appointment)}>
          View Details
        </button>
      </div>
    </div>
  )
}

export default AppointmentCard