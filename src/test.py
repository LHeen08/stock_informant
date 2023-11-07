# Testing
from data_collection import CompanyData
from valuation_functions import *
from yahooquery import Ticker
import json

TICKER = 'GOOGL'


if __name__ == '__main__':
    try:
        test_data = Ticker(TICKER)
        success = True
    except Exception as e:
        print("ERROR getting company data: " + str(e))
        
        
    if success:
        modules_to_retrieve = "assetProfile price recommendationTrend financialData incomeStatementHistory cashflowStatementHistory earningsHistory earnings defaultKeyStatistics earningsTrend industryTrend sectorTrend balanceSheetHistory balanceSheetHistoryQuarterly"

        # modules = test_data.get_modules(modules_to_retrieve)[TICKER]
        # print("All needed modules: ", json.dumps(modules, sort_keys=True, indent=4))
        # print to file
        # Serializing json
        # json_object = json.dumps(modules, indent=4)
        
        # Writing to sample.json
        # with open("test.json", "w") as outfile:
        #     outfile.write(json_object)
        
        
        # Test peter lynch values:
        # GOOGL
        peg_ratio = 1.22
        pe_ratio = 24.73
        eps = 5.21
        dividend_yield = 1.41
        eps_growth_rate = 19.03
        print("Peter Lynch: ", calculate_peter_lynch_formulas(eps, eps_growth_rate, peg_ratio, pe_ratio, dividend_yield))

        # Test graham number
        bvps = 50.39
        print("graham number : ", calculate_graham_number(eps, bvps))
        
        # Test ben graham formula
        print("Ben graham: ", calculate_benjamin_graham_new(eps, eps_growth_rate, 4.4,  5.43))
        

        cash_flow_to_use = test_data.cash_flow().to_dict(orient="records")
        for entry in cash_flow_to_use:
            entry['asOfDate'] = entry['asOfDate'].strftime('%Y-%m-%d')

        cash_and_cash_equiv = 29640000000
        total_debt = 41193000000
        shares = 3960000000

        
        dcf_data = calculate_dcf_free_cash_flow(cash_flow_to_use, cash_and_cash_equiv, 
                                                total_debt, shares, .4272, .20, .03)
        
        margin_of_safety = .30
        print("DCF Val w/ MOS: ", dcf_data["DCFVal"]*margin_of_safety)
        
        
        
        
