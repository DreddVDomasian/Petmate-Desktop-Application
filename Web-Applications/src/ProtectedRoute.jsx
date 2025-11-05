// ProtectedRoute.jsx
import { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';

export default function ProtectedRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  const location = useLocation();

  useEffect(() => {
    checkAuthentication();
  }, [location]);

  const checkAuthentication = async () => {
    try {
      const res = await fetch('/api/user/', {
        credentials: 'include',
        headers: { 'Cache-Control': 'no-cache' }
      });

      if (res.ok) {
        const data = await res.json();
        setIsAuthenticated(data.is_authenticated);
      } else {
        setIsAuthenticated(false);
      }
    } catch (error) {
      setIsAuthenticated(false);
    }
  };

  if (isAuthenticated === null) {
    return <div>Loading...</div>; // Or a loading spinner
  }

  return isAuthenticated ? children : <Navigate to="/?redirect=true" replace />;
}