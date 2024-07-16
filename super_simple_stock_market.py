"""
Stock Market Simulation

This script simulates a stock market where stocks can be added, trades recorded,
and various financial metrics (like Dividend Yield, P/E Ratio, VWSP, and GBCE All Share Index)
can be calculated and displayed.
"""

from datetime import datetime, timedelta
import math

class StockMarket:
    """
    StockMarket class to manage multiple stocks and their trades.
    """
    def __init__(self):
        # Initialize an empty dictionary to store stock by their symbol
        self.stocks = {}

    def add_stock(self, stock):
        """
        Add a stock to the market.

        Args:
            stock (Stock): Stock object to be added to the market.
        """
        # Add stock to the market
        self.stocks[stock.symbol] = stock

    def record_trade(self, symbol, quantity, indicator, price):
        """
        Record a trade for a specific stock identified by its symbol.

        Args:
            symbol (str): Symbol of the stock for which trade is being recorded.
            quantity (float): Quantity of shares traded.
            indicator (str): Indicator of the trade ('buy' or 'sell').
            price (float): Price per share of the trade.

        Raises:
            ValueError: If the indicator is not 'buy' or 'sell', or if the stock symbol is not found in the market.
        """
        # Validate indicator
        if indicator.lower() not in ["buy", "sell"]:
            raise ValueError("Indicator must be 'buy' or 'sell'")
        
        # Record a trade for a specific stock identified by its symbol
        if symbol in self.stocks:
            self.stocks[symbol].record_trade(quantity, indicator, price)
        else:
            raise ValueError("Stock symbol not found in market")
        
    def calculate_all_share_index(self):
        """
        Calculate the GBCE All Share Index using the geometric mean of VWSP for all stocks.

        Returns:
            float: Calculated GBCE All Share Index.

        Notes:
            Returns 0 if there are no trades in any stock.
        """
        # Calculate the GBCE All Share Index using the geometric mean of VWSP for all stocks
        volumeWeightedPrices = [stock.calculate_volume_weighted_stock_price() for stock in self.stocks.values()]
        nonZeroPrices = [price for price in volumeWeightedPrices if price > 0]

        if not nonZeroPrices:
            return 0 # No trades in any stock
        
        # Geometric mean formula: nth root of the product of prices
        productOfPrices = math.prod(nonZeroPrices)
        return productOfPrices ** (1/len(nonZeroPrices))
    
class Stock:
    """
    Stock class representing a single stock in the market.
    """
    def __init__(self, symbol, type, lastDividend, fixedDividend, parValue):
        # Initialise the stock with given attributes
        self.symbol = symbol # Stock symbol, e.g. 'POP'
        self.type = type # Type of stock: 'Common' or 'Preferred'
        self.lastDividend = lastDividend # Last dividend value
        self.fixedDividend = fixedDividend # Fixed dividend for Preferred GIN stock
        self.parValue = parValue # Par value of the stock
        self.trades = [] # List to record all trades for this stock 

    def calculate_dividend_yield(self, price):
        """
        Calculate the dividend yield based on the stock type and given price.

        Args:
            price (float): Price per share for calculating dividend yield.

        Returns:
            float: Calculated dividend yield.

        Raises:
            ValueError: If price is not greater than zero or if stock type is unknown.
        """
        # Calculate the dividend yield based on the stock type and given price
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        
        if self.type == 'Common':
            # Dividend Yield for Common stock: lastDividend / price
            return self.lastDividend / price
        elif self.type == 'Preferred':
            # Dividend Yield for Preferred stock: (fixedDividend * parValue) / price
            return (self.fixedDividend * self.parValue) / price
        else:
            raise ValueError('Unknown stock type.')
        
    def calculate_pe_ratio(self, price):
        """
        Calculate the Price-to-Earnings (P/E) ratio based on the given price.

        Args:
            price (float): Price per share for calculating P/E ratio.

        Returns:
            float: Calculated P/E ratio.

        Notes:
            If last dividend is zero, returns float('inf') indicating an infinite P/E ratio.
        """
        # Calculate the P/E Ratio: price / lastDividend
        if self.lastDividend == 0:
            return float('inf') # P/E ratio is infinite if last dividend is zero
        return price / self.lastDividend
    
    def record_trade(self, quantity, indicator, price):
        """
        Record a trade with the given details.

        Args:
            quantity (float): Number of shares traded.
            indicator (str): Indicator of the trade ('buy' or 'sell').
            price (float): Price per share of the trade.
        """
        # Record a trade with the given details
        trade = Trade(datetime.now(), quantity, indicator, price)
        self.trades.append(trade)

    def calculate_volume_weighted_stock_price(self):
        """
        Calculate the Volume Weighted Stock Price (VWSP) based on trades in the past 5 minutes.

        Returns:
            float: Calculated VWSP.

        Notes:
            Returns 0 if no trades occurred in the past 5 minutes.
        """
        # Calculate the Volume Weighted Stock Price based on trades in the past 5 minutes
        now = datetime.now()

        # Filter trades that occured in the last 5 minutes
        pastTrades = [trade for trade in self.trades if now - trade.timestamp <= timedelta(minutes=5)]

        totalQuantity = sum(trade.quantity for trade in pastTrades)
        if totalQuantity == 0:
            return 0 # No trades in the past 5 minutes

        totalTradePriceQuantity = sum(trade.price * trade.quantity for trade in pastTrades)

        # VWSP Formula: sum(price * quantity) / sum(quantity)
        return totalTradePriceQuantity / totalQuantity
  
