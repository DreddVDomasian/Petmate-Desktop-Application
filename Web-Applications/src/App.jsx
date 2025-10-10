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
          <Route path="/" element={<Index />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
