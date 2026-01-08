import React, { useEffect, useState } from 'react';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { apiFetch, readJsonSafe, getApiUrl } from '../../config/api';

function AboutSection() {
    const [about, setAbout] = useState({
        // Editable headline (about-title)
        title: 'At PetMate Animal Clinic,\nwe are dedicated to providing exceptional veterinary care\nfor your beloved pets.',
        // Editable description (about-body)
        body: `Our clinic offers a full range of medical, surgical, and wellness
services to ensure the health and happiness of your furry
companions...

From routine check-ups and vaccinations to emergency treatments
and specialized services, we are committed to delivering
high-quality, personalized care tailored to your pet's needs.`,
        image_url: '',
    });

    useEffect(() => {
        AOS.init({
            once: false,       //  allow animation to repeat
            duration: 1000,    // default duration 
        });
    }, []);

    const resolvedImageSrc = (() => {
        if (!about.image_url) return '';
        // If backend returns a relative /media/... path, prefix with API base.
        if (typeof about.image_url === 'string' && about.image_url.startsWith('http')) return about.image_url;
        return getApiUrl(about.image_url);
    })();

    useEffect(() => {
        let isMounted = true;
        (async () => {
            try {
                const res = await apiFetch('/api/about/', { method: 'GET' });
                if (!res.ok) return;
                const data = await readJsonSafe(res);
                if (isMounted && data) {
                    setAbout((prev) => ({
                        title: data.title || prev.title,
                        body: data.body || prev.body,
                        image_url: data.image_url || prev.image_url,
                    }));
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
                    ABOUT OUR VETERINARY CLINIC
                </h1>

                <div className="about-content">

                    <div className="about-text" data-aos="fade-up" data-aos-duration="2000">
                        <p>
                            {String(about.title || '')
                                .split('\n')
                                .map((line, i) => (
                                    <React.Fragment key={i}>
                                        {line}
                                        {i < String(about.title || '').split('\n').length - 1 ? <br /> : null}
                                    </React.Fragment>
                                ))}
                        </p>

                        {String(about.body || '').split(/\n{2,}/).filter(Boolean).map((para, idx) => (
                            <p key={idx}>{para}</p>
                        ))}
                    </div>

                    <div className="about-image" data-aos="fade-left" data-aos-duration="2000">
                        {resolvedImageSrc ? (
                            <img src={resolvedImageSrc} alt="About clinic" />
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
