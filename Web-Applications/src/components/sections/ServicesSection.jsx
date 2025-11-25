import React from 'react';
// import ServiceCard from '../common/ServiceCard';

function ServicesSection() {
const services = [
    { icon: "fas fa-stethoscope", title: "Wellness Exams", desc: "Comprehensive physical examinations to assess your pet's overall health and detect potential issues early." },
    { icon: "fas fa-syringe", title: "Vaccinations", desc: "Essential vaccines to protect your pet from common diseases and keep them healthy throughout their life." },
    { icon: "fas fa-bone", title: "Dental Care", desc: "Professional dental cleanings, extractions, and oral health assessments to maintain your pet's dental hygiene." },
    { icon: "fas fa-clinic-medical", title: "Surgery", desc: "Safe surgical procedures performed in our state-of-the-art operating room with advanced monitoring equipment." },
    { icon: "fas fa-first-aid", title: "Emergency Care", desc: "24/7 emergency services for urgent medical situations that require immediate attention." },
    { icon: "fas fa-paw", title: "Grooming", desc: "Professional grooming services to keep your pet looking and feeling their best." },
];


    return (
        <section className="services" id="services">
        <div className="container">
            <h1 className="section-title">OUR SERVICES</h1>
            <div className="services-grid">
            {services.map((service, index) => (
                <div className="service-card" key={index}>
                <div className="service-icon">
                    <i className={service.icon}></i>
                </div>
                <h3>{service.title}</h3>
                <p>{service.desc}</p>
                </div>
            ))}
            </div>
            <div className="below-image">
                <img src="/assets/images/pets/dog2.png" alt="Dog" />
            </div>
        </div>
        

        </section>
    );
}

export default ServicesSection;


