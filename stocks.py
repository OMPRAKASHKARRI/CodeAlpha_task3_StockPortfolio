
import pandas as pd
import matplotlib.pyplot as plt

# Portfolio class
class StockPortfolio:
    def __init__(self):
        # Creating an empty dataframe to hold portfolio information
        self.portfolio = pd.DataFrame(columns=["Symbol", "Quantity", "Buy Price", "Current Price", "Total Cost", "Current Value", "Gain/Loss"])
    
    # Add stock to the portfolio
    def add_stock(self, symbol, quantity, buy_price):
        current_price = self.get_stock_price(symbol)
        new_entry = {
            "Symbol": symbol,
            "Quantity": quantity,
            "Buy Price": buy_price,
            "Current Price": current_price,
            "Total Cost": quantity * buy_price,
            "Current Value": quantity * current_price,
            "Gain/Loss": (current_price - buy_price) * quantity
        }
        self.portfolio = self.portfolio.append(new_entry, ignore_index=True)
    
    # Remove stock from portfolio
    def remove_stock(self, symbol):
        self.portfolio = self.portfolio[self.portfolio.Symbol != symbol]

    # Fetch stock price using yfinance
    def get_stock_price(self, symbol):
        stock = yf.Ticker(symbol)
        return stock.history(period="1d")["Close"].iloc[0]
    
    # Update all prices and gains in the portfolio
    def update_prices(self):
        for idx, row in self.portfolio.iterrows():
            symbol = row["Symbol"]
            current_price = self.get_stock_price(symbol)
            self.portfolio.at[idx, "Current Price"] = current_price
            self.portfolio.at[idx, "Current Value"] = current_price * row["Quantity"]
            self.portfolio.at[idx, "Gain/Loss"] = (current_price - row["Buy Price"]) * row["Quantity"]
    
    # Display the portfolio as a table
    def show_portfolio(self):
        print("\nCurrent Portfolio:\n")
        print(self.portfolio)
    
    # Plot portfolio performance
    def plot_performance(self):
        self.update_prices()  # Ensure prices are up-to-date
        self.portfolio.plot(x="Symbol", y=["Total Cost", "Current Value"], kind="bar")
        plt.title("Portfolio Performance")
        plt.ylabel("Value in $")
        plt.xlabel("Stock Symbol")
        plt.show()

# Example usage of the Stock Portfolio Tracker

# Instantiate the portfolio
portfolio = StockPortfolio()

# Adding stocks to the portfolio
portfolio.add_stock("AAPL", 10, 150)   # 10 shares of Apple bought at $150
portfolio.add_stock("GOOGL", 5, 2800)  # 5 shares of Google bought at $2800

# Display the portfolio
portfolio.show_portfolio()

# Update the stock prices with real-time data
portfolio.update_prices()

# Display the updated portfolio
portfolio.show_portfolio()

# Plot the portfolio performance (comparing cost vs current value)
portfolio.plot_performance()

# Remove a stock from the portfolio and show updated portfolio
portfolio.remove_stock("AAPL")
portfolio.show_portfolio()
