import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './BookNow.css';
import BookingForm from '../../components/BookingForm';
import PageHeader from '../../components/PageHeader';


function BookNow() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    service: '',
    date: '',
    time: '',
    notes: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you would typically send the data to your backend
    console.log('Booking submitted:', formData);
    alert('Appointment booked successfully!');
    navigate('/manage-booking');
  };

  const handleBackClick = () => {
    navigate('/');
  };

  return (
    <div className="book-now-page">
      <PageHeader onBackClick={handleBackClick} />
      <BookingForm 
        formData={formData}
        handleChange={handleChange}
        handleSubmit={handleSubmit}
      />
    </div>
  );
}

export default BookNow;