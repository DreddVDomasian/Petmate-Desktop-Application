import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { apiCall } from './utils/api.js'

// Ensure CSRF cookie is set for API calls
apiCall('/api/csrf/', { credentials: 'include' }).catch(() => {});

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
