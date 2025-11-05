import React from 'react';
import { Routes, Route } from 'react-router-dom';


// Import styles
import '../styles/Dashboard.css';

// Import all components
import SideNav from '../components/navigation/SideNav';
import AddPets from '../components/forms/AddPets';
import ViewPets from '../components/view/ViewPets';
import SetAppointment from '../components/forms/SetAppointment';
import ViewAppointments from '../components/view/ViewAppointments';
import Settings from '../components/common/Settings';

function Dashboard() {
    return (
        <div className="dashboard"> 
            <SideNav />
            <main className="rightside">
                <Routes>
                    <Route path="addpets" element={<AddPets />} />
                    <Route path="viewpets" element={<ViewPets />} />
                    <Route path="setappointment" element={<SetAppointment />} />
                    <Route path="viewappointments" element={<ViewAppointments />} />
                    <Route path="settings" element={<Settings />} />
                    {/* Add more routes as needed */}
                </Routes>
            </main>
        </div>
    );
}

export default Dashboard;