# Testing
from data_collection import CompanyData
from valuation_functions import *
from yahooquery import Ticker
import json

TICKER = "GOOGL"


if __name__ == "__main__":
    try:
        test_data = Ticker(TICKER)
        treasury_data = Ticker("^TYX").summary_detail["^TYX"]
        success = True
    except Exception as e:
        print("ERROR getting company data: " + str(e))
        
        
    if success:
        modules_to_retrieve = "assetProfile summaryDetail price summaryProfile defaultKeyStatistics earningsTrend"
        cash_flow_to_use = test_data.cash_flow().to_dict(orient="records")

        modules = test_data.get_modules(modules_to_retrieve)[TICKER]
        # print("All needed modules: ", json.dumps(modules, sort_keys=True, indent=4))
        # print to file
        # Serializing json
        # json_object = json.dumps(modules, indent=4)
        
        # # Writing to sample.json
        # with open("test.json", "w") as outfile:
        #     outfile.write(json_object)

        current_treasury_data_aaa_bond = (treasury_data["dayLow"] + treasury_data["dayHigh"]) / 2 
        average_treasury_data_aaa_bond = treasury_data["twoHundredDayAverage"]

        # Test peter lynch values:
        # GOOGL
        peg_ratio = modules["defaultKeyStatistics"]["pegRatio"]
        pe_ratio = modules["summaryDetail"]["trailingPE"]
        eps = modules["defaultKeyStatistics"]["trailingEps"]
        dividend_yield = modules["summaryDetail"]["dividendYield"]
        next_five_years = [trend for trend in modules["earningsTrend"]["trend"] if trend["period"] == "+5y"]
        eps_growth_rate = next_five_years[0]["growth"] if next_five_years else None
        bvps = modules["defaultKeyStatistics"]["bookValue"]

        print("Peter Lynch: ", calculate_peter_lynch_formulas(eps, eps_growth_rate, peg_ratio, pe_ratio, dividend_yield))

        # Test graham number
        print("BVPS: ", bvps)
        print("graham number : ", calculate_graham_number(eps, bvps))
        
        # Test ben graham formula
        print("Ben graham: ", calculate_benjamin_graham_new(eps, eps_growth_rate, average_treasury_data_aaa_bond,  current_treasury_data_aaa_bond))
        
        for entry in cash_flow_to_use:
            entry["asOfDate"] = entry["asOfDate"].strftime("%Y-%m-%d")


        dcf_needs = test_data.get_financial_data(trailing=True)
        print(dcf_needs)
        cash_and_cash_equiv = dcf_needs["CashAndCashEquivalents"]
        total_debt = dcf_needs["TotalDebt"]
        shares = modules["defaultKeyStatistics"]["sharesOutstanding"]
        
        dcf_data = calculate_dcf_free_cash_flow(cash_flow_to_use, cash_and_cash_equiv, 
                                                total_debt, shares, eps_growth_rate, .20, .03)
        
        margin_of_safety = .30
        print("DCF Val w/ MOS: ", dcf_data["DCFVal"]*margin_of_safety)
        
        
        
        