class Trade:
    """
    Trade class to represent individual trades.
    """
    def __init__(self, timestamp, quantity, indicator, price):
        # Initialize a trade with given attributes
        self.timestamp = timestamp # Time when trade occured
        self.quantity = quantity # Number of shares traded
        self.indicator = indicator # 'buy' or 'sell'
        self.price = price # Trade price per share

class UserInput:
    """
    User Input class for handling user interactions and inputs related to stock trading.
    """
    def __init__(self):
        # Initialize with predefined stock symbols and valid trading indicators
        self.stockSymbols = ['TEA', 'POP', 'ALE', 'GIN', 'JOE']
        self.validIndicators = ["buy", "sell"]

    def get_stock_symbol(self):
        """
        Prompt the user to enter a stock symbol or exit command.

        Returns:
            str or None: Selected stock symbol or None if user chooses to exit.
        """
        while True:
            print("\nAvailable stock symbols:", stockSymbols)
            stockSymbol = input("Enter the stock symbol (or type 'exit' to quit): ").strip().upper()
            if stockSymbol == 'EXIT':
                print("\nExiting the program. Goodbye!")
                return None  # Return None to indicate exit
            elif stockSymbol in self.stockSymbols:
                return stockSymbol # Return valid stock symbol
            else:
                print(f"Invalid stock symbol '{stockSymbol}'. Please choose from the available symbols.")

    def get_trading_quantity(self):
        """
        Prompt the user to enter a trading quantity.

        Returns:
            float: Trading quantity entered by the user.
        """
        while True:
            try:
                tradingQuantity = float(input("Enter the trading quantity: "))
                return tradingQuantity # Return valid trading quantity
            except ValueError:
                print("Invalid input. Please enter a valid number for trading quantity.")

    def get_indicator(self):
        """
        Prompt the user to enter a trading indicator (buy or sell).

        Returns:
            str: Trading indicator ('buy' or 'sell').
        """
        while True:
            indicator = input("Enter if you want to buy or sell: ").strip().lower()
            if indicator in self.validIndicators:
                return indicator # Return valid trading indicator
            else:
                print("Invalid input. Please enter 'buy' or 'sell'.")

    def get_price(self):
        """
        Prompt the user to enter a price for calculating metrics.

        Returns:
            float: Price entered by the user.
        """
        while True:
            try:
                price = float(input("Enter the price for calculating metrics: "))
                return price # Return valid price
            except ValueError:
                print("Invalid input. Please enter a valid number for price.")
    
if __name__== "__main__":

    userInput = UserInput()
    # Create a StockMarket instance
    stockMarket = StockMarket()
    
    # Add stocks to the market 
    # Sample number values (Table 1.) were given in pennies
    stockMarket.add_stock(Stock("TEA", "Common", 0, None, 1)) 
    stockMarket.add_stock(Stock("POP", "Common", 0.08, None, 1))
    stockMarket.add_stock(Stock("ALE", "Common", 0.23, None, 0.6))
    stockMarket.add_stock(Stock("GIN", "Preferred", 0.08, 0.02, 1))
    stockMarket.add_stock(Stock("JOE", "Common", 0.13, None, 2.5))

    stockSymbols = list(stockMarket.stocks.keys())
    
    while True:
        stockSymbol = userInput.get_stock_symbol()
        if stockSymbol is None:
            break  # Exit loop if user chooses to exit

        tradingQuantity = userInput.get_trading_quantity()
        indicator = userInput.get_indicator()
        price = userInput.get_price()

        # Record the trade in the Stock object
        try:
            stockMarket.stocks[stockSymbol].record_trade(tradingQuantity, indicator, price)
            print(f"Trade recorded successfully for {stockSymbol}.")
        except ValueError as e:
            print(f"Error recording trade for {stockSymbol}: {e}")
        
        # Calculate and display metrics
        stock = stockMarket.stocks[stockSymbol]
        print(f"\nDividend Yield for {stockSymbol}: {stock.calculate_dividend_yield(price)}")
        print(f"P/E Ratio for {stockSymbol}: {stock.calculate_pe_ratio(price)}")
        print(f"Volume Weighted Stock Price for {stockSymbol}: {stock.calculate_volume_weighted_stock_price()}")
        print(f"GBCE All Share Index: {stockMarket.calculate_all_share_index()}")
