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


import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Header from '../components/navigation/Header'
import ProfileContent from '../components/view/ProfileContent'
import AddPetModal from '../components/forms/AddPetModal'
import BookAppointmentModal from '../components/forms/BookAppointmentModal'
import '../styles/Dashboard.css';

// Create a Protected Route wrapper
const ProtectedRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = React.useState(null)
  const [loading, setLoading] = React.useState(true)

  React.useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    try {
      const res = await fetch('/api/user/', {
        credentials: 'include',
        headers: {
          'Cache-Control': 'no-cache'
        }
      })

      if (res.ok) {
        const data = await res.json()
        setIsAuthenticated(data.is_authenticated)
      } else {
        setIsAuthenticated(false)
      }
    } catch (error) {
      setIsAuthenticated(false)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return isAuthenticated ? children : <Navigate to="/" replace />
}

// Dashboard component with modals
function Dashboard() {
  const [activeModal, setActiveModal] = useState(null)

  const openModal = (modalName) => setActiveModal(modalName)
  const closeModal = () => setActiveModal(null)

  return (
    <div className="dashboard-new">
      <Header />
      <ProfileContent onOpenModal={openModal} />
      
      {/* Modals */}
      <AddPetModal 
        isOpen={activeModal === 'addPet'} 
        onClose={closeModal}
        onPetAdded={() => {
          closeModal()
          // Data will be refreshed by ProfileContent
        }}
      />
      
      <BookAppointmentModal 
        isOpen={activeModal === 'bookAppointment'} 
        onClose={closeModal}
        onAppointmentBooked={() => {
          closeModal()
          // Data will be refreshed by ProfileContent
        }}
      />
    </div>
  )
}

// Your existing Index page (public facing)
function Index() {
  return (
    <div>
      {/* Your existing Index page content */}
      <h1>Welcome to PetMate</h1>
      <p>This is the public facing page</p>
    </div>
  )
}

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<Index />} />
          <Route
            path="/dashboard/*"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App