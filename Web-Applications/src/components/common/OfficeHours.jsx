import React, { useState, useEffect } from "react";
import AOS from "aos";
import "aos/dist/aos.css";
import { apiFetch } from '../../config/api';

const DAY_ORDER = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];

const OfficeHours = () => {
    const [officeHours, setOfficeHours] = useState([]);
    const [orderedHours, setOrderedHours] = useState([]); // <-- fixed Mon-Sun, 1 row per day
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchOfficeHours();

        AOS.init({
            once: false,
            duration: 1000,
            easing: "ease-in-out",
        });
    }, []);

    useEffect(() => {
        if (!isLoading) {
            AOS.refresh();
        }
    }, [isLoading]);

    const fetchOfficeHours = async () => {
        try {
            setIsLoading(true);
            const response = await apiFetch('/api/office-hours/');
            if (!response.ok) {
                throw new Error('Failed to fetch office hours');
            }
            const data = await response.json();

            setOfficeHours(data);
            setOrderedHours(buildOrderedHours(data)); // <-- always Mon-Sun, never grouped
        } catch (err) {
            console.error('Error fetching office hours:', err);
            setError('Unable to load office hours. Please try again later.');
        } finally {
            setIsLoading(false);
        }
    };

    // Always return 7 entries (Mon-Sun). Same hours won't be merged.
    const buildOrderedHours = (hours) => {
        const byDay = new Map();

        for (const h of (hours || [])) {
            const dayKey = String(h?.day || '').toLowerCase().trim();
            if (!dayKey) continue;

            // If duplicates exist per day, keep the first one (change if you prefer last one).
            if (!byDay.has(dayKey)) byDay.set(dayKey, h);
        }

        return DAY_ORDER.map((day) => {
            const entry = byDay.get(day) || { day, status: 'closed', start_time: null, end_time: null };
            return {
                day,
                label: getFullDayName(day),
                displayTime: formatDisplayTime(entry.status, entry.start_time, entry.end_time),
            };
        });
    };

    const getFullDayName = (dayCode) => {
        const dayMap = {
            monday: 'Monday',
            tuesday: 'Tuesday',
            wednesday: 'Wednesday',
            thursday: 'Thursday',
            friday: 'Friday',
            saturday: 'Saturday',
            sunday: 'Sunday'
        };
        const key = String(dayCode || '').toLowerCase();
        return dayMap[key] || (String(dayCode || '').charAt(0).toUpperCase() + String(dayCode || '').slice(1));
    };

    const formatDisplayTime = (status, startTime, endTime) => {
        if (status === 'closed') return 'Closed';
        if (status === 'appointment_only') return 'Appointment Only';
        if (!startTime || !endTime) return 'Appointment Only';

        const start = formatTimeForDisplay(startTime);
        const end = formatTimeForDisplay(endTime);
        return `${start} - ${end}`;
    };

    const formatTimeForDisplay = (timeString) => {
        if (!timeString) return '';

        try {
            const [hours, minutes] = String(timeString).split(':').slice(0, 2);
            const hour = parseInt(hours, 10);
            const minute = parseInt(minutes, 10);

            const ampm = hour >= 12 ? 'PM' : 'AM';
            const displayHour = hour % 12 || 12;
            const displayMinute = minute.toString().padStart(2, '0');

            return `${displayHour}:${displayMinute} ${ampm}`;
        } catch (error) {
            return timeString;
        }
    };

    if (isLoading) {
        return (
            <section className="hours" id="hours" data-aos="fade-up">
                <div className="container">
                    <h1 className="section-title" data-aos="fade-down">OFFICE HOURS</h1>
                    <div className="hours-container" data-aos="fade-up">
                        <div className="hours-visual" data-aos="zoom-in">
                            <div className="clock-icon" data-aos="fade-right">
                                <i className="far fa-clock"></i>
                            </div>
                            <p>Loading office hours...</p>
                        </div>
                    </div>
                </div>
            </section>
        );
    }

    if (error) {
        return (
            <section className="hours" id="hours" data-aos="fade-up">
                <div className="container">
                    <h1 className="section-title" data-aos="fade-down">OFFICE HOURS</h1>
                    <div className="hours-container" data-aos="fade-up">
                        <div className="hours-visual" data-aos="zoom-in">
                            <div className="clock-icon" data-aos="fade-right">
                                <i className="far fa-clock"></i>
                            </div>
                            <p className="text-error">{error}</p>
                        </div>
                    </div>
                </div>
            </section>
        );
    }

    return (
        <section className="hours" id="hours">
            <div className="container">
                <h1 className="section-title" data-aos="fade-down">OFFICE HOURS</h1>
                <div className="hours-container">
                    <div className="hours-visual">
                        <div className="clock-icon" data-aos="fade-right">
                            <i className="far fa-clock"></i>
                        </div>
                        <div className="hours-text" data-aos="fade-left">
                            <h3>Visit Us Today</h3>
                            <p>We're here to care for your pets</p>
                        </div>

                        <ul className="hours-list">
                            {orderedHours.map((item, index) => (
                                <li
                                    key={item.day}
                                    data-aos="fade-up"
                                    data-aos-delay={index * 100}
                                >
                                    <span className="day">{item.label}</span>
                                    <span>{item.displayTime}</span>
                                </li>
                            ))}
                        </ul>

                    </div>
                </div>
            </div>
        </section>
    );
};

export default OfficeHours;