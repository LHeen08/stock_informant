# This file is to collect data and put what I actually need into useful items to use in other areas
from yahooquery import Ticker



# Function to try and fetch the financial data
def try_fetch_stock_data(ticker):
    
    ticker = ticker.upper()
    
    try: # Try to get stock data
        stock_data = Ticker(ticker, validate=True)
        
        try: # Try to get treasury data
            treasury_data = Ticker("^TYX").summary_detail["^TYX"]
        except Exception as exc:
            raise ValueError(f"Error: Unable to retrieve data for ticker ^TYX. Error Details: {str(exc)}")
        
    except Exception as exc:
        raise ValueError(f"Error: Unable to retrieve data for ticker {ticker}. Error Details: {str(exc)}")

    
    modules_to_retrieve = "assetProfile summaryDetail price summaryProfile defaultKeyStatistics earningsTrend financialData" # modules to get from object
    cash_flow_to_use = stock_data.cash_flow().to_dict(orient="records") # get cash flow to use for dcf
    for entry in cash_flow_to_use:
        entry["asOfDate"] = entry["asOfDate"].strftime("%Y-%m-%d") # convert timestamps to strings
    
    prev_free_cash_flows = [(entry["asOfDate"][:4], entry["FreeCashFlow"]) for entry in cash_flow_to_use]   
    
    modules = stock_data.get_modules(modules_to_retrieve)[ticker] # get the modules listed above
    
    current_treasury_data_aaa_bond = (treasury_data["dayLow"] + treasury_data["dayHigh"]) / 2 # treasury data
    average_treasury_data_aaa_bond = treasury_data["twoHundredDayAverage"] # treasury data
    
    company_name = modules["price"]["longName"] # company long name
    current_price = modules["financialData"]["currentPrice"] # current price
    company_summary = modules["summaryProfile"]["longBusinessSummary"] # Summary of business
    market_cap = modules["price"]["marketCap"] # market cap
    beta = modules["summaryDetail"]["beta"] # beta
    
    peg_ratio = modules["defaultKeyStatistics"]["pegRatio"] # peg ratio
    try:
        pe_ratio = modules["summaryDetail"]["trailingPE"]
    except KeyError:
        pe_ratio = "N/A"
    eps = modules["defaultKeyStatistics"]["trailingEps"] # eps ttm
    dividend_yield = modules["summaryDetail"]["dividendYield"] # dividend yield
    bvps = modules["defaultKeyStatistics"]["bookValue"] # book value per share

    next_five_years = [trend for trend in modules["earningsTrend"]["trend"] if trend["period"] == "+5y"]
    eps_growth_rate = next_five_years[0]["growth"] if next_five_years else None # projected growth next 5 years
    
    cash_and_cash_equiv = modules["financialData"]["totalCash"] # total cash
    total_debt = modules["financialData"]["totalDebt"] # total debt
    shares = modules["defaultKeyStatistics"]["sharesOutstanding"] # shares outstanding
    
    # dictionary filled with useful data to return    
    stock_fetched_data = {
        "company_ticker" : ticker,
        "company_name" : company_name,
        "current_price" : round(current_price, 2),
        "company_summary" : company_summary,
        "cash_flow_data" : prev_free_cash_flows,
        "current_treasury_aaa" : round(current_treasury_data_aaa_bond, 2),
        "avg_treasury_aaa" : round(average_treasury_data_aaa_bond, 2),
        "peg_ratio" : round(peg_ratio, 2), 
        "pe_ratio" : round(pe_ratio, 2), 
        "eps" : eps, 
        "dividend_yield" : dividend_yield, 
        "bvps" : bvps,
        "eps_growth_rate" : eps_growth_rate, 
        "cash_and_cash_equiv" : cash_and_cash_equiv,
        "total_debt" : total_debt,
        "shares" : shares,
        "market_cap" : round(market_cap, 2),
        "beta" : round(beta, 2)
    }
    
    return stock_fetched_data