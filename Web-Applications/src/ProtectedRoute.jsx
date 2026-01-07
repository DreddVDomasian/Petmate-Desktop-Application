// ProtectedRoute.jsx
import { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { apiFetch } from './config/api';

export default function ProtectedRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  const location = useLocation();

  useEffect(() => {
    checkAuthentication();
  }, [location]);

  const checkAuthentication = async () => {
    try {
      // Bust iOS/Safari cache
      const res = await apiFetch(`/api/user/?_=${Date.now()}`, {
        cache: 'no-store',
        headers: {
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache',
        },
      });

      if (!res.ok) {
        setIsAuthenticated(false);
        return;
      }

      const data = await res.json();
      setIsAuthenticated(Boolean(data?.is_authenticated));
    } catch {
      setIsAuthenticated(false);
    }
  };

  if (isAuthenticated === null) return <div>Loading...</div>;
  return isAuthenticated ? children : <Navigate to="/?redirect=true" replace />;
}