import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from main import Stock, Trade, StockMarket, UserInput

# Unit test for the Stock class
class TestStock(unittest.TestCase):

    def setUp(self):
        # Set up common test data for Stock tests
        self.stockCommon = Stock("POP", "Common", 8, None, 100)
        self.stockPreferred = Stock("GIN", "Preferred", 8, 0.02, 100)

    def test_calculate_dividend_yield_common(self):
        # Test dividend yield calculation for common stock
        self.assertEqual(self.stockCommon.calculate_dividend_yield(100), 0.08)

    def test_calculate_dividend_yield_preferred(self):
        # Test dividend yield calculation for preferred stock
        self.assertEqual(self.stockPreferred.calculate_dividend_yield(100), 0.02)

    def test_calculate_dividend_yield_invalid_price(self):
        # Test that invalid price raises ValueError
        with self.assertRaises(ValueError):
            self.stockCommon.calculate_dividend_yield(0)

    def test_calculate_pe_ratio(self):
        # Test P/E ratio calculation
        self.assertEqual(self.stockCommon.calculate_pe_ratio(100), 12.5)

    def test_calculate_pe_ratio_zero_dividend(self):
        # Test P/E ratio when the last dividend is zero
        stock = Stock("TEST", "Common", 0, None, 100)
        self.assertEqual(stock.calculate_pe_ratio(100), float('inf'))

    def test_record_trade(self):
        # Test recording a trade
        self.stockCommon.record_trade(100, "buy", 120)
        self.assertEqual(len(self.stockCommon.trades), 1)
        trade = self.stockCommon.trades[0]
        self.assertEqual(trade.quantity, 100)
        self.assertEqual(trade.indicator, "buy")
        self.assertEqual(trade.price, 120)

    def test_calculate_volume_weighted_stock_price(self):
        # Test volume weighted stock price calculation
        self.stockCommon.record_trade(100, "buy", 120)
        self.stockCommon.record_trade(200, "buy", 150)
        self.assertAlmostEqual(self.stockCommon.calculate_volume_weighted_stock_price(), 140)


# Unit test for the Trade class
class TestTrade(unittest.TestCase):

    def test_trade_initialization(self):
        # Test initialization of a Trade object
        now = datetime.now()
        trade = Trade(now, 100, "buy", 120)
        self.assertEqual(trade.timestamp, now)
        self.assertEqual(trade.quantity, 100)
        self.assertEqual(trade.indicator, "buy")
        self.assertEqual(trade.price, 120)


# Unit test for the StockMarket class
class TestStockMarket(unittest.TestCase):

    def setUp(self):
        # Set up common test data for StockMarket tests
        self.stockCommon = Stock("POP", "Common", 8, None, 100)
        self.stockPreferred = Stock("GIN", "Preferred", 8, 0.02, 100)
        self.stockMarket = StockMarket()
        self.stockMarket.add_stock(self.stockCommon)
        self.stockMarket.add_stock(self.stockPreferred)

    def test_add_stock(self):
        # Test adding stocks to the market
        self.assertIn("POP", self.stockMarket.stocks)
        self.assertIn("GIN", self.stockMarket.stocks)

    def test_record_trade(self):
        # Test recording a trade for a stock
        self.stockMarket.record_trade("POP", 100, "buy", 120)
        self.assertEqual(len(self.stockMarket.stocks["POP"].trades), 1)

    def test_record_trade_invalid_symbol(self):
        # Test that recording a trade with an invalid symbol raises ValueError
        with self.assertRaises(ValueError):
            self.stockMarket.record_trade("INVALID", 100, "buy", 120)

    def test_record_trade_invalid_indicator(self):
        # Test that recording a trade with an invalid symbol raises ValueError
        with self.assertRaises(ValueError):
            self.stockMarket.record_trade("POP", 100, "INVALID", 120)

    def test_calculate_all_share_index(self):
        # Test calculation of the GBCE All Share Index
        self.stockCommon.record_trade(100, "buy", 120)
        self.stockPreferred.record_trade(200, "sell", 90)
        self.assertAlmostEqual(self.stockMarket.calculate_all_share_index(), 103.92304845413264, places=5)

    def test_calculate_all_share_index_no_trades(self):
        # Test GBCE All Share Index calculation when there are no trades
        self.assertEqual(self.stockMarket.calculate_all_share_index(), 0)

class TestUserInput(unittest.TestCase):
    
    def setUp(self):
        self.ui = UserInput()

    def test_valid_stock_symbol(self):
        # Test valid input for stock symbol
        with patch('builtins.input', side_effect=['TEA']):
            symbol = self.ui.get_stock_symbol()
            self.assertEqual(symbol, 'TEA')

    def test_invalid_stock_symbol(self):
        # Test invalid input for stock symbol
        with patch('builtins.input', side_effect=['XYZ', 'ALE']):
            symbol = self.ui.get_stock_symbol()
            self.assertEqual(symbol, 'ALE')

    def test_exit_command(self):
        # Test exit command
        with patch('builtins.input', side_effect=['EXIT']):
            symbol = self.ui.get_stock_symbol()
            self.assertIsNone(symbol)

    def test_valid_trading_quantity(self):
        # Test valid input for trading quantity
        with patch('builtins.input', side_effect=['100']):
            quantity = self.ui.get_trading_quantity()
            self.assertEqual(quantity, 100.0)

    def test_invalid_trading_quantity(self):
        # Test invalid input for trading quantity
        with patch('builtins.input', side_effect=['abc', '50']):
            quantity = self.ui.get_trading_quantity()
            self.assertEqual(quantity, 50.0)

    def test_valid_indicator(self):
        # Test valid input for indicator
        with patch('builtins.input', side_effect=['buy']):
            indicator = self.ui.get_indicator()
            self.assertEqual(indicator, 'buy')

    def test_invalid_indicator(self):
        # Test invalid input for indicator
        with patch('builtins.input', side_effect=['sell', 'hold']):
            indicator = self.ui.get_indicator()
            self.assertEqual(indicator, 'sell')

    def test_valid_price(self):
        # Test valid input for price
        with patch('builtins.input', side_effect=['50.25']):
            price = self.ui.get_price()
            self.assertEqual(price, 50.25)

    def test_invalid_price(self):
        # Test invalid input for price
        with patch('builtins.input', side_effect=['abc', '75.50']):
            price = self.ui.get_price()
            self.assertEqual(price, 75.50)

if __name__ == "__main__":
    unittest.main()
