# This file is to collect data and put what I actually need into useful items to use in other areas
from yahooquery import Ticker
import pandas as pd

# Get the ticker: Getting from the ticker.py file for now
from ticker import ticker_sym



class CompanyData:
    def __init__(self, ticker):
        self.ticker = str(ticker).upper()
        try:
            stock_data = Ticker(ticker, validate=True)
        except Exception as exc:
            raise ValueError(f"Error: Unable to retrieve data for ticker {ticker}. Error Details: {str(exc)}")

        # Set instance variables for data attributes
        self.company_full_name = stock_data.price[self.ticker]["longName"]
        self.company_profile = stock_data.asset_profile[self.ticker]
        self.current_price = stock_data.financial_data[self.ticker]["currentPrice"]
        self.shares_outstanding = stock_data.key_stats[self.ticker]["sharesOutstanding"]
        self.income_statement = stock_data.income_statement()
        self.balance_sheet = stock_data.balance_sheet(trailing=True)
        self.cash_flow_statement = stock_data.cash_flow()
        self.trailing_eps_ttm = stock_data.key_stats[self.ticker]["trailingEps"]
        self.net_income_ttm = stock_data.income_statement().iloc[-1]["NetIncome"]
        self.eps_data_from_earnings_history = stock_data.earning_history
        self.eps_growth_trends = stock_data.earnings_trend[self.ticker]["trend"]
        self.preferred_dividends = self.get_preferred_dividends()
        self.eps_growth_current_quarter = self.get_eps_growth_current_quarter()
        self.eps_growth_next_five_years = self.get_eps_growth_next_five_years()

    def to_dict(self):
        return {
            "company_full_name": self.company_full_name,
            "company_profile": self.company_profile,
            "current_price": self.current_price,
            "shares_outstanding": self.shares_outstanding,
            "income_statement": self.income_statement.to_dict(orient="records"),
            "balance_sheet": self.balance_sheet.to_dict(orient="records"),
            "cash_flow_statement": self.cash_flow_statement.to_dict(orient="records"),
            "trailing_eps_ttm": self.trailing_eps_ttm,
            "net_income_ttm": self.net_income_ttm,
            "eps_data_from_earnings_history": self.eps_data_from_earnings_history,
            "eps_growth_trends": self.eps_growth_trends,
            "preferred_dividends": self.preferred_dividends,
            "eps_growth_current_quarter": self.eps_growth_current_quarter,
            "eps_growth_next_five_years": self.eps_growth_next_five_years,
        }

    def get_preferred_dividends(self):
        income_stmnt = self.income_statement
        if "PreferredStockDividends" in income_stmnt:
            return income_stmnt["PreferredStockDividends"].iloc[-1]
        else:
            return 0

    def get_eps_growth_current_quarter(self):
        current_quarter = [trend for trend in self.eps_growth_trends if trend["period"] == "0q"]
        return current_quarter[0]["growth"] if current_quarter else None

    def get_eps_growth_next_five_years(self):
        next_five_years = [trend for trend in self.eps_growth_trends if trend["period"] == "+5y"]
        return next_five_years[0]["growth"] if next_five_years else None




# This function should retrieve data for the given ticker and return a dictionary of this data
# def get_company_data(ticker):
#     ticker_sym = ticker_sym.upper()

#     # Make a query to see if we can even get data for this stock ticker
#     try:
#         stock_data = Ticker(ticker_sym, validate=True, progress=True)

#     except Exception as exc:
#         print(f"Error: Unable to retrieve data for ticker "{ticker_sym}".")
#         print(f"Error Details: {str(exc)}")
#         exit(1)


#     # Cache the api calls, so we dont have to do it multiple times in the dict for specific members
#     income_stmnt = stock_data.income_statement() # Income statement
#     cash_flow_stmnt = stock_data.cash_flow() # Cash flow statement
#     balance_sheet = stock_data.balance_sheet(trailing=True)  # Balance sheet TTM
#     key_stock_stats = stock_data.key_stats[ticker_sym]  # Some key stats (used for trailing_eps, )
#     eps_data_from_earning_hist = stock_data.earning_history # EPS calc from earning history
#     eps_growth_trends = stock_data.earnings_trend[ticker_sym]["trend"] # EPS Trends: eps growth is retrieved from this


#     # Get the preferred dividends
#     if "PreferredStockDividends" in income_stmnt:
#         preferred_dividends = income_stmnt["PreferredStockDividends"].iloc[-1]
#     else:
#         preferred_dividends = 0



#     eps_growth_current_quarter = [trend for trend in eps_growth_trends if trend["period"] == "0q"] # EPS growth for current quarter
#     eps_growth_current_quarter = eps_growth_current_quarter[0]["growth"] 

#     eps_growth_next_five_yrs = [trend for trend in eps_growth_trends if trend["period"] == "+5y"] # EPS growth for the next five years
#     eps_growth_next_five_yrs = eps_growth_next_five_yrs[0]["growth"]


#     company_data = {
#         "company_full_name" : stock_data.price[ticker_sym]["longName"], # Company full name
#         "company_profile" : stock_data.asset_profile[ticker_sym], # Company asset profile (location, operation...etc)
#         "current_price" : stock_data.financial_data[ticker_sym]["currentPrice"], # Current price
#         "shares_outstanding" : stock_data.key_stats[ticker_sym]["sharesOutstanding"], # Shares Outstanding
#         "income_statement" : income_stmnt, # income statement
#         "balance_sheet" : balance_sheet, # balance sheet
#         "cash_flow_statement" : cash_flow_stmnt, # cash flow statement
#         "trailing_eps_ttm" : key_stock_stats[ticker_sym]["trailingEps"], # TTM EPS
#         "net_income_ttm" : income_stmnt.iloc[-1]["NetIncome"], # Trailing Twelve months net income
#         "eps_data_from_earnings_history" : eps_data_from_earning_hist, # EPS data from earnings history
#         "eps_growth_trends" : eps_growth_trends, # Trend data for earnings and revenue data
#         "preferred_dividends" : preferred_dividends, # Preferred dividends
#         "eps_growth_current_quarter" : eps_growth_current_quarter, # Current quarter eps growth
#         "eps_growth_next_five_years" : eps_growth_next_five_yrs # EPS growth next five years

#     }   

#     # eps_data_from_earning_hist = eps_data_from_earning_hist.drop(columns=["maxAge"]) # Drop the columns we dont care about
#     # eps_data_to_print = eps_data_from_earning_hist.reset_index(drop=True).values.tolist() # Convert it to a list for printing, with the dropped cols
#     # eps_actual_total = sum(row[0] for row in eps_data_to_print) # Get the total 12 Month EPS
#     # eps_actual_total = round(eps_actual_total, 2) # Round
#     # eps_data_to_print = [row[::-1] for row in eps_data_to_print] # Reverse columns

#     # eps_data_to_print.append(["", "", "", "", "Current Year EPS", eps_actual_total]) # Append the 12 Month eps to the table
#     # headers = ["Period", "Quarter", "Surprise Percent", "EPS Difference", "EPS Estimate", "EPS Actual"] # Setup the headers

#     return company_data

