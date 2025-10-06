import React from 'react';

function AboutSection() {
    return (
        <section className="about section" id="about">
        <h1>ABOUT US</h1>
        <div className="about-content">
            <div className="about-text">
            <h3>ABOUT OUR<br />VETERINARY CLINIC</h3>
            <p>At <b style={{color: '#ff8c00'}}>PetMate Animal Clinic</b>, we are dedicated to providing exceptional veterinary care for your beloved pets. 
                Our clinic offers a full range of medical, surgical, and wellness services to ensure the health and happiness of your furry companions. 
                With a team of experienced veterinarians and compassionate staff, 
                we strive to create a welcoming environment where pets receive the best possible care.
                From routine check-ups and vaccinations to emergency treatments and specialized services, we are committed to delivering high-quality, personalized care tailored to your pet's needs. At <b style={{color: '#ff8c00'}}>PetMate Animal Clinic</b>, 
                your pet's well-being is our top priority.</p>
            </div>
            <div className="about-image">
            <img src="/assets/dog3.png" alt="Dog" />
            </div>
        </div>
        </section>
    );
}

export default AboutSection;