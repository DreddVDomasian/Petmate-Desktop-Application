import React from 'react';

function AboutSection() {
    return (
        <section className="about-section" id="about">
            <div className="container">


                <h1 className="section-title">ABOUT OUR VETERINARY CLINIC</h1>
                <div className="about-content">

                    <div className="about-text">
                        <p>
                        At PetMate Animal Clinic, 
                        we are dedicated to providing exceptional veterinary care 
                        for your beloved pets. 
                        </p>

                        <p>
                        Our clinic offers a full range of medical, surgical, and wellness
                        services to ensure the health and happiness of your furry
                        companions. With a team of experienced veterinarians and
                        compassionate staff, we strive to create a welcoming environment
                        where pets receive the best possible care.
                        </p>

                        <p>
                        From routine check-ups and vaccinations to emergency treatments
                        and specialized services, we are committed to delivering
                        high-quality, personalized care tailored to your pet's needs. At
                        PetMate Animal Clinic, your pet's well-being is our top priority.
                        </p>
                    </div>

                    <div className="about-image">
                        <img src="https://plus.unsplash.com/premium_photo-1707353400249-1d96e1a7e0e6?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3Dttps://images.unsplash.com/photo-1592194996308-7b43878e84a6?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="PET DITO NAKALAGAY "/>
                    </div>

                </div>                
            </div>
        </section>
    );
}

export default AboutSection;


