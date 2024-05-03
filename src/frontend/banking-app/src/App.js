import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/auth/Login';
import Home from './components/pages/Home'

function App() {
  
  return (
    <Router>
      <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/home" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App;
