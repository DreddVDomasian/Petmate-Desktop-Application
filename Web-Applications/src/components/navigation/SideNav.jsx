import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';

export default function SideNav({ defaultActive = 'addclient', onNavigate = () => {} }) {
  const [active, setActive] = useState(defaultActive);
  const [userFirstName, setUserFirstName] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  // Enhanced auth check function
  const checkAuth = async () => {
    try {
      const res = await fetch('/api/user/', {
        credentials: 'include',
        headers: {
          'Cache-Control': 'no-cache'
        }
      });

      if (res.ok) {
        const data = await res.json();
        if (data && data.is_authenticated) {
          setIsAuthenticated(true);
          setUserFirstName(data.first_name || data.username || '');
          return true;
        }
      }

      // If not authenticated, redirect to login
      setIsAuthenticated(false);
      setUserFirstName('');

      // Only redirect if we're not already on login page
      if (!location.pathname.includes('/login') && location.pathname !== '/') {
        navigate('/?session_expired=true');
      }
      return false;
    } catch (error) {
      console.error('Auth check failed:', error);
      setIsAuthenticated(false);
      return false;
    }
  };

  useEffect(() => {
    checkAuth();
  }, [location.pathname]); // Re-check auth on route change

  // Handle browser navigation (popstate event)
  useEffect(() => {
    const handlePopState = () => {
      // Check auth when user navigates with back/forward buttons
      setTimeout(() => checkAuth(), 100);
    };

    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const items = [
    { id: 'addpets', label: 'Add Pets', icon: '/assets/icons/add.png', to: '/dashboard/addpets' },
    { id: 'viewpets', label: 'View Pets', icon: '/assets/icons/view.png', to: '/dashboard/viewpets' },
    { id: 'setappointment', label: 'Set Appointment', icon: '/assets/icons/appointment.png', to: '/dashboard/setappointment' },
    { id: 'appointments', label: 'View Appointments', icon: '/assets/icons/view.png', to: '/dashboard/viewappointments' },
    { id: 'settings', label: 'Settings', icon: '/assets/icons/settings.png', to: '/dashboard/settings' },
    
  ];

  function handleAction(id, to) {
    // Check auth before navigation
    checkAuth().then(authenticated => {
      if (authenticated && to) {
        setActive(id);
        onNavigate(id);
        navigate(to);
      }
    });
  }

  async function handleLogout() {
    if (!window.confirm('Are you sure you want to logout?')) return;

    try {
      // Call logout API
      await fetch('/api/logout/', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'X-CSRFToken': getCookie('csrftoken') || ''
        }
      });
    } catch (error) {
      console.error('Logout API call failed:', error);
    } finally {
      // Clear client-side storage
      localStorage.clear();
      sessionStorage.clear();

      // Reset state
      setIsAuthenticated(false);
      setUserFirstName('');

      // Force navigation to home and clear history
      window.location.replace('/?logout=true');
    }
  }

  // Don't render nav if not authenticated
  if (!isAuthenticated) {
    return null;
  }

  return (
    <aside className="leftside">
      <div className="nav-header">
        <img src="/assets/icons/account.png" alt="user" className="nav-logo" />
        <h1>Welcome</h1>
        <p className="welcome-text">{userFirstName || 'USER'}</p>
      </div>

      <nav className="main-nav" aria-label="Main navigation">
        <ul className="nav-menu">
          {items.map(i => (
            <li key={i.id} className={`nav-item ${active === i.id ? 'active' : ''}`}>
              <NavLink
                to={i.to}
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                onClick={(e) => {
                  e.preventDefault();
                  handleAction(i.id, i.to);
                }}
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

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}