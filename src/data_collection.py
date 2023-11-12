# This file is to collect data and put what I actually need into useful items to use in other areas
from yahooquery import Ticker, Screener
import math
from valuation_functions import calculate_benjamin_graham_new, calculate_dcf_free_cash_flow, calculate_graham_number, calculate_peter_lynch_formulas
from Levenshtein import distance
import threading
import json

# Function to try and fetch the financial data
def try_fetch_stock_data(ticker):
    
    ticker = ticker.upper()
    
    try: # Try to get stock data
        stock_data = Ticker(ticker, validate=True, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
        
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


    current_sector = modules["summaryProfile"]["sector"].lower() # current company sector
    current_industry = modules["summaryProfile"]["industry"].lower() # current company industry

    # Create a dictionary to hold the result
    result_holder = {"multiples_valuation_companies": None}
    # Make another thread do this:
    thread = threading.Thread(target=find_multiples_valuation_companies, args=(ticker, current_sector, current_industry, result_holder))
    # Find similar companies to use for multiples valuation
    #  = multiples_valuation_find_companies(ticker, current_sector, current_industry)
    thread.start()

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
    
    try:    
        peg_ratio = modules["defaultKeyStatistics"]["pegRatio"] # peg ratio
        peg_ratio = round(peg_ratio, 2)
    except KeyError:
        peg_ratio = "N/A"
    
    # If pe ratio is N/A:
    try:
        pe_ratio = modules["summaryDetail"]["trailingPE"]
        pe_ratio = round(pe_ratio, 2)
    except KeyError:
        pe_ratio = "N/A"
        
    eps = modules["defaultKeyStatistics"]["trailingEps"] # eps ttm

    try:
        dividend_yield = modules["summaryDetail"]["dividendYield"] # dividend yield
        dividend_yield = dividend_yield
    except KeyError:
        dividend_yield = "N/A"

    bvps = modules["defaultKeyStatistics"]["bookValue"] # book value per share

    next_five_years = [trend for trend in modules["earningsTrend"]["trend"] if trend["period"] == "+5y"]
    eps_growth_rate = next_five_years[0]["growth"] if next_five_years else None # projected growth next 5 years
    
    try:
        ev_to_ebitda = modules["defaultKeyStatistics"]["enterpriseToEbitda"] # EV / EBITDA
        ev_to_ebitda = round(ev_to_ebitda, 2)
    except KeyError:
        ev_to_ebitda = "N/A"
        
    cash_and_cash_equiv = modules["financialData"]["totalCash"] # total cash
    total_debt = modules["financialData"]["totalDebt"] # total debt
    shares = modules["defaultKeyStatistics"]["sharesOutstanding"] # shares outstanding
    

    # Perform the initial calculations
    peter_lynch_vals = calculate_peter_lynch_formulas(eps, eps_growth_rate, peg_ratio, pe_ratio, dividend_yield)
    graham_num = calculate_graham_number(eps, bvps)
    if graham_num != "N/A: Negative Number":
        graham_num = round(graham_num, 2)
    ben_graham_calc = calculate_benjamin_graham_new(eps, eps_growth_rate, average_treasury_data_aaa_bond, current_treasury_data_aaa_bond)

    default_discount_percent = 10
    default_terminal_growth_percent = 2
    default_margin_of_safety = 10
    dcf_val = calculate_dcf_free_cash_flow(prev_free_cash_flows, cash_and_cash_equiv, total_debt, shares, eps_growth_rate, (default_discount_percent / 100), (default_terminal_growth_percent / 100), default_margin_of_safety)


    thread.join()
    multiples_valuation_companies = result_holder["multiples_valuation_companies"]

    # dictionary filled with useful data to return    
    stock_fetched_data = {
        "company_ticker" : ticker,
        "company_name" : company_name,
        "current_price" : round(current_price, 2),
        "company_summary" : company_summary,
        "cash_flow_data" : prev_free_cash_flows,
        "current_treasury_aaa" : round(current_treasury_data_aaa_bond, 2),
        "avg_treasury_aaa" : round(average_treasury_data_aaa_bond, 2),
        "peg_ratio" : peg_ratio, 
        "pe_ratio" : pe_ratio,
        "eps" : eps, 
        "dividend_yield" : dividend_yield, 
        "bvps" : round(bvps, 2),
        "ev_to_ebitda" : ev_to_ebitda,
        "eps_growth_rate_percent" : "{:.2f}".format(eps_growth_rate * 100), # Convert to percentage
        "cash_and_cash_equiv" : cash_and_cash_equiv,
        "total_debt" : total_debt,
        "shares" : shares,
        "market_cap" : round(market_cap, 2),
        "beta" : beta,
        "peter_lynch_calcs" : peter_lynch_vals, 
        "graham_num" : graham_num, 
        "ben_graham_calc" : round(ben_graham_calc, 2), 
        "dcf_val" : "{:.2f}".format(dcf_val["DCFVal"]),
        "default_discount_percent" : default_discount_percent, 
        "default_terminal_growth_percent" : default_terminal_growth_percent,
        "default_margin_of_safety" : default_margin_of_safety,
        "multiples_val_companies" : multiples_valuation_companies 
    }

    
    return stock_fetched_data


def find_multiples_valuation_companies(ticker, current_sector, current_industry, result_holder):
    result_holder["multiples_valuation_companies"] = multiples_valuation_find_companies(ticker, current_sector, current_industry)


# This function looks up similar companies using the Screener from yahooquery
# Returns a dict of multiples valuation
def multiples_valuation_find_companies(current_ticker, current_sector, current_industry):

    screener = Screener() # Screener 

    # Main sectors
    main_sectors = [
        'ms_basic_materials',
        'ms_communication_services',
        'ms_consumer_cyclical',
        'ms_consumer_defensive',
        'ms_energy',
        'ms_financial_services',
        'ms_healthcare',
        'ms_industrials',
        'ms_real_estate',
        'ms_technology',
        'ms_utilities',
    ]    
    
    # find closest match to the current sector
    closest_match = min(main_sectors, key=lambda category: distance(category.lower(), current_sector.lower()))

    try:
        similar_matches = screener.get_screeners(closest_match) # Get companies with screener (default of 25 items)
    except Exception as e:
        print("Unable to get similar stocks: ", e)
        return {e}
    

    similar_comps_list = []

    if closest_match in similar_matches:
        # Iterate over quotes for the current closest match
        for quote in similar_matches[closest_match]["quotes"]:
            if quote["symbol"] != current_ticker:
                similar_comps_list.append(quote["symbol"])
    else:
        print(f"No quotes found for '{closest_match}'")

    tickers = Ticker(similar_comps_list, asynchronous=True, validate=True, retry=10, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
    
    modules = ["defaultKeyStatistics", "summaryProfile", "quoteType", "summaryDetail"]
    
    fetched_data = tickers.get_modules(modules)
    
    index_by_industry = {}
    
    for ticker, company_data in fetched_data.items():
        industry = company_data["summaryProfile"]["industry"].lower()
        
        if industry not in index_by_industry:
            index_by_industry[industry] = set()
        index_by_industry[industry].add(ticker)
        
    
    industry_matches = index_by_industry.get(current_industry, set())
    while len(industry_matches) < 5:
        for other_industry, other_tickers in index_by_industry.items():
            if other_industry != current_industry.lower():
                additional_tickers = list(other_tickers - industry_matches)
                industry_matches.update(additional_tickers)
                if len(industry_matches) >= 5:
                    break  # Stop if we have enough tickers
        if len(industry_matches) >= 5:
            break  # Stop the outer loop if we have enough tickers

    industry_matches_list = list(industry_matches)[:5]
    
    list_of_companies_w_data = {}
    # modules = ["defaultKeyStatistics", "summaryDetail", "quoteType"]
    
    # Access methods on the original Ticker object
    for ticker in industry_matches_list:
        try:
            peg_ratio = fetched_data[ticker]["defaultKeyStatistics"]["pegRatio"]
            peg_ratio = round(peg_ratio, 2)
        except KeyError:
            peg_ratio = "N/A"

        try:
            pe_ratio = fetched_data[ticker]["summaryDetail"]["trailingPE"]
            pe_ratio = round(pe_ratio, 2)
        except KeyError:
            pe_ratio = "N/A"
            
        try:
            ev_to_ebitda = fetched_data[ticker]["defaultKeyStatistics"]["enterpriseToEbitda"]
            ev_to_ebitda = round(ev_to_ebitda, 2)
        except KeyError:
            ev_to_ebitda = "N/A"

        # Add information to the dictionary
        list_of_companies_w_data[ticker] = {
            "company_name": fetched_data[ticker]["quoteType"]["longName"],
            "peg": peg_ratio,
            "pe": pe_ratio,
            "ev/ebitda": ev_to_ebitda
        }


    return list_of_companies_w_data