import React from 'react';
import '../styles/Index.css';

// Import all components
import Navigation from '../components/navigation/Navigation';
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
        <Navigation />
        <HomePage />
        <AboutSection />
        <ServicesSection />
        <OfficeHours />
        <ContactSection />
        <Footer />
      </div>
    </>
  );
}

export default Index;