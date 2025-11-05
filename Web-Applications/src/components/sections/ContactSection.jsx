import React from 'react';

function ContactSection() {
    return (
        <section className="contact" id="contact">
        <h1>CONTACT US</h1>
        
        <div className="contact-container">
            <div className="contact-info">
            <div className="dog-image-container">
                <img src="/assets/images/pets/dog1.png" alt="Dog" />
            </div>
            
            <div className="contact-details">
                <div className="email-contact">
                <img src="/assets/icons/FACEBOOK.png" alt="clinic" />
                <span>PETMATE ANIMAL CLINIC</span>
                </div>

                <div className="social-contact">
                <img src="/assets/icons/Email.png" alt="email" />
                <span>petmate@gmail.com</span>
                </div>
            </div>
            </div>
            
            <div className="contact-form">
            <div className="form-row">
                <div className="form-group">
                <label htmlFor="name">Name</label>
                <input type="text" id="name" name="name" />
                </div>
                
                <div className="form-group">
                <label htmlFor="email">Email</label>
                <input type="email" id="email" name="email" />
                </div>
            </div>
            
            <div className="form-group">
                <label htmlFor="message">Message</label>
                <textarea id="message" name="message" rows="9"></textarea>
            </div>
            
            <button className="send-message-btn">SEND MESSAGE</button>
            </div>
        </div>
        </section>
    );
}

export default ContactSection;