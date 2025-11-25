import React from "react";

const Officehours = () => {
    return (
        <section className="hours" id="hours">
            <div className="container">
                <h1 className="section-title">OFFICE HOURS</h1>
                <div className="hours-container">
                    <div className="hours-visual">
                        <div className="clock-icon">
                            <i className="far fa-clock"></i>
                        </div>
                        <div className="hours-text">
                            <h3>Visit Us Today</h3>
                            <p>We're here to care for your pets</p>
                        </div>
                        <ul className="hours-list">
                            <li>
                                <span className="day">Monday - Friday</span>
                                <span>8:00 AM - 6:00 PM</span>
                            </li>
                            <li>
                                <span className="day">Saturday</span>
                                <span>9:00 AM - 4:00 PM</span>
                            </li>
                            <li>
                                <span className="day">Sunday</span>
                                <span>Appointment Only</span>
                            </li>
                        </ul>
                        <div className="emergency-note">
                            <h4>Emergency Services</h4>
                            <p>Available 24/7 for urgent care needs</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Officehours;
