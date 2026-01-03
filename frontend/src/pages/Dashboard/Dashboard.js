import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import { stockAPI } from '../../api/api';

const Dashboard = () => {
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedStock, setSelectedStock] = useState('RELIANCE.NS');

  const popularStocks = [
    { symbol: 'RELIANCE.NS', name: 'Reliance Industries' },
    { symbol: 'TCS.NS', name: 'Tata Consultancy Services' },
    { symbol: 'INFY.NS', name: 'Infosys' },
    { symbol: 'HDFCBANK.NS', name: 'HDFC Bank' },
    { symbol: 'ITC.NS', name: 'ITC Limited' },
  ];

  useEffect(() => {
    fetchStockData();
  }, [selectedStock]);

  const fetchStockData = async () => {
    try {
      setLoading(true);
      const response = await stockAPI.getStockPrice(selectedStock, '1mo');
      if (response.data.success) {
        setStockData(response.data.data);
      }
    } catch (error) {
      console.error('Error fetching stock data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Stock Trading Dashboard</h1>
        <p>Real-time NSE/BSE stock analysis with CNN-LSTM predictions</p>
      </div>

      <div className="stock-selector">
        <label>Select Stock:</label>
        <select 
          value={selectedStock} 
          onChange={(e) => setSelectedStock(e.target.value)}
        >
          {popularStocks.map(stock => (
            <option key={stock.symbol} value={stock.symbol}>
              {stock.name} ({stock.symbol})
            </option>
          ))}
        </select>
      </div>

      <div className="dashboard-grid">
        <div className="card stats-card">
          <h3>Portfolio Value</h3>
          <div className="stat-value">₹1,00,000</div>
          <div className="stat-change positive">+15.2%</div>
        </div>

        <div className="card stats-card">
          <h3>Total Returns</h3>
          <div className="stat-value">₹15,200</div>
          <div className="stat-change positive">+15.2%</div>
        </div>

        <div className="card stats-card">
          <h3>Win Rate</h3>
          <div className="stat-value">68%</div>
          <div className="stat-change">32/47 trades</div>
        </div>

        <div className="card stats-card">
          <h3>Sharpe Ratio</h3>
          <div className="stat-value">1.85</div>
          <div className="stat-change">Risk-adjusted</div>
        </div>
      </div>

      <div className="card">
        <h3>Recent Activity</h3>
        {loading ? (
          <div className="loading">Loading stock data...</div>
        ) : (
          <div className="activity-list">
            <p>Stock data loaded successfully. View detailed charts in the Live Charts section.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
