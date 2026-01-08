import React, { useState, useEffect } from "react";
import AOS from "aos";
import "aos/dist/aos.css";
import { apiFetch } from '../../config/api';

const OfficeHours = () => {
    const [officeHours, setOfficeHours] = useState([]);
    const [groupedHours, setGroupedHours] = useState([]);
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
            groupOfficeHours(data);
        } catch (err) {
            console.error('Error fetching office hours:', err);
            setError('Unable to load office hours. Please try again later.');
        } finally {
            setIsLoading(false);
        }
    };

    const groupOfficeHours = (hours) => {
        const originalOrder = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];

        // Sort by weekday order first (Monday always comes first).
        const sortedByDay = [...hours].sort((a, b) => {
            const aIdx = originalOrder.indexOf(String(a.day || '').toLowerCase());
            const bIdx = originalOrder.indexOf(String(b.day || '').toLowerCase());
            // Unknown days go last.
            const aSafe = aIdx === -1 ? 999 : aIdx;
            const bSafe = bIdx === -1 ? 999 : bIdx;
            return aSafe - bSafe;
        });

        // Group by (status + time range) but preserve the first-seen ordering by day.
        const groupsByKey = new Map();
        const keysInOrder = [];

        for (const hour of sortedByDay) {
            const status = hour.status;
            const start = hour.start_time || '';
            const end = hour.end_time || '';
            const key = `${String(status)}|${String(start)}|${String(end)}`;

            if (!groupsByKey.has(key)) {
                groupsByKey.set(key, {
                    days: [],
                    status,
                    start_time: hour.start_time,
                    end_time: hour.end_time,
                });
                keysInOrder.push(key);
            }

            const group = groupsByKey.get(key);
            group.days.push(getFullDayName(hour.day));
        }

        const firstDayIndex = (g) => {
            const indices = (g.days || [])
                .map((d) => originalOrder.indexOf(String(d || '').toLowerCase()))
                .filter((i) => i !== -1);
            return indices.length ? Math.min(...indices) : 999;
        };

        const groups = keysInOrder
            .map((key) => groupsByKey.get(key))
            // Keep groups ordered by their earliest weekday (Monday first).
            .sort((a, b) => firstDayIndex(a) - firstDayIndex(b))
            .map((g) => formatGroup(g, sortedByDay));

        setGroupedHours(groups);
    };

    const formatGroup = (group, allHours) => {
        if (group.days.length === 1) {
            return {
                label: group.days[0],
                status: group.status,
                time: formatTimeRange(group.status, group.start_time, group.end_time),
                displayTime: formatDisplayTime(group.status, group.start_time, group.end_time)
            };
        }

        
        const days = group.days;
        const originalOrder = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];

        
        days.sort((a, b) => originalOrder.indexOf(a.toLowerCase()) - originalOrder.indexOf(b.toLowerCase()));

        
        const ranges = [];
        let startIndex = 0;

        for (let i = 0; i < days.length; i++) {
            const currentIndex = originalOrder.indexOf(days[i].toLowerCase());
            const prevIndex = i > 0 ? originalOrder.indexOf(days[i - 1].toLowerCase()) : null;

            if (prevIndex !== null && currentIndex !== prevIndex + 1) {
                
                ranges.push(days.slice(startIndex, i));
                startIndex = i;
            }
        }
        ranges.push(days.slice(startIndex));

        
        const rangeLabels = ranges.map(range => {
            if (range.length === 1) return range[0];
            if (range.length === 2) return `${range[0]} & ${range[1]}`;
            return `${range[0]} - ${range[range.length - 1]}`;
        });

        const label = rangeLabels.join(', ');

        return {
            label,
            status: group.status,
            time: formatTimeRange(group.status, group.start_time, group.end_time),
            displayTime: formatDisplayTime(group.status, group.start_time, group.end_time)
        };
    };

    const getFullDayName = (dayCode) => {
        const dayMap = {
            'monday': 'Monday',
            'tuesday': 'Tuesday',
            'wednesday': 'Wednesday',
            'thursday': 'Thursday',
            'friday': 'Friday',
            'saturday': 'Saturday',
            'sunday': 'Sunday'
        };
        return dayMap[dayCode] || dayCode.charAt(0).toUpperCase() + dayCode.slice(1);
    };

    const formatTimeRange = (status, startTime, endTime) => {
        if (status === 'closed') return 'Closed';
        if (status === 'appointment_only') return 'Appointment Only';
        if (!startTime || !endTime) return 'Appointment Only';

        const start = formatTimeForDisplay(startTime);
        const end = formatTimeForDisplay(endTime);
        return `${start} - ${end}`;
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
            const [hours, minutes] = timeString.split(':').slice(0, 2);
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

    
    const hasEmergency = officeHours.some(hour =>
        hour.day === 'sunday' && hour.status === 'appointment_only'
    );

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
                            {groupedHours.map((group, index) => (
                                <li 
                                    key={index}
                                    data-aos="fade-up"
                                    data-aos-delay={index * 100} 
                                >
                                    <span className="day">{group.label}</span>
                                    <span>{group.displayTime}</span>
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