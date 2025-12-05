// Header.jsx (fixed with proper home and section navigation)
import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import LoginModal from "../modals/LoginModal";
import SignupModal from "../modals/SignupModal";

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [userFirstName, setUserFirstName] = useState('')
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);
  const [activeSection, setActiveSection] = useState('home'); // Track active section
  const navigate = useNavigate()
  const location = useLocation()

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
        if (data && data.is_authenticated) {
          setIsAuthenticated(true)
          setUserFirstName(data.first_name || data.username || '')
          return true
        }
      }

      setIsAuthenticated(false)
      setUserFirstName('')
      return false
    } catch (error) {
      console.error('Auth check failed:', error)
      setIsAuthenticated(false)
      return false
    }
  }

  useEffect(() => {
    checkAuth()
  }, [location.pathname])

  // Add scroll spy to detect active section
  useEffect(() => {
    if (location.pathname === '/') {
      const handleScroll = () => {
        const sections = ['home', 'about', 'services', 'hours', 'contact'];
        const scrollY = window.pageYOffset + 100; // Offset for better detection
        const headerHeight = 80;

        let currentSection = 'home';

        for (const section of sections) {
          const element = document.getElementById(section);
          if (element) {
            const elementTop = element.offsetTop - headerHeight;

            // Check if we've scrolled past this section's start
            if (scrollY >= elementTop) {
              currentSection = section;
            }
          }
        }

        setActiveSection(currentSection);
      };

      window.addEventListener('scroll', handleScroll);
      handleScroll(); // Initial check

      return () => window.removeEventListener('scroll', handleScroll);
    }
  }, [location.pathname]);

  const handleLogout = async () => {
    if (!window.confirm('Are you sure you want to logout?')) return

    try {
      await fetch('/api/logout/', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'X-CSRFToken': getCookie('csrftoken') || ''
        }
      })
    } catch (error) {
      console.error('Logout API call failed:', error)
    } finally {
      localStorage.clear()
      sessionStorage.clear()
      setIsAuthenticated(false)
      setUserFirstName('')
      navigate('/?logout=true')
    }
  }

  function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';')
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }

  const getUserInitial = () => {
    return userFirstName ? userFirstName.charAt(0).toUpperCase() : 'U'
  }

  const handleNavigation = (path) => {
    navigate(path)
    setMobileMenuOpen(false)
  }

  const handleLoginClick = (e) => {
    e.preventDefault();
    setShowLogin(true);
    setMobileMenuOpen(false);
  }

  // Handle Home click - scroll to top if on home page, otherwise navigate to home
  const handleHomeClick = (e) => {
    e.preventDefault();

    if (location.pathname === '/') {
      // Already on home page - scroll to top
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
      setActiveSection('home');
    } else {
      // Not on home page - navigate to home
      navigate('/');
    }

    setMobileMenuOpen(false);
  }

  // Handle section clicks
  const handleSectionClick = (e, sectionId) => {
    e.preventDefault();

    // If we're not on the home page, navigate to home first
    if (location.pathname !== '/') {
      navigate('/');
      // Wait for navigation to complete, then scroll to section
      setTimeout(() => {
        scrollToSection(sectionId);
      }, 100);
    } else {
      // We're already on home page, just scroll to section
      scrollToSection(sectionId);
    }

    setActiveSection(sectionId);
    setMobileMenuOpen(false);
  }

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      const offsetTop = element.offsetTop - 80; // Adjust for fixed header height
      window.scrollTo({
        top: offsetTop,
        behavior: 'smooth'
      });
    }
  }

  // Check if a section is active
  const isSectionActive = (section) => {
    if (location.pathname !== '/') return false;
    return activeSection === section;
  }

  return (
    <header>
      <div className="container">
        <nav className="navbar">
          <div className="logo header-profile">
            <img
              src="/assets/images/logo/PETMATE LOGO.png"
              alt="PetMate Logo"
              onClick={handleHomeClick}
              style={{ cursor: 'pointer' }}
            />
          </div>

          <div className={`nav-links ${mobileMenuOpen ? 'active' : ''}`}>
            <a
              href="/"
              onClick={handleHomeClick}
              className={location.pathname === '/' && activeSection === 'home' ? 'active' : ''}
            >
              Home
            </a>
            <a
              href="#about"
              onClick={(e) => handleSectionClick(e, 'about')}
              className={isSectionActive('about') ? 'active' : ''}
            >
              About
            </a>
            <a
              href="#services"
              onClick={(e) => handleSectionClick(e, 'services')}
              className={isSectionActive('services') ? 'active' : ''}
            >
              Services
            </a>
            <a
              href="#hours"
              onClick={(e) => handleSectionClick(e, 'hours')}
              className={isSectionActive('hours') ? 'active' : ''}
            >
              Hours
            </a>
            <a
              href="#contact"
              onClick={(e) => handleSectionClick(e, 'contact')}
              className={isSectionActive('contact') ? 'active' : ''}
            >
              Contact
            </a>

            {isAuthenticated && (
              <a
                href="/dashboard"
                onClick={(e) => { e.preventDefault(); handleNavigation('/dashboard'); }}
                className={location.pathname === '/dashboard' ? 'active' : ''}
              >
                My Profile
              </a>
            )}
          </div>

          <div className="user-menu">
            {isAuthenticated ? (
              <>
                <div className="user-info">
                  <div
                    className="user-avatar"
                    onClick={() => handleNavigation('/dashboard')}
                    title="View Profile"
                  >
                    {getUserInitial()}
                  </div>
                </div>
                <button
                  className="logout-btn"
                  onClick={handleLogout}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: '#ffa946ff',
                    cursor: 'pointer',
                    fontSize: '25px',
                    marginLeft: '10px'
                  }}
                >
                  <i className="fas fa-sign-out-alt"></i>
                </button>
              </>
            ) : (
              <a
                href="#"
                className="login-btn"
                onClick={handleLoginClick}
              >
                Login
              </a>
            )}

            <div className="mobile-menu" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
              <i className="fas fa-bars"></i>
            </div>
          </div>
        </nav>

        {/* Modals */}
        <LoginModal
          visible={showLogin}
          onClose={() => setShowLogin(false)}
          onOpenSignup={() => {
            setShowLogin(false);
            setShowSignup(true);
          }}
          onLoginSuccess={() => {
            setShowLogin(false);
            checkAuth();
            navigate('/dashboard');
          }}
        />
        <SignupModal
          visible={showSignup}
          onClose={() => setShowSignup(false)}
          onOpenLogin={() => {
            setShowSignup(false);
            setShowLogin(true);
          }}
          onSignupSuccess={() => {
            setShowSignup(false);
          }}
        />
      </div>
    </header>
  )
}

export default Header