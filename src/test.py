# Testing
from data_collection import try_fetch_stock_data
from valuation_functions import *
from yahooquery import Ticker, Screener
from Levenshtein import distance
import json

TICKER = "aapl"

if __name__ == "__main__":
    TICKER = TICKER.upper()
    # try:
    test_data = Ticker(TICKER)
    #     treasury_data = Ticker("^TYX").summary_detail["^TYX"]
    #     success = True
    # except Exception as e:
    #     print("ERROR getting company data: " + str(e))
    
    print(test_data.sec_filings)
        
    # if success:

    # data = try_fetch_stock_data(TICKER)

    stats = test_data.summary_profile[TICKER]
    # Store the current: TICKER, sector, and industry
    current_ticker = TICKER
    current_sector = stats["sectorKey"]
    current_industry = stats["industryKey"]

    print("Current Sector: ", current_sector, " Current Industry: ", current_industry)


    screen = Screener()
    # all_avail_screeners = Screener().available_screeners

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

    # Find closest match to the sector
    # closest_matches = get_close_matches(current_sector, filtered_screeners)
    closest_match = min(main_sectors, key=lambda category: distance(category.lower(), current_sector.lower()))
    print(f"Closest match: '{current_sector}' is '{closest_match}'")

    # Get 10 symbols from the list, look up those 10 symbols summary 
    # profile and compare the sector and industry to the current stock. 
    # If they are the same use them
    # Get the following from each: ev/ebitda, peg and pe ratios
    # Look through 25 (default)
    similar_matches = screen.get_screeners(closest_match)
    
    similar_comps_list = []

    # Iterate over each closest match
    if closest_match in similar_matches:
        # Iterate over quotes for the current closest match
        for quote in similar_matches[closest_match]["quotes"]:
            if quote["symbol"] != current_ticker:
                similar_comps_list.append(quote["symbol"])
    else:
        print(f"No quotes found for '{closest_match}'")

    tickers = Ticker(similar_comps_list, asynchronous=True, validate=True)

    good_match = []
    # # Get each companys summary profile to compare industry and sector, add those to a new list
    for ticker, data in tickers.summary_profile.items():
        sector_key = data.get("sectorKey", "").lower()
        industry_key = data.get("industryKey", "").lower()

        print("TICKER: ", ticker, " sector: ", sector_key, " industry: ", industry_key)

        if sector_key == current_sector and industry_key == current_industry:
            good_match.append(ticker)


    # Check if the good_match list has fewer than 5 elements
    if len(good_match) < 5:
        # Create a set of tickers already in good_match
        existing_tickers = set(good_match)

        # Iterate through tickers and add non-matching ones to good_match
        for ticker, data in tickers.summary_profile.items():
            sector_key = data.get("sectorKey", "").lower()
            industry_key = data.get("industryKey", "").lower()

            # Check if the ticker is not already in good_match and matches the sector and industry
            if ticker not in existing_tickers:
                good_match.append(ticker)


    print(good_match)

    # Convert Python to JSON  
    json_object = json.dumps(similar_matches, indent = 4) 

    # # # Convert and write JSON object to file
    with open("test.json", "w") as outfile: 
        print(json_object, file=outfile)

 



