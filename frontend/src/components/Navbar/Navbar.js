import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <span className="logo-icon">📈</span>
          <span className="logo-text">FINANZ</span>
        </Link>
        <ul className="navbar-menu">
          <li className="navbar-item">
            <Link to="/" className="navbar-link">Dashboard</Link>
          </li>
          <li className="navbar-item">
            <Link to="/chart" className="navbar-link">Live Charts</Link>
          </li>
          <li className="navbar-item">
            <Link to="/predictions" className="navbar-link">Predictions</Link>
          </li>
          <li className="navbar-item">
            <Link to="/backtest" className="navbar-link">Backtest</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
