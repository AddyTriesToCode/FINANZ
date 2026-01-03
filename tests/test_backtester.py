"""
Test suite for backtesting service
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.services.backtester import Backtester
import unittest
from datetime import datetime, timedelta

class TestBacktester(unittest.TestCase):
    def setUp(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        self.backtester = Backtester(
            'RELIANCE.NS',
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
    
    def test_sma_crossover_strategy(self):
        """Test SMA crossover strategy"""
        results = self.backtester.run_strategy('sma_crossover')
        self.assertIsNotNone(results)
        self.assertIn('metrics', results)
        self.assertIn('total_return', results['metrics'])
    
    def test_buy_and_hold_strategy(self):
        """Test buy and hold strategy"""
        results = self.backtester.run_strategy('buy_and_hold')
        self.assertIsNotNone(results)
        self.assertGreater(len(results['trades']), 0)

if __name__ == '__main__':
    unittest.main()
