import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';

export default function SideNav({ defaultActive = 'addclient', onNavigate = () => {} }) {
  const [active, setActive] = useState(defaultActive);
  const [userFirstName, setUserFirstName] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // fetch current user info from backend
    fetch('/api/user/', { credentials: 'include' })
      .then(res => res.ok ? res.json() : Promise.reject(res))
      .then(data => {
        if (data && data.is_authenticated) {
          setUserFirstName(data.first_name || data.username || '');
        }
      })
      .catch(() => {
        // ignore errors in UI; optional: setUserFirstName('Guest')
      });
  }, []);

  const items = [
    { id: 'addpets', label: 'Add Pets', icon: '/assets/icons/add.png', to: '/dashboard/addpets' }, /*waala pa, */ 
    { id: 'viewpets', label: 'View Pets', icon: '/assets/icons/view.png', to: '/dashboard/viewpets' }, /* yung # dyan ilalagay kung saan gusto mo papuntahin */
    { id: 'setappointment', label: 'Set Appointment', icon: '/assets/icons/appointment.png', to: '/dashboard/setappointment' },
    { id: 'appointments', label: 'View Appointments', icon: '/assets/icons/view.png', to: '#' },
  ];

  function handleAction(id, to) {
    setActive(id);
    onNavigate(id);
    if (to) {
      navigate(to);
    }
  }

  function handleLogout() {
    if (!window.confirm('Are you sure you want to logout?')) return;
    // clear storage and redirect to login/home
    localStorage.clear();
    sessionStorage.clear();
    onNavigate('logout');
    navigate('/');
  }

  return (
    <aside className="leftside">
      <div className="nav-header">
        <img src="/assets/hjk-removebg-preview.png" alt="user" className="nav-logo" />
        <h1>Welcome</h1>
        <p className="welcome-text">{userFirstName || 'USER'}</p> {/* shows first name when available */}
      </div>

      <nav className="main-nav" aria-label="Main navigation">
        <ul className="nav-menu">
          {items.map(i => (
            <li key={i.id} className={`nav-item ${active === i.id ? 'active' : ''}`}>
              <NavLink
                to={i.to}
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                onClick={() => handleAction(i.id, i.to)}
                aria-current={active === i.id ? 'page' : undefined}
              >
                <img src={i.icon} alt="" className="nav-icon" />
                <span className="nav-text">{i.label}</span>
              </NavLink>
            </li>
          ))}
        </ul>

        <div className="nav-divider" />

        <ul className="nav-menu secondary">
          <li className={`nav-item ${active === 'settings' ? 'active' : ''}`}>
            <NavLink
              to="#" /*dito ang link palitan hehe, */
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
              onClick={() => handleAction('settings', '/settings')}
              aria-current={active === 'settings' ? 'page' : undefined}
            >
              <img src="/assets/icons/settings.png" alt="" className="nav-icon" />
              <span className="nav-text">Settings</span>
            </NavLink>
          </li>

          <li className="nav-item">
            <button
              type="button"
              className="nav-link logout"
              onClick={handleLogout}
            >
              <img src="/assets/icons/logout.png" alt="" className="nav-icon" />
              <span className="nav-text">Logout</span>
            </button>
          </li>
        </ul>
      </nav>
    </aside>
  );
}