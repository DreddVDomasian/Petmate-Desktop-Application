import React from 'react';

function ServiceCard({ image, title, description }) {
    return (
        <div className="card">
        <div className="main">
            <img className="tokenImage" src={image} alt={title} />
            <h2>{title}</h2>
            <p className="description">{description}</p>
            <div className="tokenInfo">
            <div className="day">
                <ins>📍</ins>
                <p><a href="https://www.google.com/maps/place/Petmate+Animal+Clinic" target="_blank" rel="noopener noreferrer">PETMATE ANIMAL CLINIC</a></p>
            </div>
            </div>
            <hr />
        </div>
        </div>
    );
}

export default ServiceCard;