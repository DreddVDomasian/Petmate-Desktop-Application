import React, { useState, useEffect } from "react";
import AOS from "aos";
import "aos/dist/aos.css";

const OfficeHours = () => {
    const [officeHours, setOfficeHours] = useState([]);
    const [groupedHours, setGroupedHours] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    // 1. Initialize AOS and Fetch Data
    useEffect(() => {
        fetchOfficeHours();
        
        AOS.init({
            once: false, 
            duration: 1000,
            easing: "ease-in-out",
        });
    }, []);

    // 2. Refresh AOS when loading finishes
    // This ensures animations calculate correctly after data arrives from your API
    useEffect(() => {
        if (!isLoading) {
            AOS.refresh();
        }
    }, [isLoading]);

    const fetchOfficeHours = async () => {
        try {
            setIsLoading(true);
            const response = await fetch('/api/office-hours/'); // Adjust URL based on your Django settings
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
        const groups = [];
        let currentGroup = null;

        // Sort by status and times to group properly
        const sortedHours = [...hours].sort((a, b) => {
            if (a.status !== b.status) {
                return a.status.localeCompare(b.status);
            }
            if (a.start_time !== b.start_time) {
                if (!a.start_time) return 1;
                if (!b.start_time) return -1;
                return a.start_time.localeCompare(b.start_time);
            }
            if (a.end_time !== b.end_time) {
                if (!a.end_time) return 1;
                if (!b.end_time) return -1;
                return a.end_time.localeCompare(b.end_time);
            }
            return 0;
        });

        for (let i = 0; i < sortedHours.length; i++) {
            const hour = sortedHours[i];
            const dayName = getFullDayName(hour.day);

            // If current group exists and this hour can join it
            if (currentGroup && canJoinGroup(currentGroup, hour)) {
                currentGroup.days.push(dayName);
                currentGroup.endDayIndex = i;
            } else {
                // Start a new group
                if (currentGroup) {
                    groups.push(formatGroup(currentGroup, sortedHours));
                }

                currentGroup = {
                    days: [dayName],
                    status: hour.status,
                    start_time: hour.start_time,
                    end_time: hour.end_time,
                    startDayIndex: i,
                    endDayIndex: i
                };
            }
        }

        // Don't forget the last group
        if (currentGroup) {
            groups.push(formatGroup(currentGroup, sortedHours));
        }

        setGroupedHours(groups);
    };

    const canJoinGroup = (group, hour) => {
        // Can only join if status and times match
        if (group.status !== hour.status) return false;
        if (group.start_time !== hour.start_time) return false;
        if (group.end_time !== hour.end_time) return false;

        // Check if days are consecutive in the original order
        const originalOrder = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
        const groupLastDay = group.days[group.days.length - 1].toLowerCase();
        const newDay = getFullDayName(hour.day).toLowerCase();

        // Allow grouping even if not strictly consecutive
        return true; 
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

        // Try to create a compact range
        const days = group.days;
        const originalOrder = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];

        // Sort days in original order
        days.sort((a, b) => originalOrder.indexOf(a.toLowerCase()) - originalOrder.indexOf(b.toLowerCase()));

        // Find consecutive ranges
        const ranges = [];
        let startIndex = 0;

        for (let i = 0; i < days.length; i++) {
            const currentIndex = originalOrder.indexOf(days[i].toLowerCase());
            const prevIndex = i > 0 ? originalOrder.indexOf(days[i - 1].toLowerCase()) : null;

            if (prevIndex !== null && currentIndex !== prevIndex + 1) {
                // Not consecutive, end previous range
                ranges.push(days.slice(startIndex, i));
                startIndex = i;
            }
        }
        ranges.push(days.slice(startIndex));

        // Create labels for each range
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

    // Check if we have emergency services (sunday appointment only)
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
                                    data-aos-delay={index * 100} // This creates the staggered effect
                                >
                                    <span className="day">{group.label}</span>
                                    <span>{group.displayTime}</span>
                                </li>
                            ))}
                        </ul>
                        {hasEmergency && (
                            <div className="emergency-note" data-aos="fade-up" data-aos-delay={100}>
                                <h4>Emergency Services</h4>
                                <p>Available 24/7 for urgent care needs</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </section>
    );
};

export default OfficeHours;