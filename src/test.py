# Testing
from data_collection import try_fetch_stock_data
from valuation_functions import *
from yahooquery import Ticker, Screener
from Levenshtein import distance
import json

TICKER = "xom"

if __name__ == "__main__":
    TICKER = TICKER.upper()
    # try:
    # test_data = Ticker(TICKER, validate=True)
    #     treasury_data = Ticker("^TYX").summary_detail["^TYX"]
    #     success = True
    # except Exception as e:
    #     print("ERROR getting company data: " + str(e))
    
    # print(test_data.sec_filings)
        
    # if success:

    data = try_fetch_stock_data(TICKER)

    # stats = test_data.summary_profile[TICKER]
    # # Store the current: TICKER, sector, and industry
    # current_ticker = TICKER
    # current_sector = stats["sector"].lower()
    # current_industry = stats["industry"].lower()

    # print("Current Sector: ", current_sector, " Current Industry: ", current_industry)


    # screen = Screener()
    # # all_avail_screeners = Screener().available_screeners

    # # Main sectors
    # main_sectors = [
    #     'ms_basic_materials',
    #     'ms_communication_services',
    #     'ms_consumer_cyclical',
    #     'ms_consumer_defensive',
    #     'ms_energy',
    #     'ms_financial_services',
    #     'ms_healthcare',
    #     'ms_industrials',
    #     'ms_real_estate',
    #     'ms_technology',
    #     'ms_utilities',
    # ]

    # # Find closest match to the sector
    # # closest_matches = get_close_matches(current_sector, filtered_screeners)
    # closest_match = min(main_sectors, key=lambda category: distance(category.lower(), current_sector.lower()))
    # print(f"Closest match: '{current_sector}' is '{closest_match}'")

    # # Get 10 symbols from the list, look up those 10 symbols summary 
    # # profile and compare the sector and industry to the current stock. 
    # # If they are the same use them
    # # Get the following from each: ev/ebitda, peg and pe ratios
    # # Look through 25 (default)
    # similar_matches = screen.get_screeners(closest_match)
    
    # similar_comps_list = []

    # # Iterate over each closest match
    # if closest_match in similar_matches:
    #     # Iterate over quotes for the current closest match
    #     for quote in similar_matches[closest_match]["quotes"]:
    #         if quote["symbol"] != current_ticker:
    #             similar_comps_list.append(quote["symbol"])
    # else:
    #     print(f"No quotes found for '{closest_match}'")

    # tickers = Ticker(similar_comps_list, asynchronous=True, validate=True)

    # filtered_tickers = []

    # # Get exact matches first
    # for ticker, data in tickers.summary_profile.items():
    #     sector_key = data.get("sector", "").lower()
    #     industry_key = data.get("industry", "").lower()

    #     if sector_key == current_sector and industry_key == current_industry:
    #         # Add the ticker and its data to the list
    #         filtered_tickers.append((ticker, data))

    # # Check if the length of filtered_tickers is less than 5
    # if len(filtered_tickers) < 5:
    #     # Create a set of tickers already in filtered_tickers
    #     existing_tickers = set(ticker_data[0] for ticker_data in filtered_tickers)

    #     # Iterate through tickers and add non-matching ones to filtered_tickers
    #     for ticker, data in tickers.summary_profile.items():
    #         sector_key = data.get("sectorKey", "").lower()
    #         industry_key = data.get("industryKey", "").lower()

    #         # Check if the ticker is not already in filtered_tickers and matches the sector and industry
    #         if ticker not in existing_tickers and sector_key == current_sector and industry_key == current_industry:
    #             # Add the ticker and its data to the list
    #             filtered_tickers.append((ticker, data))

    #         # Check if the length of filtered_tickers is 5
    #         if len(filtered_tickers) == 5:
    #             break

    # # Now filtered_tickers contains up to 5 tickers that match your criteria

    # # Print the resulting list
    # # print(filtered_tickers)


    # multiples = {}
    # # Access methods on the original Ticker object
    # for ticker, data in filtered_tickers:
    #     print("ticker: ", ticker)
    #     print("Company name: ", tickers.price[ticker]["longName"])
    #     try:
    #         peg_ratio = tickers.key_stats[ticker]["pegRatio"]
    #         peg_ratio = round(peg_ratio, 2)
    #     except KeyError:
    #         peg_ratio = "N/A"

    #     try:
    #         pe_ratio = tickers.summary_detail[ticker]["trailingPE"]
    #         pe_ratio = round(pe_ratio, 2)
    #     except KeyError:
    #         pe_ratio = "N/A"

    #     print("PEG Ratio: ", peg_ratio)
    #     print("PE Ratio: ", pe_ratio)
    #     print("EV/EBITDA: ", tickers.key_stats[ticker]["enterpriseToEbitda"])
    
    


    # # Convert Python to JSON  
    # json_object = json.dumps(similar_matches, indent = 4) 

    # # # # Convert and write JSON object to file
    # with open("test.json", "w") as outfile: 
    #     print(json_object, file=outfile)

 

    # Recommendations, we should base recommendations off of dcf, peter lynch, benjamin graham, graham number and then do analyst recommendations
    # FIRST START WITH ANALYST recommendations



