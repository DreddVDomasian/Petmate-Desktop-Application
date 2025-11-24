// import React from 'react';
// import { Routes, Route } from 'react-router-dom';


// // Import styles
// import '../styles/Dashboard.css';

// // Import all components
// import SideNav from '../components/navigation/SideNav';
// import AddPets from '../components/forms/AddPets';
// import ViewPets from '../components/view/ViewPets';
// import SetAppointment from '../components/forms/SetAppointment';
// import ViewAppointments from '../components/view/ViewAppointments';
// import Settings from '../components/common/Settings';

// function Dashboard() {
//     return (
//         <div className="dashboard"> 
//             <SideNav />
//             <main className="rightside">
//                 <Routes>
//                     <Route path="addpets" element={<AddPets />} />
//                     <Route path="viewpets" element={<ViewPets />} />
//                     <Route path="setappointment" element={<SetAppointment />} />
//                     <Route path="viewappointments" element={<ViewAppointments />} />
//                     <Route path="settings" element={<Settings />} />
//                     {/* Add more routes as needed */}
//                 </Routes>
//             </main>
//         </div>
//     );
// }

// export default Dashboard;

import React, { useState, useEffect } from 'react'
import Header from '../components/navigation/Header'
import ProfileContent from '../components/view/ProfileContent'
import AddPetModal from '../components/forms/AddPetModal'
import BookAppointmentModal from '../components/forms/BookAppointmentModal'
import PetDetailsModal from '../components/modals/PetDetailsModal' // Add this import
import AppointmentDetailsModal from '../components/modals/AppointmentDetailsModal' 
import '../styles/Dashboard.css';

function Dashboard(props) {
  const [activeModal, setActiveModal] = useState(null)
  const [refreshTrigger, setRefreshTrigger] = useState(0)
  const [activeTab, setActiveTab] = useState('pets')
  const openModal = (modalName) => setActiveModal(modalName)
  const closeModal = () => setActiveModal(null)

  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [showAppointmentModal, setShowAppointmentModal] = useState(false);
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
  const fetchPets = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/pets/', { credentials: 'include' });
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
      const res = await fetch('/api/walkIn/', { credentials: 'include' });
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
      <Header setActiveTab={setActiveTab} />
      <ProfileContent 
        onOpenModal={openModal} 
        pets={pets}
        appointments={appointments}
        loading={loading}
        onRefresh={triggerRefresh}
        onViewPetDetails={handleViewPetDetails}
        onViewAppointmentDetails={handleViewAppointmentDetails}
        activeTab={activeTab}           // Pass activeTab
        setActiveTab={setActiveTab}     // Pass setActiveTab
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
      <AppointmentDetailsModal 
        isOpen={showAppointmentModal}
        onClose={handleCloseAppointmentModal}
        appointment={selectedAppointment}
      />
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