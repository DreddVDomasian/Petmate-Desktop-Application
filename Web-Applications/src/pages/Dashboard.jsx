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
import '../styles/Dashboard.css';

function Dashboard(props) {
  const [activeModal, setActiveModal] = useState(null)
  const [refreshTrigger, setRefreshTrigger] = useState(0)

  const openModal = (modalName) => setActiveModal(modalName)
  const closeModal = () => setActiveModal(null)

  // new state for lists & loading
  const [pets, setPets] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);

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
      
      console.log('Appointments data:', data);
      
      // Extract the actual appointments array from the paginated response
      const appointmentsList = data.results || [];
      
      console.log('Appointments list:', appointmentsList);
      console.log('Number of appointments:', appointmentsList.length);
      
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

  return (
    <div className="dashboard-new">
      <Header />
      <ProfileContent 
        onOpenModal={openModal} 
        pets={pets}
        appointments={appointments}
        loading={loading}
        onRefresh={triggerRefresh} // Only pass the refresh function
        // Remove onRegisterRefresh since we're not using it
      />
      
      {/* Modals */}
      <AddPetModal 
        isOpen={activeModal === 'addPet'} 
        onClose={closeModal}
        onPetAdded={() => {
          fetchPets(); // Refresh pets list
          triggerRefresh(); // Trigger general refresh
        }}
      />
      
      <BookAppointmentModal 
        isOpen={activeModal === 'bookAppointment'} 
        onClose={closeModal}
        onAppointmentBooked={() => {
          fetchAppointments(); // Refresh appointments list
          triggerRefresh(); // Trigger general refresh
        }}
      />
    </div>
  )
}

export default Dashboard