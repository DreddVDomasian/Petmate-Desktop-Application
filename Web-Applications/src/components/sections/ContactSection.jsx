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
        <div className="container">
            <h2 className="section-title">CONTACT US</h2>

            <div className="contact-content">
                <div className="contact-info">
                    
                    <div className="contact-item">
                        <div className="contact-icon">
                            <i className="fas fa-map-marker-alt"></i>
                        </div>
                        <div>
                            <h3>Our Location</h3>
                            <p>Imus, Cavite</p>
                        </div>
                    </div>
                    <div className="contact-item">
                        <div className="contact-icon">
                            <i className="fas fa-phone"></i>
                        </div>
                        <div>
                            <h3>Phone Number</h3>
                            <p>0922-623-5529</p>
                        </div>
                    </div>
                    <div className="contact-item">
                        <div className="contact-icon">
                            <i className="fas fa-envelope"></i>
                        </div>
                        <div>
                            <h3>Email Address</h3>
                            <p>petmateanimalclinic@gmail.com</p>
                        </div>
                    </div>
                    <div className="contact-item">
                        <div className="contact-icon">
                            <i className="fas fa-clock"></i>
                        </div>
                        <div>
                            <h3>Emergency Contact</h3>
                            <p> 0922-623-5529 </p>
                        </div>
                    </div>
                    
                </div>
                
            </div>
            
            <div className="contact-form">
                <form>
                    <div className="form-group">
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
                    <div className="form-group">
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
                    <div className="form-group">
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
                    >
                        {isSending ? "SENDING..." : "SEND MESSAGE"}
                    </button>
                </form>
            </div>
        </div>
    </section>
    );
}
