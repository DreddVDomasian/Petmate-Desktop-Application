import React, { useState } from 'react';
import LoginModal from "../modals/LoginModal";
import SignupModal from "../modals/SignupModal";

function HomePage() {
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);

  const openLogin = () => { setShowLogin(true); setShowSignup(false); };
  const closeLogin = () => setShowLogin(false);

  const openSignup = () => { setShowSignup(true); setShowLogin(false); };
  const closeSignup = () => setShowSignup(false);

  return (
    <section className="home-section" id="home">
      <div className="home-container">
        <div className="content-wrapper">

          <div className="doctor-image">
            <img src="/assets/images/misc/doc.png" alt="Veterinarian with dog" />
          </div>
        </div>

      </div>

      <LoginModal visible={showLogin} onClose={closeLogin} onOpenSignup={openSignup} />
      <SignupModal visible={showSignup} onClose={closeSignup} onOpenLogin={openLogin} />
    </section>
  );
}

export default HomePage;