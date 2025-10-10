
import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Index from './pages/Index'
import Account from './pages/Account'

import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<Index />} />

        </Routes>
      </div>
    </Router>
  )
}

export default App
