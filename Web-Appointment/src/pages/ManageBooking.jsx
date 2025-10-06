import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/ManageBooking.css';

function ManageBooking() {
  const navigate = useNavigate();
  const [searchEmail, setSearchEmail] = useState('');
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(false);

  // Mock data - in real app, this would come from your backend
  const mockBookings = [
    {
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
      service: 'Consultation',
      date: '2025-10-15',
      time: '10:00',
      status: 'Confirmed'
    },
    {
      id: 2,
      name: 'Jane Smith',
      email: 'jane@example.com',
      service: 'Follow-up',
      date: '2025-10-16',
      time: '14:30',
      status: 'Pending'
    }
  ];

  const handleSearch = (e) => {
    e.preventDefault();
    setLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      const userBookings = mockBookings.filter(
        booking => booking.email.toLowerCase() === searchEmail.toLowerCase()
      );
      setBookings(userBookings);
      setLoading(false);
    }, 1000);
  };

  const handleCancel = (bookingId) => {
    if (window.confirm('Are you sure you want to cancel this appointment?')) {
      setBookings(bookings.filter(booking => booking.id !== bookingId));
      alert('Appointment cancelled successfully!');
    }
  };

  const handleReschedule = (bookingId) => {
    alert('Reschedule functionality would open a date/time picker here.');
    // In a real app, this would open a modal or navigate to a reschedule form
  };

  return (
    <div className="manage-booking-page">
      <header>
        <h1>Manage Your Bookings</h1>
        <button onClick={() => navigate('/')} className="back-btn">
          ← Back to Home
        </button>
      </header>

      <div className="search-section">
        <form onSubmit={handleSearch} className="search-form">
          <div className="form-group">
            <label htmlFor="searchEmail">Enter your email to view bookings:</label>
            <input
              type="email"
              id="searchEmail"
              value={searchEmail}
              onChange={(e) => setSearchEmail(e.target.value)}
              placeholder="your-email@example.com"
              required
            />
          </div>
          <button type="submit" className="search-btn" disabled={loading}>
            {loading ? 'Searching...' : 'Find My Bookings'}
          </button>
        </form>
      </div>

      {bookings.length > 0 && (
        <div className="bookings-section">
          <h2>Your Appointments</h2>
          <div className="bookings-list">
            {bookings.map(booking => (
              <div key={booking.id} className="booking-card">
                <div className="booking-info">
                  <h3>{booking.service}</h3>
                  <p><strong>Date:</strong> {new Date(booking.date).toLocaleDateString()}</p>
                  <p><strong>Time:</strong> {booking.time}</p>
                  <p><strong>Status:</strong> 
                    <span className={`status ${booking.status.toLowerCase()}`}>
                      {booking.status}
                    </span>
                  </p>
                </div>
                <div className="booking-actions">
                  <button 
                    onClick={() => handleReschedule(booking.id)}
                    className="btn btn-secondary"
                  >
                    Reschedule
                  </button>
                  <button 
                    onClick={() => handleCancel(booking.id)}
                    className="btn btn-danger"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {bookings.length === 0 && searchEmail && !loading && (
        <div className="no-bookings">
          <p>No bookings found for this email address.</p>
          <button 
            onClick={() => navigate('/book-now')} 
            className="btn btn-primary"
          >
            Book Your First Appointment
          </button>
        </div>
      )}

      <div className="help-section">
        <h3>Need Help?</h3>
        <p>If you're having trouble finding your booking, please contact us:</p>
        <ul>
          <li>Phone: (555) 123-4567</li>
          <li>Email: support@appointments.com</li>
        </ul>
      </div>
    </div>
  );
}

export default ManageBooking;