import React from 'react';

function OfficeHours() {
    const hours = [
        { day: "Monday", time: "9:00 am - 6:00 pm" },
        { day: "Tuesday", time: "9:00 am - 6:00 pm" },
        { day: "Wednesday", time: "9:00 am - 6:00 pm" },
        { day: "Thursday", time: "9:00 am - 6:00 pm" },
        { day: "Friday", time: "9:00 am - 6:00 pm" },
        { day: "Saturday", time: "9:00 am - 6:00 pm" },
        { day: "Sunday", time: "By Appointment" }
    ];

    return (
        <section className="office-hours">
        <h1>Office Hours</h1>
        <div className="hours-container">
            {hours.map((item, index) => (
            <div key={index} className="day-column">
                <h3>{item.day}</h3>
                <p>{item.time}</p>
            </div>
            ))}
        </div>
        </section>
    );
}

export default OfficeHours;