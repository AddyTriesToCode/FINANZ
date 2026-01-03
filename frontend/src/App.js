import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar/Navbar';
import Dashboard from './pages/Dashboard/Dashboard';
import StockChart from './pages/StockChart/StockChart';
import Backtest from './pages/Backtest/Backtest';
import Predictions from './pages/Predictions/Predictions';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/chart" element={<StockChart />} />
          <Route path="/backtest" element={<Backtest />} />
          <Route path="/predictions" element={<Predictions />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
