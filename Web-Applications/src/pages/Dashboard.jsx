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
  const [profileRefresh, setProfileRefresh] = useState(null)

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
      const res = await fetch('/api/appointments/', { credentials: 'include' });
      if (!res.ok) throw new Error('Failed to fetch appointments');
      const data = await res.json();
      setAppointments(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('fetchAppointments error', err);
    }
  };

  // initial load
  useEffect(() => {
    fetchPets();
    fetchAppointments();
  }, []);

  // handler passed into AddPetModal — called after successful add
  const handlePetAdded = () => {
    fetchPets();
    // optional: switch to pets tab if you want
  };

  // unified refresh if you kept onRefresh prop usage
  const handleRefresh = () => {
    fetchPets();
    fetchAppointments();
  };

  return (
    <div className="dashboard-new">
      <Header />
      <ProfileContent onOpenModal={openModal} onRegisterRefresh={setProfileRefresh} />
      
      {/* Modals */}
      <AddPetModal 
        isOpen={activeModal === 'addPet'} 
        onClose={closeModal}
        onPetAdded={() => {
          // modal already closed by AddPetModal, trigger profile refresh
          if (profileRefresh) {
            console.log('Dashboard: calling profileRefresh after pet added')
            profileRefresh();
          } else {
            console.warn('Dashboard: profileRefresh not registered')
          }
        }}
      />
      
      <BookAppointmentModal 
        isOpen={activeModal === 'bookAppointment'} 
        onClose={closeModal}
        onAppointmentBooked={() => {
          if (profileRefresh) {
            console.log('Dashboard: calling profileRefresh after appointment booked')
            profileRefresh();
          } else {
            console.warn('Dashboard: profileRefresh not registered')
          }
        }}
      />
    </div>
  )
}

export default Dashboard