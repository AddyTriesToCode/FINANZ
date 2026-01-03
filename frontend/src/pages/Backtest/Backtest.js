import React, { useState } from 'react';
import './Backtest.css';
import { backtestAPI } from '../../api/api';

const Backtest = () => {
  const [formData, setFormData] = useState({
    symbol: 'RELIANCE.NS',
    strategy: 'sma_crossover',
    start_date: '2023-01-01',
    end_date: '2024-12-25',
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await backtestAPI.runBacktest(formData);
      if (response.data.success) {
        setResults(response.data.results);
      }
    } catch (error) {
      console.error('Error running backtest:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="backtest-page">
      <div className="page-header">
        <h1>Strategy Backtesting</h1>
        <p>Test trading strategies with historical data</p>
      </div>

      <div className="card">
        <h3>Backtest Configuration</h3>
        <form onSubmit={handleSubmit} className="backtest-form">
          <div className="form-group">
            <label>Stock Symbol:</label>
            <input
              type="text"
              name="symbol"
              value={formData.symbol}
              onChange={handleChange}
              placeholder="e.g., RELIANCE.NS"
            />
          </div>

          <div className="form-group">
            <label>Strategy:</label>
            <select name="strategy" value={formData.strategy} onChange={handleChange}>
              <option value="sma_crossover">SMA Crossover (50/200)</option>
              <option value="ml_predictions">ML Predictions (CNN-LSTM)</option>
              <option value="buy_and_hold">Buy and Hold</option>
            </select>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Start Date:</label>
              <input
                type="date"
                name="start_date"
                value={formData.start_date}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>End Date:</label>
              <input
                type="date"
                name="end_date"
                value={formData.end_date}
                onChange={handleChange}
              />
            </div>
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Running Backtest...' : 'Run Backtest'}
          </button>
        </form>
      </div>

      {results && (
        <div className="card results-card">
          <h3>Backtest Results</h3>
          <div className="results-grid">
            <div className="result-item">
              <div className="result-label">Total Return</div>
              <div className={`result-value ${results.metrics.total_return >= 0 ? 'positive' : 'negative'}`}>
                {results.metrics.total_return}%
              </div>
            </div>

            <div className="result-item">
              <div className="result-label">Sharpe Ratio</div>
              <div className="result-value">{results.metrics.sharpe_ratio}</div>
            </div>

            <div className="result-item">
              <div className="result-label">Max Drawdown</div>
              <div className="result-value negative">{results.metrics.max_drawdown}%</div>
            </div>

            <div className="result-item">
              <div className="result-label">Number of Trades</div>
              <div className="result-value">{results.metrics.num_trades}</div>
            </div>

            <div className="result-item">
              <div className="result-label">Final Portfolio Value</div>
              <div className="result-value">₹{results.metrics.final_value.toLocaleString()}</div>
            </div>
          </div>

          <div className="trades-section">
            <h4>Trade History</h4>
            <div className="trades-list">
              {results.trades.slice(0, 10).map((trade, index) => (
                <div key={index} className="trade-item">
                  <span className={`trade-type ${trade.type.toLowerCase()}`}>{trade.type}</span>
                  <span>{trade.shares} shares @ ₹{trade.price.toFixed(2)}</span>
                  <span>{trade.date}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Backtest;
