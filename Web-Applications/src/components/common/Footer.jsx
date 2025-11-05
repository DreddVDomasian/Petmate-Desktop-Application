import React from 'react';

function Footer() {
    return (
        <footer className="footer">
        <div className="footer-content">
            <div className="footer-left">
            <img src="/assets/images/logo/PETMATE LOGO.png" alt="PetMate Logo" className="footer-logo" />
            <p className="footer-description">Providing exceptional veterinary care with compassion and expertise for your beloved pets.</p>
            </div>
            
            <div className="footer-center">
            <h3>Quick Links</h3>
            <ul className="footer-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#contact">Contact Us</a></li>
            </ul>
            </div>
            
            <div className="footer-right">
            <h3>Contact Info</h3>
            <div className="contact-item">
                <img src="/assets/icons/Email.png" alt="Email" />
                <a href="mailto:petmate@gmail.com">petmate@gmail.com</a>
            </div>
            <div className="contact-item">
                <img src="/assets/icons/FACEBOOK.png" alt="Facebook" />
                <a href="https://www.facebook.com/PetmateAnimalClinic" target="_blank" rel="noopener noreferrer">Petmate Animal Clinic</a>
            </div>
            </div>
        </div>
        
        <div className="footer-bottom">
            <p>©2024 PetMate Animal Clinic. All rights reserved.</p>
            <a href="#nav" className="back-to-top">
            <img src="/assets/icons/up-arrow.png" alt="Back to Top" className="arrowup" />
            </a>
        </div>
        </footer>
    );
    }

export default Footer;