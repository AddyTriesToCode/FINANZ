"""
Backtesting service for trading strategies
"""
import pandas as pd
import numpy as np
from services.data_fetcher import DataFetcher

class Backtester:
    def __init__(self, symbol, start_date, end_date, initial_capital=100000):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.data_fetcher = DataFetcher()
        
    def run_strategy(self, strategy_name):
        """
        Run backtesting for a given strategy
        
        Args:
            strategy_name: Name of the strategy to test
        
        Returns:
            Dictionary with backtest results
        """
        # Fetch historical data
        data = self.data_fetcher.fetch_stock_data(self.symbol, period='max')
        df = pd.DataFrame(data)
        
        # Initialize portfolio
        portfolio = {
            'capital': self.initial_capital,
            'shares': 0,
            'trades': [],
            'portfolio_value': []
        }
        
        # Apply strategy (placeholder - implement specific strategies)
        if strategy_name == 'sma_crossover':
            results = self._sma_crossover_strategy(df, portfolio)
        elif strategy_name == 'ml_predictions':
            results = self._ml_prediction_strategy(df, portfolio)
        else:
            results = self._buy_and_hold_strategy(df, portfolio)
        
        # Calculate metrics
        metrics = self._calculate_metrics(results)
        
        return {
            'portfolio_value': results['portfolio_value'],
            'trades': results['trades'],
            'metrics': metrics
        }
    
    def _sma_crossover_strategy(self, df, portfolio):
        """Simple Moving Average Crossover Strategy"""
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        # Trading logic
        for i in range(200, len(df)):
            if df['SMA_50'].iloc[i] > df['SMA_200'].iloc[i] and portfolio['shares'] == 0:
                # Buy signal
                shares_to_buy = int(portfolio['capital'] / df['Close'].iloc[i])
                cost = shares_to_buy * df['Close'].iloc[i]
                portfolio['shares'] += shares_to_buy
                portfolio['capital'] -= cost
                portfolio['trades'].append({
                    'date': str(df.index[i]),
                    'type': 'BUY',
                    'shares': shares_to_buy,
                    'price': df['Close'].iloc[i]
                })
            
            elif df['SMA_50'].iloc[i] < df['SMA_200'].iloc[i] and portfolio['shares'] > 0:
                # Sell signal
                revenue = portfolio['shares'] * df['Close'].iloc[i]
                portfolio['capital'] += revenue
                portfolio['trades'].append({
                    'date': str(df.index[i]),
                    'type': 'SELL',
                    'shares': portfolio['shares'],
                    'price': df['Close'].iloc[i]
                })
                portfolio['shares'] = 0
            
            # Calculate portfolio value
            portfolio_value = portfolio['capital'] + (portfolio['shares'] * df['Close'].iloc[i])
            portfolio['portfolio_value'].append({
                'date': str(df.index[i]),
                'value': portfolio_value
            })
        
        return portfolio
    
    def _buy_and_hold_strategy(self, df, portfolio):
        """Buy and Hold Strategy"""
        # Buy at start
        shares = int(portfolio['capital'] / df['Close'].iloc[0])
        portfolio['shares'] = shares
        portfolio['capital'] -= shares * df['Close'].iloc[0]
        
        portfolio['trades'].append({
            'date': str(df.index[0]),
            'type': 'BUY',
            'shares': shares,
            'price': df['Close'].iloc[0]
        })
        
        # Track portfolio value
        for i in range(len(df)):
            portfolio_value = portfolio['capital'] + (portfolio['shares'] * df['Close'].iloc[i])
            portfolio['portfolio_value'].append({
                'date': str(df.index[i]),
                'value': portfolio_value
            })
        
        return portfolio
    
    def _ml_prediction_strategy(self, df, portfolio):
        """ML-based prediction strategy (placeholder)"""
        # This will use the CNN-LSTM model predictions
        return self._buy_and_hold_strategy(df, portfolio)
    
    def _calculate_metrics(self, results):
        """Calculate performance metrics"""
        portfolio_values = [pv['value'] for pv in results['portfolio_value']]
        
        total_return = ((portfolio_values[-1] - self.initial_capital) / self.initial_capital) * 100
        
        returns = np.diff(portfolio_values) / portfolio_values[:-1]
        sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(252) if len(returns) > 0 else 0
        
        cumulative_returns = (np.array(portfolio_values) - self.initial_capital) / self.initial_capital
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - running_max)
        max_drawdown = np.min(drawdown) * 100 if len(drawdown) > 0 else 0
        
        return {
            'total_return': round(total_return, 2),
            'sharpe_ratio': round(sharpe_ratio, 2),
            'max_drawdown': round(max_drawdown, 2),
            'num_trades': len(results['trades']),
            'final_value': round(portfolio_values[-1], 2)
        }
