# Testing interface for data collection and backend processing used
import unittest
from yahooquery import Ticker
from data_collection import collect_stock_data, multiples_valuation_find_companies


class TestFetchData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("[Info] Attempting to fetch 'AAPL'")
        cls.stock_data = collect_stock_data('AAPL')


    def test_stock_data_fetch(self):
        # Test stock data fetched successfully
        self.assertIsNotNone(self.stock_data)



    def test_multiples_valuation_find_companies(self):
        # Test multiples valuation, so test fetching other companies
        print("[Info] Attempting to fetch other similar companies")
        self.assertIsNotNone(multiples_valuation_find_companies(self.stock_data["company_ticker"], self.stock_data["current_sector"], self.stock_data["current_industry"]))



