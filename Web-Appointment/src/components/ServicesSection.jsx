import React from 'react';
import ServiceCard from './ServiceCard';

function ServicesSection() {
    const services = [
        {
        image: "/assets/surgery.png",
        title: "SURGERY",
        description: "At PetMate Animal Clinic, we provide expert surgical care with precision and compassion, ensuring your pet receives the best treatment for a speedy and safe recovery."
        },

        {
        image: "/assets/vaccination.png",
        title: "VACCINATIONS",
        description: "Protect your pet with our comprehensive vaccination services. We offer all core and lifestyle vaccines to keep your furry friend safe from preventable diseases."
        },

        {
        image: "/assets/deworming.png",
        title: "DEWORMING",
        description: "Professional deworming services to keep your pet healthy, protected, and parasite-free. From regular treatments to expert care, we ensure your pet stays safe and well."
        },

        {
        image: "/assets/pet-flea-tick-prevention 1.png",
        title: "TICK & FLEA PREVENTION",
        description: "Complete tick and flea prevention services, including treatments and protection plans, to keep your pet comfortable, healthy, and free from parasites."
        },

        {
        image: "/assets/testing-diagnosis 1.png",
        title: "DIAGNOSTIC AND LABORATORY",
        description: "Comprehensive diagnostic and laboratory services to accurately assess your pet's health. From blood tests to imaging, we provide essential insights for effective treatment."
        },
        
        {
        image: "/assets/consultation.png",
        title: "CONSULTATION",
        description: "Expert veterinary consultations for all your pet health concerns. Our experienced vets provide thorough examinations and personalized care plans."
        }
    ];

    return (
        <section className="services" id="services">
        <h1>SERVICES</h1>
        <div className="card-container">
            {services.map((service, index) => (
            <ServiceCard
                key={index}
                image={service.image}
                title={service.title}
                description={service.description}
            />
            ))}
        </div>
        <div className="below-image">
            <img src="/assets/dog2.png" alt="Dog" />
        </div>
        </section>
    );
}

export default ServicesSection;