# This file is to collect data and put what I actually need into useful items to use in other areas
from yahooquery import Ticker
import math
from valuation_functions import calculate_benjamin_graham_new, calculate_dcf_free_cash_flow, calculate_graham_number, calculate_peter_lynch_formulas



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

    # Convert date and timestamps to strings, dont add to list if FreeCashFlow is nan
    prev_free_cash_flows = [(entry["asOfDate"].strftime("%Y-%m-%d")[:4], entry["FreeCashFlow"]) 
                            for entry in cash_flow_to_use if not math.isnan(entry.get("FreeCashFlow"))]

    
    modules = stock_data.get_modules(modules_to_retrieve)[ticker] # get the modules listed above

    current_treasury_data_aaa_bond = (treasury_data["dayLow"] + treasury_data["dayHigh"]) / 2 # treasury data
    average_treasury_data_aaa_bond = treasury_data["twoHundredDayAverage"] # treasury data
    
    company_name = modules["price"]["longName"] # company long name
    current_price = modules["financialData"]["currentPrice"] # current price
    company_summary = modules["summaryProfile"]["longBusinessSummary"] # Summary of business
    market_cap = modules["price"]["marketCap"] # market cap

    # See if Beta is N/A
    try:
        beta = modules["summaryDetail"]["beta"] # beta
        beta = round(beta, 2)
    except KeyError:
        beta = "N/A"
    
    peg_ratio = modules["defaultKeyStatistics"]["pegRatio"] # peg ratio
    # If pe ratio is N/A:
    try:
        pe_ratio = modules["summaryDetail"]["trailingPE"]
        pe_ratio = round(pe_ratio, 2)
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
    

    # Perform the initial calculations
    peter_lynch_vals = calculate_peter_lynch_formulas(eps, eps_growth_rate, peg_ratio, pe_ratio, dividend_yield)
    graham_num = calculate_graham_number(eps, bvps)
    if graham_num != "N/A: Negative Number":
        graham_num = round(graham_num, 2)
    ben_graham_calc = calculate_benjamin_graham_new(eps, eps_growth_rate, average_treasury_data_aaa_bond, current_treasury_data_aaa_bond)

    default_discount = .10
    default_terminal_growth = .02
    dcf_val = calculate_dcf_free_cash_flow(prev_free_cash_flows, cash_and_cash_equiv, total_debt, shares, eps_growth_rate, default_discount, default_terminal_growth)


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
        "pe_ratio" : pe_ratio,
        "eps" : eps, 
        "dividend_yield" : format(dividend_yield, ".2"), 
        "bvps" : bvps,
        "eps_growth_rate" : format(eps_growth_rate, ".2"), 
        "cash_and_cash_equiv" : cash_and_cash_equiv,
        "total_debt" : total_debt,
        "shares" : shares,
        "market_cap" : round(market_cap, 2),
        "beta" : beta,
        "peter_lynch_calcs" : peter_lynch_vals, 
        "graham_num" : graham_num, 
        "ben_graham_calc" : round(ben_graham_calc, 2), 
        "dcf_val" : dcf_val["DCFVal"],
        "default_discount" : default_discount, 
        "default_terminal_growth" : default_terminal_growth
    }
    
    return stock_fetched_data