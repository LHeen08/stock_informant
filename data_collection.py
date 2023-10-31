# This file is to collect data and put what I actually need into useful items to use in other areas
from yahooquery import Ticker
import pandas as pd

# Get the ticker: Getting from the ticker.py file for now
from ticker import ticker_sym


ticker_sym = ticker_sym.upper()

# Make a query to see if we can even get data for this stock ticker
try:
    stock_data = Ticker(ticker_sym, validate=True, progress=True)

except Exception as exc:
    print(f"Error: Unable to retrieve data for ticker '{ticker_sym}'.")
    print(f"Error Details: {str(exc)}")
    exit(1)


company_full_name = stock_data.price[ticker_sym]['longName'] # Didnt hit exception lookup the rest

company_profile = stock_data.asset_profile[ticker_sym] # Store some data to use for later
current_price = stock_data.financial_data[ticker_sym]['currentPrice'] # Current price
shares_outstanding = stock_data.key_stats[ticker_sym]['sharesOutstanding'] # Shares Outstanding
income_stmnt = stock_data.income_statement() # Income statement
cash_flow_stmnt = stock_data.cash_flow() # cash flow statement
balance_sheet = stock_data.balance_sheet(trailing=True) # Balance sheet
# for index, row in cash_flow_stmnt.iterrows():
#     cash_flow = row['FreeCashFlow']
#     print(f"Row {index}: free cash flow = {cash_flow}")
    
key_stock_stats = stock_data.key_stats[ticker_sym] # Some key stats

net_income_ttm = income_stmnt.iloc[-1]['NetIncome'] # Trailing Twelve months net income

eps_data_from_earning_hist = stock_data.earning_history # EPS calc from earning history
trailing_eps_ttm = key_stock_stats['trailingEps'] # TTM EPS
eps_growth_trends = stock_data.earnings_trend[ticker_sym]['trend'] # EPS Trends: eps growth is retrieved from this


# Get the preferred dividends
if 'PreferredStockDividends' in income_stmnt:
    preferred_dividends = income_stmnt['PreferredStockDividends'].iloc[-1]
else:
    preferred_dividends = 0


eps_data_from_earning_hist = eps_data_from_earning_hist.drop(columns=['maxAge']) # Drop the columns we dont care about
eps_data_to_print = eps_data_from_earning_hist.reset_index(drop=True).values.tolist() # Convert it to a list for printing, with the dropped cols
eps_actual_total = sum(row[0] for row in eps_data_to_print) # Get the total 12 Month EPS
eps_actual_total = round(eps_actual_total, 2) # Round
eps_data_to_print = [row[::-1] for row in eps_data_to_print] # Reverse columns

eps_data_to_print.append(['', '', '', '', 'Current Year EPS', eps_actual_total]) # Append the 12 Month eps to the table
headers = ["Period", "Quarter", "Surprise Percent", "EPS Difference", "EPS Estimate", "EPS Actual"] # Setup the headers


eps_growth_current_quarter = [trend for trend in eps_growth_trends if trend['period'] == '0q'] # EPS growth for current quarter
eps_growth_current_quarter = eps_growth_current_quarter[0]['growth'] 

eps_growth_next_five_yrs = [trend for trend in eps_growth_trends if trend['period'] == '+5y'] # EPS growth for the next five years
eps_growth_next_five_yrs = eps_growth_next_five_yrs[0]['growth']
