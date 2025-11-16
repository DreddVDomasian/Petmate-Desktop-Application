import React, { useState } from 'react';
import axios from 'axios';

export default function ContactSection() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [isSending, setIsSending] = useState(false); // prevent duplicate sends

    const getCookie = (name) => {
        const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return m ? decodeURIComponent(m.pop()) : null;
    };

    const handleSend = async () => {
        if (isSending) return; // already sending, ignore duplicate clicks

        try {
            setIsSending(true);

            // Make sure CSRF cookie is set by calling endpoint (server returns/sets cookie)
            await axios.get("http://localhost:8000/api/csrf/", { withCredentials: true });

            const csrf = getCookie("csrftoken") || getCookie("csrf") || getCookie("XSRF-TOKEN");

            const res = await axios.post(
                "http://127.0.0.1:8000/api/contact-us_message/",
                { name, email, message },
                {
                    withCredentials: true,
                    headers: { "X-CSRFToken": csrf }
                }
            );

            alert(res.data.message);
            setName("");
            setEmail("");
            setMessage("");
        } catch (err) {
            console.error(err);
            const errMsg = err.response?.data?.error || "Failed to send message. Please try again.";
            alert(errMsg);
        } finally {
            setIsSending(false);
        }
    };

    return (
        <section className="contact" id="contact">
            <h1>CONTACT US</h1>
            <div className="contact-container">
                <div className="contact-info">
                    <div className="logo-image-container">
                        <img src="/assets/images/logo/PETMATE LOGO.png" alt="PetMate Logo" />
                    </div>
                    <div className="contact-details">
                        <div className="email-contact">
                            <img src="/assets/icons/FACEBOOK.png" alt="clinic" />
                            <span>PETMATE ANIMAL CLINIC</span>
                        </div>
                        <div className="social-contact">
                            <img src="/assets/icons/Email.png" alt="email" />
                            <span>petmateanimalclinic@gmail.com</span>
                        </div>
                    </div>
                </div>
                <div className="contact-form">
                    <div className="form-row">
                        <div className="form-group">
                            <label htmlFor="name">Name</label>
                            <input
                                type="text"
                                id="name"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="email">Email</label>
                            <input
                                type="email"
                                id="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>
                    </div>
                    <div className="form-group">
                        <label htmlFor="message">Message</label>
                        <textarea
                            id="message"
                            rows="9"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                        ></textarea>
                    </div>
                    <button
                        className="send-message-btn"
                        onClick={handleSend}
                        disabled={isSending}
                        aria-busy={isSending}
                    >
                        {isSending ? "SENDING..." : "SEND MESSAGE"}
                    </button>
                </div>
            </div>
        </section>
    );
}
