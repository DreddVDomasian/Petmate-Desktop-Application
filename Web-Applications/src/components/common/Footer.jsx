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
                
            </div>
            <div className="copyright">
                <p>&copy; 2026 PetMate Animal Clinic. All rights reserved.</p>
            </div>
        </div>
    </footer>
    );
    }

export default Footer;