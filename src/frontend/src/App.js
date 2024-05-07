import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/auth/Login';
import Home from './components/pages/Home'
import Account from './components/pages/Account';
import Deposit from './components/pages/Deposit';
import Withdraw from './components/pages/Withdraw';
import Transfer from './components/pages/Transfer';

function App() {
  
  return (
    <Router>
      <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/home" element={<Home />} />
      <Route path="/account/:accountType" element={<Account />} />
      <Route path="/account/deposit/:accountType" element={<Deposit />} />
      <Route path="/account/withdraw/:accountType" element={<Withdraw />} />
      <Route path="/account/transfer/:accountType" element={<Transfer />} />
      </Routes>
    </Router>
  );
}

export default App;
