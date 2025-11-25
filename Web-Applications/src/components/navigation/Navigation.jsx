import React, { useState } from 'react';
import LoginModal from "../modals/LoginModal";
import SignupModal from "../modals/SignupModal";

const Navigation = () => {

    // STATE FOR LOGIN MODAL
    const [showLogin, setShowLogin] = useState(false);
    const [showSignup, setShowSignup] = useState(false);

    const [isMenuActive, setIsMenuActive] = useState(false);

    const toggleMenu = () => {
        setIsMenuActive(!isMenuActive);
    };

    const closeMenu = () => {
        setIsMenuActive(false);
    };

    return (
        <>
        <header>
        <div className="container">
            <nav className="nav" id="nav">
                <div className="logo" >
                    <img src="/assets/images/logo/PETMATE LOGO.png" alt="PetMate Logo" />
                </div>

            <ul className={`nav-links ${isMenuActive ? 'active' : ''}`}>
                <li><a href="#home" onClick={closeMenu}>Home</a></li>
                <li><a href="#about" onClick={closeMenu}>About</a></li>
                <li><a href="#services" onClick={closeMenu}>Services</a></li>
                {/* <li><a href="#office-hours" onClick={closeMenu}>Hours</a></li> */}
                <li><a href="#contact" onClick={closeMenu}>Contact</a></li>
                <li>
                    <a href="#" className="login-btn" onClick={() => { closeMenu(); setShowLogin(true); }}>
                    LOG IN
                    </a>
                </li>
            </ul>

            {/* FOR MOBILE  */}
            <div className="mobile-menu" onClick={toggleMenu}>
                <i className="fas fa-bars"></i>
            </div>
            </nav>
            
            {/* Modals */}
            <LoginModal
                visible={showLogin}
                onClose={() => setShowLogin(false)}
                onOpenSignup={() => {
                setShowLogin(false);
                setShowSignup(true);
                }}
            />
            <SignupModal
                visible={showSignup}
                onClose={() => setShowSignup(false)}
                onOpenLogin={() => {
                setShowSignup(false);
                setShowLogin(true);
                }}
            />
        </div>
        </header>
        </>
    );
};

export default Navigation;