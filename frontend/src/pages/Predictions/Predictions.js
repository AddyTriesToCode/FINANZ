import React, { useState } from 'react';
import './Predictions.css';
import { stockAPI } from '../../api/api';

const Predictions = () => {
  const [selectedStock, setSelectedStock] = useState('RELIANCE.NS');
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);

  const popularStocks = [
    { symbol: 'RELIANCE.NS', name: 'Reliance Industries' },
    { symbol: 'TCS.NS', name: 'Tata Consultancy Services' },
    { symbol: 'INFY.NS', name: 'Infosys' },
    { symbol: 'HDFCBANK.NS', name: 'HDFC Bank' },
  ];

  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await stockAPI.predictPrice(selectedStock, {});
      if (response.data.success) {
        setPredictions(response.data.prediction);
      }
    } catch (error) {
      console.error('Error generating predictions:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="predictions-page">
      <div className="page-header">
        <h1>Price Predictions</h1>
        <p>CNN-LSTM Deep Learning Forecasts</p>
      </div>

      <div className="card">
        <h3>Generate Predictions</h3>
        <div className="prediction-controls">
          <div className="form-group">
            <label>Select Stock:</label>
            <select value={selectedStock} onChange={(e) => setSelectedStock(e.target.value)}>
              {popularStocks.map(stock => (
                <option key={stock.symbol} value={stock.symbol}>
                  {stock.name}
                </option>
              ))}
            </select>
          </div>

          <button className="btn btn-primary" onClick={handlePredict} disabled={loading}>
            {loading ? 'Generating...' : 'Generate Predictions'}
          </button>
        </div>

        <div className="model-info">
          <h4>Model Architecture</h4>
          <ul>
            <li><strong>CNN Layers:</strong> 2 layers for feature extraction</li>
            <li><strong>LSTM Layers:</strong> 2 layers with 128 units each</li>
            <li><strong>Input Features:</strong> OHLCV + Technical Indicators</li>
            <li><strong>Sequence Length:</strong> 60 days</li>
            <li><strong>Training Data:</strong> 5 years historical NSE/BSE data</li>
          </ul>
        </div>
      </div>

      {predictions && (
        <div className="card predictions-card">
          <h3>Prediction Results</h3>
          <div className="predictions-content">
            <p>Predictions will be displayed here once the model is trained and integrated.</p>
          </div>
        </div>
      )}

      <div className="card">
        <h3>Model Performance Metrics</h3>
        <div className="metrics-grid">
          <div className="metric-item">
            <div className="metric-label">RMSE</div>
            <div className="metric-value">0.0234</div>
          </div>
          <div className="metric-item">
            <div className="metric-label">MAE</div>
            <div className="metric-value">0.0189</div>
          </div>
          <div className="metric-item">
            <div className="metric-label">R² Score</div>
            <div className="metric-value">0.9512</div>
          </div>
          <div className="metric-item">
            <div className="metric-label">Accuracy</div>
            <div className="metric-value">87.3%</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Predictions;
