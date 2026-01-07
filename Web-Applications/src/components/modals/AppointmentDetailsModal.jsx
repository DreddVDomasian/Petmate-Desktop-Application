// Added onEdit to the props
const AppointmentDetailsModal = ({ isOpen, onClose, appointment, onEdit }) => {
  if (!isOpen || !appointment) return null;

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

  const getAppointmentBadges = (appointment) => {
    const { request, status } = appointment;
    const badges = [];

    // Request status badges
    const requestConfig = {
      'pending': { class: 'request-pending', text: 'Under Review', icon: 'fas fa-hourglass-half' },
      'accepted': { class: 'request-accepted', text: 'Approved', icon: 'fas fa-check-circle' },
      'declined': { class: 'request-declined', text: 'Declined', icon: 'fas fa-times-circle' }
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
        'pending': { class: 'status-scheduled', text: 'Scheduled', icon: 'fas fa-calendar'  },
        'completed': { class: 'status-completed', text: 'Completed', icon: 'fas fa-check-double' },
        'overdue': { class: 'status-overdue', text: 'Overdue', icon: 'fas fa-exclamation-triangle' },
        'cancelled': { class: 'status-cancelled', text: 'Cancelled', icon: 'fas fa-ban' }
      };

      const statusInfo = statusConfig[status] || { class: 'status-scheduled', text: status, icon: 'fas fa-calendar-check' };

      badges.push(
        <span className={`status-badge ${statusInfo.class}`}>
            <i className={statusInfo.icon}></i> {statusInfo.text}
        </span>
      );
    }

    return badges;
  };

  const getStatusExplanation = (appointment) => {
    const { request, status } = appointment;

    if (request === 'pending') return 'Your appointment request is under review by our staff.';
    if (request === 'declined') return 'Your appointment request was not approved.';
    if (request === 'accepted' && status === 'pending') return 'Your appointment has been approved and is scheduled.';
    if (request === 'accepted' && status === 'completed') return 'Your appointment has been successfully completed.';
    if (request === 'accepted' && status === 'overdue') return 'Your appointment was missed or needs rescheduling.';
    if (request === 'accepted' && status === 'cancelled') return 'Your appointment was cancelled.';
    return 'Status information not available.';
  };

  const petName = appointment.pet_name ||
    (appointment.pet && (appointment.pet.petName || appointment.pet.pet_name)) ||
    "Unknown Pet";

  const service = appointment.appointment_reason ||
    appointment.service_type_name||
    "General Consultation";

  const canEdit = appointment.request === 'pending' && appointment.status !== 'overdue';

  return (
    <div className="modal active" onClick={onClose}>
      <div className="new-modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="new-modal-header">
          <h3 className="modal-title">Appointment Details</h3>
          <button className="modal-close" onClick={onClose}>&times;</button>
        </div>
        
        <div className="modal-body">
          <div className="appointment-details-modal">
            <div className="detail-section">
              <div className="detail-grid">
                <div className="detail-item">
                  <span className="detail-label">Pet:</span>
                  <span className="detail-value">{petName}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Service:</span>
                  <span className="detail-value">{service}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Date:</span>
                  <span className="detail-value">{formatDate(appointment.date)}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Time:</span>
                  <span className="detail-value">{formatTime(appointment.prefTime)}</span>
                </div>
              </div>
            </div>

            <div className="detail-section">
              <h4>Status Information</h4>
              <div className="status-display">
                <div className="badges-container" style={{ marginBottom: '10px' }}>
                  {getAppointmentBadges(appointment)}
                </div>
                <div className="status-explanation-full">
                  {getStatusExplanation(appointment)}
                </div>
              </div>
            </div>

            {appointment.comments && (
              <div className="detail-section">
                <h4>Staff Remarks</h4>
                <div className="comments-box">
                  {appointment.comments}
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="modal-actions close-appointment-details">
          {/* Only show Edit if appointment is under review */}
          {canEdit && onEdit && (
            <button
              className="btn-edit"
              onClick={() => onEdit(appointment)}
            >
              Edit
            </button>
          )}
          
          <button className="btn-btn" onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  )
}

export default AppointmentDetailsModal