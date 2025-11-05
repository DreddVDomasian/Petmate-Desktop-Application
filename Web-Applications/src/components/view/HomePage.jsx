import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import LoginModal from "../modals/LoginModal";
import SignupModal from "../modals/SignupModal";

function LandingPage() {
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);

  const openLogin = () => { setShowLogin(true); setShowSignup(false); };
  const closeLogin = () => setShowLogin(false);

  const openSignup = () => { setShowSignup(true); setShowLogin(false); };
  const closeSignup = () => setShowSignup(false);

  return (
    <section className="home section" id="home">
      <div className="home-container">
        <div className="doctor-image">
          <img src="/assets/images/misc/doc.png" alt="Veterinarian" />
        </div>
        <div className="content">
          <h1>Your pet's health<br />is our priority.</h1>
          <p>Expert care, advanced treatments,<br />and a loving touch for your pets.<br />Keeping tails wagging and hearts happy!</p>
          
          <div className="action-buttons">
            <button type="button" className="btn btn-primary" onClick={openLogin}>BOOK NOW</button>
            <Link to="#" className="btn btn-secondary">LEARN MORE</Link>
          </div>
        </div>
      </div>

      <LoginModal visible={showLogin} onClose={closeLogin} onOpenSignup={openSignup} />
      <SignupModal visible={showSignup} onClose={closeSignup} onOpenLogin={openLogin} />
    </section>
  );
}

export default LandingPage;