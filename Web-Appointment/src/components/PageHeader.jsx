import React from 'react';

function PageHeader({ onBackClick }) {
  return (
    <header>
      <h1>Book Your Appointment</h1>
      <button onClick={onBackClick} className="back-btn">
        ← Back to Home
      </button>
    </header>
  );
}

export default PageHeader;