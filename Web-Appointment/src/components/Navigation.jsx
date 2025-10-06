import React, { useState } from "react";
import LoginModal from "./LoginModal";
import SignupModal from "./SignupModal";

function Navigation() {

    const [showLogin, setShowLogin] = useState(false);
    const [showSignup, setShowSignup] = useState(false);

    return (
    <>
      <nav>
        <div className="logo">
          <img src="/assets/PETMATE LOGO.png" alt="PetMate Logo" />
        </div>
        <ul>
          <li><a href="#home">HOME</a></li>
          <li><a href="#about">ABOUT</a></li>
          <li><a href="#services">SERVICES</a></li>
          <li><a href="#contact">CONTACT US</a></li>
          <li>
            <a href="#" className="login-btn" onClick={() => setShowLogin(true)}>
              LOG IN
            </a>
          </li>
        </ul>
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
    </>
  );
}

export default Navigation;
