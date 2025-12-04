import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ServicesSection() {
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchServices();
    }, []);

    const fetchServices = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/service-types/?is_active=true');
            const serviceData = response.data.results || response.data;
            
            // Map API data to include icons based on service name
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
            
            // Fallback to default services if API fails
            setServices(getDefaultServices());
        }
    };

    // Function to map service names to icons
    const getIconForService = (serviceName) => {
        const serviceNameLower = serviceName.toLowerCase();
        
        // Mapping of keywords to Font Awesome icons
        if (serviceNameLower.includes('vaccin')) return 'fas fa-syringe';
        if (serviceNameLower.includes('wellness') || serviceNameLower.includes('check')) return 'fas fa-stethoscope';
        if (serviceNameLower.includes('dental') || serviceNameLower.includes('tooth')) return 'fas fa-tooth';
        if (serviceNameLower.includes('surgery')) return 'fas fa-user-doctor';
        if (serviceNameLower.includes('groom')) return 'fas fa-paw';
        if (serviceNameLower.includes('emergency')) return 'fas fa-ambulance';
        if (serviceNameLower.includes('deworm')) return 'fas fa-bug';
        if (serviceNameLower.includes('tick') || serviceNameLower.includes('flea')) return 'fas fa-spider';
        if (serviceNameLower.includes('consult')) return 'fas fa-comment-medical';
        if (serviceNameLower.includes('blood') || serviceNameLower.includes('test') || serviceNameLower.includes('lab')) return 'fas fa-vial';
        if (serviceNameLower.includes('pregn')) return 'fas fa-baby';
        if (serviceNameLower.includes('x-ray') || serviceNameLower.includes('xray')) return 'fas fa-x-ray';
        if (serviceNameLower.includes('ultrasound')) return 'fas fa-wave-square';
        if (serviceNameLower.includes('microchip')) return 'fas fa-microchip';
        if (serviceNameLower.includes('nutrition')) return 'fas fa-apple-alt';
        if (serviceNameLower.includes('behavior')) return 'fas fa-brain';
        if (serviceNameLower.includes('boarding') || serviceNameLower.includes('hotel')) return 'fas fa-bed';
        
        // Default icons for common service categories
        if (serviceNameLower.includes('care') || serviceNameLower.includes('health')) return 'fas fa-heartbeat';
        if (serviceNameLower.includes('exam') || serviceNameLower.includes('checkup')) return 'fas fa-stethoscope';
        if (serviceNameLower.includes('treatment')) return 'fas fa-first-aid';
        
        // Default icon if no match
        return 'fas fa-clinic-medical';
    };

    // Fallback default services if API fails
    const getDefaultServices = () => {
        return [
            { icon: "fas fa-stethoscope", title: "Wellness Exams", desc: "Comprehensive physical examinations to assess your pet's overall health." },
            { icon: "fas fa-syringe", title: "Vaccinations", desc: "Essential vaccines to protect your pet from common diseases." },
            { icon: "fas fa-tooth", title: "Dental Care", desc: "Professional dental cleanings and oral health assessments." },
            { icon: "fas user-doctor", title: "Surgery", desc: "Safe surgical procedures with advanced monitoring equipment." },
            { icon: "fas fa-ambulance", title: "Emergency Care", desc: "24/7 emergency services for urgent medical situations." },
            { icon: "fas fa-paw", title: "Grooming", desc: "Professional grooming services to keep your pet looking their best." },
        ];
    };

    if (loading) {
        return (
            <section className="services" id="services">
                <div className="container">
                    <h1 className="section-title">OUR SERVICES</h1>
                    <div className="loading">Loading services...</div>
                </div>
            </section>
        );
    }

    if (error && services.length === 0) {
        return (
            <section className="services" id="services">
                <div className="container">
                    <h1 className="section-title">OUR SERVICES</h1>
                    <div className="error">{error}</div>
                </div>
            </section>
        );
    }

    return (
        <section className="services" id="services">
            <div className="container">
                <h1 className="section-title">OUR SERVICES</h1>
                <div className="services-grid">
                    {services.map((service) => (
                        <div className="service-card" key={service.id || service.title}>
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