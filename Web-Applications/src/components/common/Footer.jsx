import React from 'react';

function Footer() {
    return (
        <footer>
        <div className="container">
            <div className="footer-content">
                <div className="footer-column">
                    <h3>PetMate Animal Clinic</h3>
                    <p>Your trusted partner in pet healthcare. We provide compassionate, comprehensive veterinary care for your beloved companions.</p>
                    <div className="social-links">
                        <a
                            href="https://www.facebook.com/PetmaleAnimalClinic"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            <i className="fab fa-facebook-f"></i>
                        </a>
                    </div>
                </div>
                <div className="footer-column">
                    <h3>Quick Links</h3>
                    <ul className="footer-links">
                        <li><a href="#home">Home</a></li>
                        <li><a href="#about">About Us</a></li>
                        <li><a href="#services">Services</a></li>
                        <li><a href="#hours">Office Hours</a></li>
                        <li><a href="#contact">Contact Us</a></li>
                    </ul>
                </div>
                
            </div>
            <div className="copyright">
                <p>&copy; 2023 PetMate Animal Clinic. All rights reserved.</p>
            </div>
        </div>
    </footer>
    );
    }

export default Footer;