import React, { useState, useEffect } from 'react'; // Added useEffect
import { apiFetch } from '../../config/api';
import AOS from 'aos'; // Added AOS import
import 'aos/dist/aos.css'; // Added AOS CSS

export default function ContactSection() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [isSending, setIsSending] = useState(false);

    // 1. Initialize AOS
    useEffect(() => {
        AOS.init({
            duration: 1000,
            once: false,
            easing: "ease-in-out",
        });
    }, []);

    const getCookie = (name) => {
        const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return m ? decodeURIComponent(m.pop()) : null;
    };

    const handleSend = async () => {
        if (isSending) return; 

        try {
            setIsSending(true);
            await apiFetch('/api/csrf/');
            const csrf = getCookie("csrftoken") || getCookie("csrf") || getCookie("XSRF-TOKEN");

            const res = await apiFetch(
                "/api/contact-us_message/",
                {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrf || ''
                    },
                    body: JSON.stringify({ name, email, message })
                }
            );

            const raw = await res.text();
            let data = {};
            try {
                data = raw ? JSON.parse(raw) : {};
            } catch {
                data = {};
            }

            if (!res.ok) {
                const msg = data?.error || data?.message || `Failed to send message (HTTP ${res.status}).`;
                throw new Error(msg);
            }

            alert(data?.message || 'Message sent!');
            setName("");
            setEmail("");
            setMessage("");
        } catch (err) {
            console.error(err);
            const errMsg = err?.message || "Failed to send message. Please try again.";
            alert(errMsg);
        } finally {
            setIsSending(false);
        }
    };

    return (
    <section className="contact" id="contact" data-aos="fade-up">
        <div className="container">
            <h2 className="section-title" data-aos="fade-down">CONTACT US</h2>
            <div className="contact-content">
                
                {/* LEFT SIDE: Contact Info */}
                <div className="contact-info">
                    
                    <div className="contact-item" data-aos="fade-right" data-aos-delay="50">
                        <div className="contact-icon">
                            <i className="fas fa-map-marker-alt"></i>
                        </div>
                        <div>
                            <h3>Our Location</h3>
                            <p>Imus, Cavite</p>
                        </div>
                    </div>

                    <div className="contact-item" data-aos="fade-right" data-aos-delay="100">
                        <div className="contact-icon">
                            <i className="fas fa-phone"></i>
                        </div>
                        <div>
                            <h3>Phone Number</h3>
                            <p>0922-623-5529</p>
                        </div>
                    </div>

                    <div className="contact-item" data-aos="fade-right" data-aos-delay="250">
                        <div className="contact-icon">
                            <i className="fas fa-envelope"></i>
                        </div>
                        <div>
                            <h3>Email Address</h3>
                            <p>petmateanimalclinic@gmail.com</p>
                        </div>
                    </div>

                    <div className="contact-item" data-aos="fade-right" data-aos-delay="300">
                        <div className="contact-icon">
                            <i className="fas fa-clock"></i>
                        </div>
                        <div>
                            <h3>Emergency Contact</h3>
                            <p> 0922-623-5529 </p>
                        </div>
                    </div>
                    
                </div>

                {/* RIGHT SIDE: Form */}
                <div className="contact-form" data-aos="fade-left">
                    <form>
                        <div className="form-group" data-aos="fade-up" data-aos-delay="100">
                            <label htmlFor="name">Your Name</label>
                            <input 
                                type="text" 
                                id="name" 
                                className="form-control" 
                                placeholder="Enter your name"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                            />
                        </div>
                        <div className="form-group" data-aos="fade-up" data-aos-delay="200">
                            <label htmlFor="email">Your Email</label>
                            <input 
                                type="email" 
                                id="email" 
                                className="form-control" 
                                placeholder="Enter your email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>
                        <div className="form-group" data-aos="fade-up" data-aos-delay="300">
                            <label htmlFor="message">Your Message</label>
                            <textarea 
                                id="message" 
                                className="form-control" 
                                placeholder="Enter your message"
                                rows="9"
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                            ></textarea>
                        </div>
                        <button 
                            type="button" 
                            className="btn send-message-btn" 
                            onClick={handleSend}
                            disabled={isSending}
                            data-aos="zoom-in" 
                            data-aos-delay="50"
                        >
                            {isSending ? "SENDING..." : "SEND MESSAGE"}
                        </button>
                    </form>
                </div>
                
            </div>
        </div>
    </section>
    );
}