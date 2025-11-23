import { useState, useEffect } from 'react'
import { getCookie } from '../utils/csrf'
import TabContent from './TabContent'

const ProfileContent = ({ onOpenModal }) => {
  const [activeTab, setActiveTab] = useState('pets')
  const [pets, setPets] = useState([])
  const [appointments, setAppointments] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedPet, setSelectedPet] = useState(null)
  const [selectedAppointment, setSelectedAppointment] = useState(null)

  // COPY fetchUserPets FROM OLD ViewPets.jsx
  const fetchUserPets = async () => {
    try {
      const res = await fetch('/api/pets/', {
        credentials: 'include',
        headers: {
          'X-CSRFToken': getCookie('csrftoken') || ''
        }
      });

      if (res.ok) {
        const petsData = await res.json();
        setPets(petsData);
      } else {
        console.error('Failed to fetch pets');
      }
    } catch (error) {
      console.error('Error fetching pets:', error);
    } finally {
      setLoading(false);
    }
  };

  // COPY fetchAppointments FROM OLD ViewAppointments.jsx
  const fetchAppointments = async () => {
    try {
      const res = await fetch("/api/walkIn/", {
        method: "GET",
        credentials: "include",
        headers: {
          Accept: "application/json",
          "X-CSRFToken": getCookie("csrftoken") || "",
        },
      });

      const text = await res.text();
      const data = text ? JSON.parse(text) : [];

      if (res.ok) {
        const list = Array.isArray(data) ? data : data.results || data.appointments || [];
        setAppointments(list);
      }
    } catch (err) {
      console.error("Error fetching appointments:", err);
    }
  };

  // Load data on component mount
  useEffect(() => {
    refreshData();
  }, []);

  const refreshData = () => {
    setLoading(true);
    fetchUserPets();
    fetchAppointments();
  };

  // Handle when a pet is added - refresh the pets list
  const handlePetAdded = () => {
    fetchUserPets();
  };

  // Handle when an appointment is booked - refresh the appointments list
  const handleAppointmentBooked = () => {
    fetchAppointments();
  };

  // Handle pet details view (you can expand this to show a modal)
  const handleViewPetDetails = (pet) => {
    setSelectedPet(pet);
    // You can open a pet details modal here
    console.log('View pet details:', pet);
    // TODO: Implement pet details modal
  };

  // Handle appointment details view (you can expand this to show a modal)
  const handleViewAppointmentDetails = (appointment) => {
    setSelectedAppointment(appointment);
    // You can open an appointment details modal here
    console.log('View appointment details:', appointment);
    // TODO: Implement appointment details modal
  };

  return (
    <div className="container">
      <div className="profile-content">
        <div className="profile-header">
          <h1 className="profile-title">My Profile</h1>
          <div>
            <button className="btn btn-primary" onClick={() => onOpenModal('addPet')}>
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
          onRefresh={refreshData}
          onViewPetDetails={handleViewPetDetails}
          onViewAppointmentDetails={handleViewAppointmentDetails}
        />
      </div>
    </div>
  )
}

export default ProfileContent