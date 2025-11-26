import React from 'react';
import '../styles/Index.css';

// Import all components

import AboutSection from '../components/sections/AboutSection';
import ServicesSection from '../components/sections/ServicesSection';
import OfficeHours from '../components/common/OfficeHours';
import ContactSection from '../components/sections/ContactSection';
import Footer from '../components/common/Footer';
import HomePage from '../components/view/HomePage';

function Index() {
  return (
    <>
      <div className="index-page">
        <HomePage id="home" />
        <AboutSection id="about" />
        <ServicesSection id="services" /> 
        <OfficeHours id="hours" />
        <ContactSection id="contact" />
        <Footer />
      </div>
    </>
  );
}

export default Index;