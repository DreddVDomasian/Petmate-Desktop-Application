import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import Index from './pages/Index'
import Dashboard from './pages/Dashboard'

import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<Index />} />  {/* index lalabas */}
          <Route path="/dashboard/*" element={<Dashboard />} /> {/* dashboard lalabas */}
        </Routes>
      </div>
    </Router>
  )
}

export default App
