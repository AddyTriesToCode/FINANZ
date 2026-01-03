"""
Test suite for data fetching service
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.services.data_fetcher import DataFetcher
import unittest

class TestDataFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = DataFetcher()
    
    def test_fetch_stock_data(self):
        """Test fetching stock data"""
        data = self.fetcher.fetch_stock_data('RELIANCE.NS', period='5d')
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)
    
    def test_get_stock_info(self):
        """Test getting stock information"""
        info = self.fetcher.get_stock_info('RELIANCE.NS')
        self.assertIsNotNone(info)
        self.assertIn('symbol', info)

if __name__ == '__main__':
    unittest.main()
