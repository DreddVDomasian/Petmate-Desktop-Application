import React, { useState } from 'react';
import './SideNav.css';

export default function SideNav({ defaultActive = 'addclient', onNavigate = () => {} }) {
   const [active, setActive] = useState(defaultActive);

  const items = [
    { id: 'addpets', label: 'Add Pets', icon: '/assets/icons/add.png' },
    { id: 'viewpets', label: 'View Pets', icon: '/assets/icons/view.png' },
    { id: 'addclient', label: 'Set Appointment', icon: '/assets/icons/appointment.png' },
    { id: 'appointments', label: 'View Appointments', icon: '/assets/icons/view.png' },
  ];

  const secondary = [
    { id: 'settings', label: 'Settings', icon: '/assets/icons/settings.png' },
    { id: 'logout', label: 'Logout', icon: '/assets/icons/logout.png' },
  ];

  function handleClick(id) {
    setActive(id);
    onNavigate(id);
  }

  return (
    <aside className="leftside">
      <div className="nav-header">
        <img src="/assets/hjk-removebg-preview.png" alt="user" className="nav-logo" />
        <h1>Welcome</h1>
        <p className="welcome-text">USER HEHE</p>
      </div>

      <nav className="main-nav" aria-label="Main navigation">
        <ul className="nav-menu">
          {items.map(i => (
            <li key={i.id} className={`nav-item ${active === i.id ? 'active' : ''}`}>
              <button
                type="button"
                id={i.id}
                className="nav-link"
                onClick={() => handleClick(i.id)}
                aria-current={active === i.id ? 'page' : undefined}
              >
                <img src={i.icon} alt="" className="nav-icon" aria-hidden="true" />
                <span className="nav-text">{i.label}</span>
              </button>
            </li>
          ))}
        </ul>

        <div className="nav-divider" />

        <ul className="nav-menu secondary">
          {secondary.map(i => (
            <li key={i.id} className={`nav-item ${active === i.id ? 'active' : ''}`}>
              <button
                type="button"
                id={i.id}
                className={`nav-link ${i.id === 'logout' ? 'logout' : ''}`}
                onClick={() => handleClick(i.id)}
                aria-current={active === i.id ? 'page' : undefined}
              >
                <img src={i.icon} alt="" className="nav-icon" aria-hidden="true" />
                <span className="nav-text">{i.label}</span>
              </button>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}