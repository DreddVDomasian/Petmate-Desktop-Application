import React from 'react';
import '../styles/Dashboard.css';

// Import all components
import SideNav from '../components/navigation/SideNav';




function Dashboard() {
    return (
        <div className="dashboard"> 
            <SideNav />
        </div>
    );
}

export default Dashboard;