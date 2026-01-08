import React, { useEffect, useState } from 'react';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { apiFetch, readJsonSafe } from '../../config/api';

function AboutSection() {
    const [about, setAbout] = useState({
        title: 'ABOUT OUR VETERINARY CLINIC',
        body: `At PetMate Animal Clinic,\nwe are dedicated to providing exceptional veterinary care for your beloved pets.\n\nOur clinic offers a full range of medical, surgical, and wellness services to ensure the health and happiness of your furry companions.\n\nFrom routine check-ups and vaccinations to emergency treatments and specialized services, we are committed to delivering high-quality, personalized care tailored to your pet\'s needs.`,
        image_url: '',
    });

    useEffect(() => {
        AOS.init({
            once: false,       //  allow animation to repeat
            duration: 1000,    // default duration 
        });
    }, []);

    useEffect(() => {
        let isMounted = true;
        (async () => {
            try {
                const res = await apiFetch('/api/about/', { method: 'GET' });
                if (!res.ok) return;
                const data = await readJsonSafe(res);
                if (isMounted && data) {
                    setAbout({
                        title: data.title || about.title,
                        body: data.body || about.body,
                        image_url: data.image_url || about.image_url,
                    });
                }
            } catch (_) {
                // ignore and keep defaults
            }
        })();
        return () => { isMounted = false; };
    }, []);

    return (
        <section className="about-section" id="about">
            <div className="container">
                <h1 className="section-title" data-aos="fade-down" data-aos-duration="1000">
                    {about.title}
                </h1>

                <div className="about-content">

                    <div className="about-text" data-aos="fade-up" data-aos-duration="2000">
                        {about.body.split(/\n{2,}/).map((para, idx) => (
                            <p key={idx}>{para}</p>
                        ))}
                    </div>

                    <div className="about-image" data-aos="fade-left" data-aos-duration="2000">
                        {about.image_url ? (
                            <img src={about.image_url} alt="About clinic" />
                        ) : (
                            <img src="https://images.unsplash.com/photo-1592194996308-7b43878e84a6?q=80&w=1974&auto=format&fit=crop" alt="About clinic" />
                        )}
                    </div>

                </div>                
            </div>
        </section>
    );
}

export default AboutSection;
