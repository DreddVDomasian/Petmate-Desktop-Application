import { useState } from 'react'
import TabContent from './TabContent'

const ProfileContent = ({ 
  onOpenModal, 
  pets,           // Receive from props
  appointments,   // Receive from props
  loading,        // Receive from props
  onRefresh       // Receive from props
}) => {
  const [activeTab, setActiveTab] = useState('pets')
  const [selectedPet, setSelectedPet] = useState(null)
  const [selectedAppointment, setSelectedAppointment] = useState(null)

  // Handle pet details view
  const handleViewPetDetails = (pet) => {
    setSelectedPet(pet)
    console.log('View pet details:', pet)
  }

  // Handle appointment details view
  const handleViewAppointmentDetails = (appointment) => {
    setSelectedAppointment(appointment)
    console.log('View appointment details:', appointment)
  }

  return (
    <div className="container">
      <div className="profile-content">
        <div className="profile-header">
          <h1 className="profile-title">My Profile</h1>
          <div>
            <button className="btn new-btn-primary" onClick={() => onOpenModal('addPet')}>
              <i className="fas fa-plus"></i> Add New Pet
            </button>
          </div>
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
          pets={pets}
          appointments={appointments}
          onOpenModal={onOpenModal}
          loading={loading}
          onRefresh={onRefresh}
          onViewPetDetails={handleViewPetDetails}
          onViewAppointmentDetails={handleViewAppointmentDetails}
        />
      </div>
    </div>
  )
}

export default ProfileContent