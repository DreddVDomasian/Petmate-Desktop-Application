import React, { useState, useEffect } from 'react';
import { apiFetch } from '../../config/api';
import AOS from 'aos';
import 'aos/dist/aos.css'; // import AOS styles

function ServicesSection() {
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchServices();

        // Initialize AOS
        AOS.init({
            once: false,        // allows repeatable animations
            duration: 1000,     // default duration in ms
            durattion: 400,
        });

        // Refresh AOS after services load
        AOS.refresh();
    }, []);

    const fetchServices = async () => {
        try {
            const response = await apiFetch('/api/service-types/?is_active=true&no_pagination=true');
            const data = await response.json();
            const serviceData = Array.isArray(data) ? data : (data.results || []);

            const servicesWithIcons = serviceData.map(service => ({
                id: service.id,
                title: service.name,
                desc: service.description || 'Professional service for your pet',
                icon: getIconForService(service.name)
            }));

            setServices(servicesWithIcons);
            setLoading(false);
        } catch (err) {
            console.error('Error fetching services:', err);
            setError('Failed to load services');
            setLoading(false);
            setServices(getDefaultServices());
        }
    };

    const getIconForService = (serviceName) => {
        const serviceNameLower = serviceName.toLowerCase();
        if (serviceNameLower.includes('vaccin')) return 'fas fa-syringe';
        if (serviceNameLower.includes('wellness') || serviceNameLower.includes('check')) return 'fas fa-stethoscope';
        if (serviceNameLower.includes('dental') || serviceNameLower.includes('tooth')) return 'fas fa-tooth';
        if (serviceNameLower.includes('surgery')) return 'fas fa-user-doctor';
        if (serviceNameLower.includes('groom')) return 'fas fa-paw';
        if (serviceNameLower.includes('emergency')) return 'fas fa-ambulance';
        return 'fas fa-clinic-medical';
    };

    const getDefaultServices = () => [
        { icon: "fas fa-stethoscope", title: "Wellness Exams", desc: "Comprehensive physical examinations to assess your pet's overall health." },
        { icon: "fas fa-syringe", title: "Vaccinations", desc: "Essential vaccines to protect your pet from common diseases." },
        { icon: "fas fa-tooth", title: "Dental Care", desc: "Professional dental cleanings and oral health assessments." },
        { icon: "fas user-doctor", title: "Surgery", desc: "Safe surgical procedures with advanced monitoring equipment." },
        { icon: "fas fa-ambulance", title: "Emergency Care", desc: "24/7 emergency services for urgent medical situations." },
        { icon: "fas fa-paw", title: "Grooming", desc: "Professional grooming services to keep your pet looking their best." },
    ];

    if (loading) {
        return (
            <section className="services" id="services">
                <div className="container">
                    <h1 className="section-title" data-aos="fade-down" data-aos-duration="1000">OUR SERVICES</h1>
                    <div className="loading">Loading services...</div>
                </div>
            </section>
        );
    }

    if (error && services.length === 0) {
        return (
            <section className="services" id="services">
                <div className="container">
                    <h1 className="section-title" data-aos="fade-down" data-aos-duration="1000">OUR SERVICES</h1>
                    <div className="error">{error}</div>
                </div>
            </section>
        );
    }

    return (
        <section className="services" id="services">
            <div className="container">
                <h1 className="section-title" data-aos="fade-down" data-aos-duration="1000">OUR SERVICES</h1>
                <div className="services-grid">
                    {services.map((service, index) => (
                        <div
                            className="service-card"
                            key={service.id || service.title}
                            data-aos="fade-up"
                            data-aos-duration="400"
                            data-aos-delay={index * 100} // stagger effect per card
                        >
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
