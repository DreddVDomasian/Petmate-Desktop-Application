import React, { useState, useEffect } from "react";
import { getCookie } from "../../utils/csrf";

export default function ViewAppointments() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
    if (!dateString) return "N/A";
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const formatTime = (timeString) => {
    if (!timeString) return "N/A";
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

  const getStatusBadge = (status) => {
    const statusText = String(status).charAt(0).toUpperCase() + String(status).slice(1);
    return <span className={`status-badge status-${status}`}>{statusText}</span>;
  };

  return (
    <div className="appointments-container">
      <h2 className="page-title">Appointments</h2>

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
            <div className="no-data">No appointments found.</div>
          ) : (
            appointments.map((appointment) => {
              const petName = appointment.pet_name ||
                (appointment.pet && (appointment.pet.petName || appointment.pet.pet_name)) ||
                "Unknown Pet";

              const service = appointment.appointment_reason ||
                appointment.service_name ||
                "General Consultation";

              const date = appointment.date ||
                appointment.appointment_datetime?.split(" ")[0] || "N/A";

              const time = appointment.prefTime ||
                (appointment.appointment_datetime?.includes(" ") 
                  ? appointment.appointment_datetime.split(" ")[1] 
                  : null) || "N/A";

              const status = appointment.status || "pending";
              const veterinarian = appointment.provider || "Not assigned";
              const bookingId = appointment.booking_id || "N/A";

              return (
                <div key={appointment.id || bookingId} className="appointment-card">
                  <div className="card-header">
                    <h3 className="pet-name">{petName}</h3>
                    {getStatusBadge(status)}
                  </div>

                  <div className="card-divider" />

                  <p><strong>Service:</strong> {service}</p>
                  <p><strong>Date:</strong> {formatDate(date)}</p>
                  <p><strong>Time:</strong> {formatTime(time)}</p>
                  <p><strong>Veterinarian:</strong> {veterinarian}</p>

                  <div className="card-actions">
                    <button
                      className="view-btn"
                      onClick={() =>
                        alert(
                          `Appointment Details:\n\nPet: ${petName}\nService: ${service}\nDate: ${formatDate(
                            date
                          )}\nTime: ${formatTime(time)}\nStatus: ${status}\nVeterinarian: ${veterinarian}\nBooking ID: ${bookingId}`
                        )
                      }
                    >
                      View Details
                    </button>
                    {appointment.comments && (
                      <button
                        className="comments-btn"
                        onClick={() => alert(`Comments:\n\n${appointment.comments}`)}
                      >
                        Remarks
                      </button>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>
      )}
    </div>
  );
}
