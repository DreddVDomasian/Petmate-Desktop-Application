import React from 'react';
import { Routes, Route } from 'react-router-dom';


// Import styles
import '../styles/Dashboard.css';

// Import all components
import SideNav from '../components/navigation/SideNav';
import AddPets from '../components/forms/AddPets';
import ViewPets from '../components/view/ViewPets';



function Dashboard() {
    return (
        <div className="dashboard"> 
            <SideNav />
            <main className="rightside">
                <Routes>
                    <Route path="addpets" element={<AddPets />} />
                    <Route path="viewpets" element={<ViewPets />} />
                    {/* Add more routes as needed */}
                </Routes>
            </main>
        </div>
    );
}

export default Dashboard;