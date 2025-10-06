import React from 'react';
import './Index.css';

// Import all components
import Navigation from '../../components/Navigation';
import HeroSection from '../../components/LandingPage';
import AboutSection from '../../components/AboutSection';
import ServicesSection from '../../components/ServicesSection';
import OfficeHours from '../../components/OfficeHours';
import ContactSection from '../../components/ContactSection';
import Footer from '../../components/Footer';
import LandingPage from '../../components/LandingPage';

function Index() {
  return (
    <div className="index-page"> 
      <Navigation />
      <LandingPage />
      <AboutSection />
      <ServicesSection />
      <OfficeHours />
      <ContactSection />
      <Footer />
    </div>
  );
}

export default Index;