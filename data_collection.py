# This file is to collect data and put what I actually need into useful items to use in other areas
from yahooquery import Ticker
import pandas as pd
from tabulate import tabulate

# Get the ticker: Getting from the ticker.py file for now
from ticker import ticker_sym

# Make a query to see if we can even get data for this stock ticker
try:
    stock_data = Ticker(ticker_sym)

except Exception as exc:
    print(f"Error: Unable to retrieve data for ticker '{ticker_sym}'.")
    print(f"Error Details: {str(exc)}")
    exit(1)


company_full_name = stock_data.price[ticker_sym]['longName'] # Didnt hit exception lookup the rest
print(tabulate([["Performing analysis on:", str(company_full_name)], ["Ticker: ", str(ticker_sym)]], 
               headers=['Company Info'],tablefmt='mixed_grid')) # Output a print that we are gathering data for the company name
company_profile = stock_data.asset_profile[ticker_sym] # Store some data to use for later
current_price = stock_data.financial_data[ticker_sym]['currentPrice'] # Current price
shares_outstanding = stock_data.key_stats[ticker_sym]['sharesOutstanding'] # Shares Outstanding
income_stmnt = stock_data.income_statement() # Income statement
key_stock_stats = stock_data.key_stats[ticker_sym] # Some key stats
data_to_fetch = ['NetIncome'] # Get other financial data
fetched_data = stock_data.get_financial_data(data_to_fetch, trailing=True) # Fetch the data
net_income = fetched_data['NetIncome'].iloc[-1] # Net Income 




# Get the preferred dividends
if 'PreferredStockDividends' in income_stmnt:
    preferred_dividends = income_stmnt['PreferredStockDividends'].iloc[-1]
else:
    preferred_dividends = 0



# Formatting functions
def format_value(value):
    if value >= 1e9:
        return f'{value/1e9:.2f}B'
    elif value >= 1e6:
        return f'{value/1e6:.2f}M'
    return str(value)


basic_data_to_print = [["Current Price", current_price], ["Net Income", format_value(net_income)], 
                       ["Shares Outstanding", format_value(shares_outstanding)], 
                       ["Preferred Dividends", format_value(preferred_dividends)]] # Basic financial data about the company

print(tabulate(basic_data_to_print, headers=['Attribute', 'Value'], tablefmt="mixed_grid", floatfmt=".2f"))



eps_data = stock_data.earning_history # EPS calc from earning history
eps_data = eps_data.drop(columns=['maxAge']) # Drop the columns we dont care about
eps_data_to_print = eps_data.reset_index(drop=True).values.tolist() # Conver it to a list for printing, with the dropped cols
eps_actual_total = sum(row[0] for row in eps_data_to_print) # Get the total 12 Month EPS
eps_actual_total = round(eps_actual_total, 2) # Round
eps_data_to_print = [row[::-1] for row in eps_data_to_print] # Reverse columns

eps_data_to_print.append(['', '', '', '', '12 Month EPS', eps_actual_total]) # Append the 12 Month eps to the table
headers = ["Period", "Quarter", "Surprise Percent", "EPS Difference", "EPS Estimate", "EPS Actual"] # Setup the headers
print("\n\nEPS Quarters: ")
print(tabulate(eps_data_to_print, headers, tablefmt="mixed_grid")) # Print the table


# Eps growth
# eps_growth = stock_data.earnings_trend

# for trend in eps_growth[ticker_sym]['trend']:
#     period = trend['period']
#     growth = trend['growth']
#     print(f"EPS TREND for period {period}: {growth}")


print(key_stock_stats)