import { useState } from 'react'
import TabContent from './TabContent'

const ProfileContent = ({ 
  onOpenModal, 
  pets,           
  appointments,   
  loading,        
  onRefresh,
  onViewPetDetails,
  onViewAppointmentDetails, 
  activeTab,
  setActiveTab   // Receive from Dashboard
}) => {
  

  return (
    <div className="container">
      <div className="profile-content">
        <div className="profile-header">
          <h1 className="profile-title">My Profile</h1>
        </div>

        <div className="profile-tabs">
          <button
            className={`tab-btn ${activeTab === 'pets' ? 'active' : ''}`}
            onClick={() => setActiveTab('pets')}
          >
            My Pets
          </button>
          <button
            className={`tab-btn ${activeTab === 'appointments' ? 'active' : ''}`}
            onClick={() => setActiveTab('appointments')}
          >
            Appointments
          </button>
          <button
            className={`tab-btn ${activeTab === 'profile' ? 'active' : ''}`}
            onClick={() => setActiveTab('profile')}
          >
            Profile Info
          </button>
        </div>

        <TabContent 
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          pets={pets}
          appointments={appointments}
          onOpenModal={onOpenModal}
          loading={loading}
          onRefresh={onRefresh}
          onViewPetDetails={onViewPetDetails}
           onViewAppointmentDetails={onViewAppointmentDetails} // Pass the prop from Dashboard directly
        />
      </div>
    </div>
  )
}

export default ProfileContent