import React from 'react';

function Footer() {
    return (
        <footer>
        <div className="container">
            <div className="footer-content">
                <div className="footer-column">
                    <h3>PetMate Animal Clinic</h3>
                    <p>Your trusted partner in pet healthcare. We provide compassionate, comprehensive veterinary care for your beloved companions.</p>
                    <div class="social-links">
                        <a href="#"><i class="fab fa-facebook-f"></i></a>
                        <a href="#"><i class="fab fa-twitter"></i></a>
                        {/* <!-- ADD NG SOCIALS NILA HERE --> */}
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