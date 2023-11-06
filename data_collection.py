# This file is to collect data and put what I actually need into useful items to use in other areas
from yahooquery import Ticker
import json

from helper_functions import calculate_dcf_with_obj


# What data is needed for every calculation
# Peter Lynch evaluation: Notes Earnings growth rate * earnings





class CompanyData:
    def __init__(self, ticker):
        self.ticker = str(ticker).upper()
        try:
            stock_data = Ticker(ticker, validate=True, progress=True)
            treasury_data = Ticker('^TYX').summary_detail['^TYX']

        except Exception as exc:
            raise ValueError(f"Error: Unable to retrieve data for ticker {ticker}. Error Details: {str(exc)}")

        # Set instance variables for data attributes
        self.company_full_name = stock_data.price[self.ticker]["longName"]
        self.company_profile = stock_data.asset_profile[self.ticker]
        self.current_price = stock_data.financial_data[self.ticker]["currentPrice"]
        self.shares_outstanding = stock_data.key_stats[self.ticker]["sharesOutstanding"]
        self.income_statement = self.convert_to_dict(stock_data.income_statement())
        self.balance_sheet = self.convert_to_dict(stock_data.balance_sheet(trailing=True))
        self.cash_flow_statement = self.convert_to_dict(stock_data.cash_flow())
        self.trailing_eps_ttm = stock_data.key_stats[self.ticker]["trailingEps"]
        self.net_income_ttm = self.income_statement[-1]["NetIncome"]
        self.eps_data_from_earnings_history = self.convert_earnings_hist_to_dict(stock_data.earning_history)
        self.eps_growth_trends = stock_data.earnings_trend[self.ticker]["trend"]
        self.preferred_dividends = self.get_preferred_dividends()
        self.eps_growth_current_quarter = self.get_eps_growth_current_quarter()
        self.eps_growth_next_five_years = self.get_eps_growth_next_five_years()
        self.current_treasury_data_aaa_bond = (treasury_data['dayLow'] + treasury_data['dayHigh']) / 2 
        self.average_treasury_data_aaa_bond = treasury_data['twoHundredDayAverage']
        self.ben_graham_new = self.get_ben_graham_new()
        self.ben_graham_old = self.get_ben_graham_old()

    def convert_to_dict(self, data):
        data_dict = data.to_dict(orient="records")
        self.convert_timestamps_to_strings(data_dict)
        return data_dict

    def convert_timestamps_to_strings(self, data):
        for entry in data:
            entry['asOfDate'] = entry['asOfDate'].strftime('%Y-%m-%d')


    def convert_earnings_hist_to_dict(self, earning_hist):
        return earning_hist.to_dict(orient="records")

    def get_preferred_dividends(self):
        income_stmnt = self.income_statement
        if "PreferredStockDividends" in income_stmnt:
            return income_stmnt[-1]["PreferredStockDividends"]
        else:
            return 0

    def get_eps_growth_current_quarter(self):
        current_quarter = [trend for trend in self.eps_growth_trends if trend["period"] == "0q"]
        return current_quarter[0]["growth"] if current_quarter else None

    def get_eps_growth_next_five_years(self):
        next_five_years = [trend for trend in self.eps_growth_trends if trend["period"] == "+5y"]
        return next_five_years[0]["growth"] if next_five_years else None
    

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
 
    
    def get_ben_graham_new(self):
        intrinsic_value = round(((self.trailing_eps_ttm * (7 + (1 * self.eps_growth_next_five_years)) * self.average_treasury_data_aaa_bond) / self.current_treasury_data_aaa_bond), 2)
        return intrinsic_value
    
    def get_ben_graham_old(self):
        intrinsic_value = round(((self.trailing_eps_ttm * (8.5 + (2 * self.eps_growth_next_five_years)) * self.average_treasury_data_aaa_bond) / self.current_treasury_data_aaa_bond), 2)
        return intrinsic_value


# company_data = CompanyData('JPM')

# cash_flow_years = [(entry['asOfDate'], entry['FreeCashFlow']) for entry in company_data.cash_flow_statement]
# print(cash_flow_years)

# for i in range(1, len(cash_flow_years)):
#         growth_rate = ((cash_flow_years[i][1] - cash_flow_years[i-1][1]) / cash_flow_years[i-1][1]) * 100
#         cash_flow_years[i] = (*cash_flow_years[i], round(growth_rate, 2))
#         print(growth_rate)

# total_growth_rate = 0
# for i in range(1, len(cash_flow_years)):
#         total_growth_rate = total_growth_rate + cash_flow_years[i][2]

# average_growth_rate = total_growth_rate / (len(cash_flow_years) - 1)  # Subtract 1 to exclude the first row
# print(average_growth_rate)



# print(calculate_dcf_with_obj(company_data))

