import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import './StockChart.css';
import { stockAPI } from '../../api/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const StockChart = () => {
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedStock, setSelectedStock] = useState('RELIANCE.NS');
  const [period, setPeriod] = useState('1mo');

  const popularStocks = [
    { symbol: 'RELIANCE.NS', name: 'Reliance Industries' },
    { symbol: 'TCS.NS', name: 'Tata Consultancy Services' },
    { symbol: 'INFY.NS', name: 'Infosys' },
    { symbol: 'HDFCBANK.NS', name: 'HDFC Bank' },
  ];

  useEffect(() => {
    fetchStockData();
  }, [selectedStock, period]);

  const fetchStockData = async () => {
    try {
      setLoading(true);
      const response = await stockAPI.getStockPrice(selectedStock, period);
      if (response.data.success) {
        setStockData(response.data.data);
      }
    } catch (error) {
      console.error('Error fetching stock data:', error);
    } finally {
      setLoading(false);
    }
  };

  const chartData = {
    labels: stockData?.map((_, i) => `Day ${i + 1}`) || [],
    datasets: [
      {
        label: 'Close Price',
        data: stockData?.map(d => d.Close) || [],
        borderColor: 'rgb(102, 126, 234)',
        backgroundColor: 'rgba(102, 126, 234, 0.1)',
        tension: 0.4,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: 'white',
        },
      },
      title: {
        display: true,
        text: `${selectedStock} Stock Price`,
        color: 'white',
        font: {
          size: 16,
        },
      },
    },
    scales: {
      y: {
        ticks: { color: 'white' },
        grid: { color: 'rgba(255, 255, 255, 0.1)' },
      },
      x: {
        ticks: { color: 'white' },
        grid: { color: 'rgba(255, 255, 255, 0.1)' },
      },
    },
  };

  return (
    <div className="stock-chart-page">
      <div className="page-header">
        <h1>Live Stock Charts</h1>
        <p>Real-time price visualization</p>
      </div>

      <div className="controls">
        <div className="control-group">
          <label>Stock:</label>
          <select value={selectedStock} onChange={(e) => setSelectedStock(e.target.value)}>
            {popularStocks.map(stock => (
              <option key={stock.symbol} value={stock.symbol}>
                {stock.name}
              </option>
            ))}
          </select>
        </div>

        <div className="control-group">
          <label>Period:</label>
          <select value={period} onChange={(e) => setPeriod(e.target.value)}>
            <option value="1d">1 Day</option>
            <option value="5d">5 Days</option>
            <option value="1mo">1 Month</option>
            <option value="3mo">3 Months</option>
            <option value="1y">1 Year</option>
          </select>
        </div>
      </div>

      <div className="card chart-container">
        {loading ? (
          <div className="loading">Loading chart...</div>
        ) : (
          <div className="chart-wrapper">
            <Line data={chartData} options={chartOptions} />
          </div>
        )}
      </div>
    </div>
  );
};

export default StockChart;
