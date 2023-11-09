# Testing
from data_collection import try_fetch_stock_data
from valuation_functions import *
from yahooquery import Ticker
import json

TICKER = "googl"


if __name__ == "__main__":
    # try:
    #     test_data = Ticker(TICKER)
    #     treasury_data = Ticker("^TYX").summary_detail["^TYX"]
    #     success = True
    # except Exception as e:
    #     print("ERROR getting company data: " + str(e))
        
        
    # if success:

    data = try_fetch_stock_data(TICKER)

    # Convert Python to JSON  
    json_object = json.dumps(data, indent = 4) 

    # Convert and write JSON object to file
    with open("test.json", "w") as outfile: 
        print(json_object, file=outfile)

 
    # print(data)
    
    # peter_lynch = calculate_peter_lynch_formulas(data["eps"], data["eps_growth_rate"], data["peg_ratio"], data["pe_ratio"], data["dividend_yield"])
    
    # graham_number = calculate_graham_number(data["eps"], data["bvps"])
    
    # ben_graham = calculate_benjamin_graham_new(data["eps"], data["eps_growth_rate"], data["avg_treasury_aaa"], data["current_treasury_aaa"])
    
    # dcf_val = calculate_dcf_free_cash_flow(data["cash_flow_data"], data["cash_and_cash_equiv"], data["total_debt"], data["shares"], data["eps_growth_rate"], .10, .02)
    
    

        
