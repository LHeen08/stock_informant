# Testing
from data_collection import try_fetch_stock_data
from valuation_functions import *
from yahooquery import Ticker
import json

TICKER = "whr"


if __name__ == "__main__":
    # try:
    #     test_data = Ticker(TICKER)
    #     treasury_data = Ticker("^TYX").summary_detail["^TYX"]
    #     success = True
    # except Exception as e:
    #     print("ERROR getting company data: " + str(e))
        
        
    # if success:
    #     modules_to_retrieve = "assetProfile summaryDetail price summaryProfile defaultKeyStatistics earningsTrend financialData"
    #     cash_flow_to_use = test_data.cash_flow().to_dict(orient="records")
    #     modules = test_data.get_modules(modules_to_retrieve)[TICKER]
        
    #     # Serializing json
    #     # json_object = json.dumps(modules, indent=4)
        
    #     # Writing to sample.json
    #     # with open("test.json", "w") as outfile:
    #     #     outfile.write(json_object)

    #     current_treasury_data_aaa_bond = (treasury_data["dayLow"] + treasury_data["dayHigh"]) / 2 
    #     average_treasury_data_aaa_bond = treasury_data["twoHundredDayAverage"]

    #     # Test peter lynch values:
    #     # GOOGL
    #     peg_ratio = modules["defaultKeyStatistics"]["pegRatio"]
    #     pe_ratio = modules["summaryDetail"]["trailingPE"]
    #     eps = modules["defaultKeyStatistics"]["trailingEps"]
    #     dividend_yield = modules["summaryDetail"]["dividendYield"]
    #     next_five_years = [trend for trend in modules["earningsTrend"]["trend"] if trend["period"] == "+5y"]
    #     eps_growth_rate = next_five_years[0]["growth"] if next_five_years else None
    #     bvps = modules["defaultKeyStatistics"]["bookValue"]

    #     print("Peter Lynch: ", calculate_peter_lynch_formulas(eps, eps_growth_rate, peg_ratio, pe_ratio, dividend_yield))

    #     # Test graham number
    #     # print("BVPS: ", bvps)
    #     print("graham number : ", calculate_graham_number(eps, bvps))
        
    #     # Test ben graham formula
    #     print("Ben graham: ", calculate_benjamin_graham_new(eps, eps_growth_rate, average_treasury_data_aaa_bond,  current_treasury_data_aaa_bond))
        
    #     for entry in cash_flow_to_use:
    #         entry["asOfDate"] = entry["asOfDate"].strftime("%Y-%m-%d")

    #     # print(m)
    #     cash_and_cash_equiv = modules["financialData"]["totalCash"]
    #     total_debt = modules["financialData"]["totalDebt"]
    #     shares = modules["defaultKeyStatistics"]["sharesOutstanding"]
        
    #     dcf_data = calculate_dcf_free_cash_flow(cash_flow_to_use, cash_and_cash_equiv, 
    #                                             total_debt, shares, eps_growth_rate, .10, .03)
        
    #     # margin_of_safety = .30
    #     print("DCF Val w/ MOS: ", dcf_data["DCFVal"])
        
    data = try_fetch_stock_data(TICKER)
    
    # print(data)
    
    peter_lynch = calculate_peter_lynch_formulas(data["eps"], data["eps_growth_rate"], data["peg_ratio"], data["pe_ratio"], data["dividend_yield"])
    
    graham_number = calculate_graham_number(data["eps"], data["bvps"])
    
    ben_graham = calculate_benjamin_graham_new(data["eps"], data["eps_growth_rate"], data["avg_treasury_aaa"], data["current_treasury_aaa"])
    
    dcf_val = calculate_dcf_free_cash_flow(data["cash_flow_data"], data["cash_and_cash_equiv"], data["total_debt"], data["shares"], data["eps_growth_rate"], .10, .02)
    
    print("Peter Lynch: ", peter_lynch)
    print("Graham Number: ", graham_number)
    print("Ben Graham: ", ben_graham)
    print("DCF Val: ", dcf_val["DCFVal"])

        
