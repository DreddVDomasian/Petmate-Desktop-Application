// App.jsx (updated)
import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Index from './pages/Index'
import Dashboard from './pages/Dashboard'
import Header from './components/navigation/Header' // Import the unified Header
import { apiFetch } from './config/api'
import './App.css'
import './styles/Dashboard.css' // Make sure Dashboard.css is imported for global styles

// Create a Protected Route wrapper
const ProtectedRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = React.useState(null)
  const [loading, setLoading] = React.useState(true)

  React.useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    try {
      const res = await apiFetch('/api/user/', {
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

function App() {
  return (
    <Router>
      <div className="app">
        {/* Unified Header for all pages */}
        <Header />
        
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