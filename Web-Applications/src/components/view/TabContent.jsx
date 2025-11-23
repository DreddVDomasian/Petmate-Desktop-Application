import { useState } from 'react'
import PetCard from './PetCard'
import AppointmentCard from './AppointmentCard'

const TabContent = ({ 
  activeTab, 
  pets, 
  appointments, 
  onOpenModal, 
  loading, 
  onRefresh,
  onViewPetDetails,
  onViewAppointmentDetails 
}) => {
  const [selectedPet, setSelectedPet] = useState(null)
  const [selectedAppointment, setSelectedAppointment] = useState(null)

  // Handle pet card click - open details modal
  const handlePetClick = (pet) => {
    setSelectedPet(pet)
    if (onViewPetDetails) {
      onViewPetDetails(pet)
    }
  }

  // Handle appointment details view
  const handleAppointmentDetails = (appointment) => {
    setSelectedAppointment(appointment)
    if (onViewAppointmentDetails) {
      onViewAppointmentDetails(appointment)
    }
  }

  // Loading state component
  const LoadingState = () => (
    <div className="loading">
      <p>Loading...</p>
    </div>
  )

  // Empty state component for pets
  const EmptyPetsState = () => (
    <div className="empty-state">
      <img src="/assets/icons/dog-walking.gif" alt="No pets" className="empty-icon" />
      <h3>No Pets Yet</h3>
      <p>Add your first pet to get started</p>
      <button 
        className="btn btn-primary" 
        onClick={() => onOpenModal('addPet')}
        style={{ marginTop: '15px' }}
      >
        <i className="fas fa-plus"></i> Add Your First Pet
      </button>
    </div>
  )

  // Empty state component for appointments
  const EmptyAppointmentsState = () => (
    <div className="empty-state">
      <img src="/assets/icons/calendar-empty.gif" alt="No appointments" className="empty-icon" />
      <h3>No Appointments Yet</h3>
      <p>Schedule your first appointment to get started</p>
      <button 
        className="btn btn-primary" 
        onClick={() => onOpenModal('bookAppointment')}
        style={{ marginTop: '15px' }}
      >
        <i className="fas fa-calendar-plus"></i> Book Your First Appointment
      </button>
    </div>
  )

  return (
    <>
      {/* My Pets Tab */}
      <div className={`tab-content ${activeTab === 'pets' ? 'active' : ''}`} id="pets-tab">
        <div className="profile-card">
          <h3><i className="fas fa-paw"></i> My Pets</h3>
          <p>Manage your pets' information and view their medical history.</p>
          
          {/* Refresh Button */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <button 
              className="btn" 
              onClick={onRefresh}
              disabled={loading}
            >
              <i className="fas fa-sync-alt"></i> Refresh
            </button>
            <button 
              className="btn btn-primary" 
              onClick={() => onOpenModal('addPet')}
            >
              <i className="fas fa-plus"></i> Add New Pet
            </button>
          </div>

          {loading ? (
            <LoadingState />
          ) : pets.length === 0 ? (
            <EmptyPetsState />
          ) : (
            <div className="pets-grid">
              {pets.map(pet => (
                <PetCard 
                  key={pet.id} 
                  pet={pet} 
                  onClick={() => handlePetClick(pet)}
                />
              ))}
            </div>
          )}
        </div>
      </div>
      
      {/* Appointments Tab */}
      <div className={`tab-content ${activeTab === 'appointments' ? 'active' : ''}`} id="appointments-tab">
        <div className="profile-card">
          <div className="appointment-card-header">
            <h3><i className="fas fa-calendar-alt"></i> My Appointments</h3>
            <button 
              className="btn btn-primary" 
              onClick={() => onOpenModal('bookAppointment')}
            >
              <i className="fas fa-calendar-plus"></i> Book New Appointment
            </button>
          </div>

          {/* Refresh Button */}
          <div style={{ marginBottom: '20px' }}>
            <button 
              className="btn" 
              onClick={onRefresh}
              disabled={loading}
            >
              <i className="fas fa-sync-alt"></i> Refresh Appointments
            </button>
          </div>

          {loading ? (
            <LoadingState />
          ) : appointments.length === 0 ? (
            <EmptyAppointmentsState />
          ) : (
            <div className="appointments-list">
              {appointments.map(appointment => (
                <AppointmentCard 
                  key={appointment.id} 
                  appointment={appointment} 
                  onViewDetails={() => handleAppointmentDetails(appointment)}
                />
              ))}
            </div>
          )}
        </div>
      </div>
      
      {/* Profile Info Tab */}
      <div className={`tab-content ${activeTab === 'profile' ? 'active' : ''}`} id="profile-tab">
        <div className="profile-card">
          <h3><i className="fas fa-user"></i> Personal Information</h3>
          <div className="profile-info">
            <div className="info-item">
              <div className="info-label">Full Name</div>
              <div className="info-value">John Doe</div>
            </div>
            <div className="info-item">
              <div className="info-label">Email</div>
              <div className="info-value">john.doe@example.com</div>
            </div>
            <div className="info-item">
              <div className="info-label">Phone</div>
              <div className="info-value">(555) 123-4567</div>
            </div>
            <div className="info-item">
              <div className="info-label">Address</div>
              <div className="info-value">123 Main Street, City, State 12345</div>
            </div>
          </div>
          <button className="btn btn-primary">Edit Profile</button>
        </div>
        
        <div className="profile-card">
          <h3><i className="fas fa-shield-alt"></i> Account Security</h3>
          <div className="profile-info">
            <div className="info-item">
              <div className="info-label">Password</div>
              <div className="info-value">••••••••</div>
            </div>
          </div>
          <button className="btn">Change Password</button>
        </div>
      </div>
    </>
  )
}

export default TabContent