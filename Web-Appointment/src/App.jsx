
import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Index from './pages/HomePage/Index'
import BookNow from './pages/BookNow/BookNow'
import ManageBooking from './pages/ManageBooking'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/book-now" element={<BookNow />} />
          <Route path="/manage-booking" element={<ManageBooking />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
