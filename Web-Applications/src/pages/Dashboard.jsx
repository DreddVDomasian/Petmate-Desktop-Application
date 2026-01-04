import React, { useState, useEffect } from 'react'
import ProfileContent from '../components/view/ProfileContent'
import AddPetModal from '../components/forms/AddPetModal'
import BookAppointmentModal from '../components/forms/BookAppointmentModal'
import PetDetailsModal from '../components/modals/PetDetailsModal' 
import AppointmentDetailsModal from '../components/modals/AppointmentDetailsModal'
import AppointmentDetailsModalEdit from '../components/modals/AppointmentDetailsModalEdit' // Imported na

import { apiCall } from '../utils/api'

import '../styles/Dashboard.css';

function Dashboard(props) {
  const [activeModal, setActiveModal] = useState(null)
  const [refreshTrigger, setRefreshTrigger] = useState(0)
  const [activeTab, setActiveTab] = useState('pets')
  const openModal = (modalName) => setActiveModal(modalName)
  const closeModal = () => setActiveModal(null)

  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [showAppointmentModal, setShowAppointmentModal] = useState(false);

  // new state for edit appointment modal
  const [showEditAppointmentModal, setShowEditAppointmentModal] = useState(false);
  
  // new state for lists & loading
  const [pets, setPets] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);

  // Add state for pet details modal
  const [selectedPet, setSelectedPet] = useState(null);
  const [showPetModal, setShowPetModal] = useState(false);

  const handleViewAppointmentDetails = (appointment) => {
    setSelectedAppointment(appointment);
    setShowAppointmentModal(true);
  };

  const handleCloseAppointmentModal = () => {
    setSelectedAppointment(null);
    setShowAppointmentModal(false);
  };

  // --- ADDED: Logic para lumipat from View to Edit ---
  const handleSwitchToEdit = (appointment) => {
    setShowAppointmentModal(false); // Close View Modal
    setSelectedAppointment(appointment); // Ensure data is set
    setShowEditAppointmentModal(true);   // Open Edit Modal
  };

  // --- ADDED: Logic pag successful ang edit ---
  const handleEditSuccess = () => {
    setShowEditAppointmentModal(false); // Close Edit Modal
    fetchAppointments(); // Refresh appointment list
    triggerRefresh();    // Trigger global refresh
  };

  const fetchPets = async () => {
    setLoading(true);
    try {
      const res = await apiCall('/api/pets/', { 
        method: 'GET',
        credentials: 'include' 
      });
      if (!res.ok) throw new Error('Failed to fetch pets');
      const data = await res.json();
      setPets(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('fetchPets error', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAppointments = async () => {
    try {
      const res = await apiCall('/api/walkIn/', { 
        method: 'GET',
        credentials: 'include' 
      });
      if (!res.ok) throw new Error('Failed to fetch appointments');
      const data = await res.json();

      // Extract the actual appointments array from the paginated response
      const appointmentsList = data.results || [];

      setAppointments(Array.isArray(appointmentsList) ? appointmentsList : []);
    } catch (err) {
      console.error('fetchAppointments error', err);
    }
  };

  // initial load
  useEffect(() => {
    fetchPets();
    fetchAppointments();
  }, []);

  // Refresh when refreshTrigger changes
  useEffect(() => {
    if (refreshTrigger > 0) {
      fetchPets();
      fetchAppointments();
    }
  }, [refreshTrigger]);

  const triggerRefresh = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  // Add handlers for pet details modal
  const handleViewPetDetails = (pet) => {
    setSelectedPet(pet);
    setShowPetModal(true);
  };

  const handleClosePetModal = () => {
    setSelectedPet(null);
    setShowPetModal(false);
  };

  const handlePetUpdated = () => {
    fetchPets(); // Refresh pets list after update
    triggerRefresh();
  };

  const handlePetDeleted = () => {
    fetchPets(); // Refresh pets list after delete
    triggerRefresh();
  };

  return (
    <div className="dashboard-new">
      <ProfileContent
        onOpenModal={openModal}
        pets={pets}
        appointments={appointments}
        loading={loading}
        onRefresh={triggerRefresh}
        onViewPetDetails={handleViewPetDetails}
        onViewAppointmentDetails={handleViewAppointmentDetails}
        activeTab={activeTab}           
        setActiveTab={setActiveTab}     
      />

      {/* Modals */}
      <AddPetModal
        isOpen={activeModal === 'addPet'}
        onClose={closeModal}
        onPetAdded={() => {
          fetchPets();
          triggerRefresh();
        }}
      />
      
      {/* --- MODIFIED: View Modal now has onEdit prop --- */}
      <AppointmentDetailsModal
        isOpen={showAppointmentModal}
        onClose={handleCloseAppointmentModal}
        appointment={selectedAppointment}
        onEdit={handleSwitchToEdit} 
      />

      {/* --- ADDED: Edit Modal Component --- */}
      {showEditAppointmentModal && (
        <AppointmentDetailsModalEdit 
          isOpen={showEditAppointmentModal}
          onClose={() => setShowEditAppointmentModal(false)}
          appointment={selectedAppointment}
          onSuccess={handleEditSuccess}
        />
      )}

      <BookAppointmentModal
        isOpen={activeModal === 'bookAppointment'}
        onClose={closeModal}
        onAppointmentBooked={() => {
          fetchAppointments();
          triggerRefresh();
        }}
      />

      {/* Pet Details Modal */}
      <PetDetailsModal
        isOpen={showPetModal}
        onClose={handleClosePetModal}
        pet={selectedPet}
        onPetUpdated={handlePetUpdated}
        onPetDeleted={handlePetDeleted}
      />
    </div>
  )
}

export default Dashboard