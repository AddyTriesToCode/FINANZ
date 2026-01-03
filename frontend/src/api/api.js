import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Stock API calls
export const stockAPI = {
  getStockPrice: (symbol, period = '1y') => 
    apiClient.get(`/stock/price/${symbol}?period=${period}`),
  
  predictPrice: (symbol, data) => 
    apiClient.post(`/stock/predict/${symbol}`, data),
};

// Backtest API calls
export const backtestAPI = {
  runBacktest: (data) => 
    apiClient.post('/backtest/run', data),
};

// Health check
export const healthCheck = () => 
  apiClient.get('/health');

export default apiClient;
