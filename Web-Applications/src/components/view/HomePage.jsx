import React from 'react';
import { Link } from 'react-router-dom';
import LoginModal from "../modals/LoginModal";


function LandingPage() {
    return (
        <section className="home section" id="home">
        <div className="home-container">
            <div className="doctor-image">
            <img src="/assets/images/misc/Doctor.png" alt="Veterinarian" />
            </div>
            <div className="content">
            <h1>Your pet's health<br />is our priority.</h1>
            <p>Expert care, advanced treatments,<br />and a loving touch for your pets.<br />Keeping tails wagging and hearts happy!</p>
            
            <div className="action-buttons">
                <Link to="/book-now" className="btn btn-primary">BOOK NOW</Link>
                <Link to="/manage-booking" className="btn btn-secondary">MANAGE APPOINTMENT</Link>
            </div>
            </div>
        </div>
        </section>
    );
}

export default LandingPage;