import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { apiFetch } from './config/api'

// Ensure CSRF cookie is set for API calls
apiFetch('/api/csrf/').catch(() => {});

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
