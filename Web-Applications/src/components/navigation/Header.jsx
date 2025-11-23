import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [userFirstName, setUserFirstName] = useState('')
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()

  // COPY AUTH CHECK FROM OLD SIDENAV
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

      // If not authenticated, redirect to login
      setIsAuthenticated(false)
      setUserFirstName('')

      // Only redirect if we're not already on login page
      if (!location.pathname.includes('/login') && location.pathname !== '/') {
        navigate('/?session_expired=true')
      }
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

  // COPY LOGOUT FUNCTION FROM OLD SIDENAV
  const handleLogout = async () => {
    if (!window.confirm('Are you sure you want to logout?')) return

    try {
      // Call logout API
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
      // Clear client-side storage
      localStorage.clear()
      sessionStorage.clear()

      // Reset state
      setIsAuthenticated(false)
      setUserFirstName('')

      // Force navigation to home and clear history
      window.location.replace('/?logout=true')
    }
  }

  // COPY GETCOOKIE FUNCTION FROM OLD SIDENAV
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

  // Get user initial for avatar
  const getUserInitial = () => {
    return userFirstName ? userFirstName.charAt(0).toUpperCase() : 'U'
  }

  return (
    <header>
      <div className="container">
        <nav className="navbar">
          <a href="/" className="logo">
            <i className="fas fa-paw"></i>
            <span>PetMate</span>
          </a>
          <div className={`nav-links ${mobileMenuOpen ? 'active' : ''}`}>
            <a href="/">Home</a>
            <a href="/#about">About</a>
            <a href="/#services">Services</a>
            <a href="/#hours">Hours</a>
            <a href="/#contact">Contact</a>
            {isAuthenticated && (
              <a href="/dashboard" className="active">My Profile</a>
            )}
          </div>
          <div className="user-menu">
            {isAuthenticated ? (
              <>
                <div className="user-info">
                  <div className="user-avatar" style={{cursor: 'pointer'}}>
                    {getUserInitial()}
                  </div>
                </div>
                <button 
                  className="logout-btn-mobile" 
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
              <a href="/" className="login-btn">Login</a>
            )}
            <div className="mobile-menu" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
              <i className="fas fa-bars"></i>
            </div>
          </div>
        </nav>
      </div>
    </header>
  )
}

export default Header