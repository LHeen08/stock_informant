# Testing
from data_collection import CompanyData
from yahooquery import Ticker
import json

TICKER = 'AAPL'






# Calculate dcf based off last 5 years of cash flow
def test_calculate_dcf_with_obj(input_cashflow_stmnts, discount_rate, perpetual_growth_rate, cash_and_cash_equiv, total_debt, shares_outstanding, projected_growth):

    # Get the last few years of cash flow with their associated date
    cash_flow_years = [(entry['asOfDate'][:4], entry['FreeCashFlow']) for entry in input_cashflow_stmnts]

    # Calculate the growth rate for each previous year 
    for i in range(1, len(cash_flow_years)):
            growth_rate = ((cash_flow_years[i][1] - cash_flow_years[i-1][1]) / cash_flow_years[i-1][1]) * 100
            cash_flow_years[i] = (*cash_flow_years[i], round(growth_rate, 2))

    total_growth_rate = 0
    for i in range(1, len(cash_flow_years)):
         total_growth_rate = total_growth_rate + cash_flow_years[i][2]

    average_growth_rate = total_growth_rate / (len(cash_flow_years) - 1)  # Subtract 1 to exclude the first row


    # Calculate DCF values
    discount_rate = .10
    perpetual_growth_rate = .025
    data_for_dcf = {
         "PreviousCashFlows" : cash_flow_years,
         "DiscountRate" : discount_rate,
         "PerpetualGrowthRate" : perpetual_growth_rate,
         "CashAndCashEquivalents" : input_cashflow_stmnts.balance_sheet[-1]["CashAndCashEquivalents"],
         "TotalDebt" : input_cashflow_stmnts.balance_sheet[-1]["TotalDebt"],
         "SharesOutstanding" : input_cashflow_stmnts.shares_outstanding,
         "ProjectedGrowthRate" : input_cashflow_stmnts.eps_growth_next_five_years
    }


    # extract this data for easier usage
    prev_cash_flows = data_for_dcf["PreviousCashFlows"]
    discount_rate = data_for_dcf["DiscountRate"]
    perpetual_growth_rate = data_for_dcf["PerpetualGrowthRate"]
    cash_and_cash_equiv = data_for_dcf["CashAndCashEquivalents"]
    total_debt = data_for_dcf["TotalDebt"]
    shares_outstanding = data_for_dcf["SharesOutstanding"]
    projected_growth_rate = data_for_dcf["ProjectedGrowthRate"]
    curr_growth_rate = 0

    # Given the previous free cash flows, calculate the average growth rate between them
    for i in range(1, len(prev_cash_flows)):
        curr_growth_rate = ((prev_cash_flows[i][1] - prev_cash_flows[i-1][1]) / prev_cash_flows[i-1][1]) * 100
        prev_cash_flows[i] = (*prev_cash_flows[i], round(curr_growth_rate, 2))

    total_growth_rate = 0
    for i in range(1, len(prev_cash_flows)):
        total_growth_rate = total_growth_rate + prev_cash_flows[i][2]

    # Average growth rate
    average_growth_rate = round(total_growth_rate / (len(prev_cash_flows) - 1), 2)  # Subtract 1 to exclude the first row

    # Calculate the now estimated future free cash flow
    # That is, using the most recent FCF number * (1+growth rate projection)
    most_recent_FCF_val = prev_cash_flows[len(prev_cash_flows) - 1][1]

    current_year = prev_cash_flows[len(prev_cash_flows) - 1][0]
    previous_year_fcf = most_recent_FCF_val # set previous to most recent

    dcf_estimated_fcf_dict = {}

    for yr in range(1, 10):
        # caculate estimated fcf: previous year * (1+projected growth rate)
        estimated_fcf = round(previous_year_fcf * ( 1 + projected_growth_rate), 2)
        previous_year_fcf = estimated_fcf
        # print("Year: ", yr + current_year, " Estimated FCF: ", estimated_fcf)
        dcf_estimated_fcf_dict[str(yr + int(current_year))] = estimated_fcf    

    last_estimated_fcf = dcf_estimated_fcf_dict[max(dcf_estimated_fcf_dict.keys())]    

    terminal_val = last_estimated_fcf * (1+perpetual_growth_rate)/(discount_rate - perpetual_growth_rate)

    dcf_present_value_of_FCFF = {}

    # Now using that, calculate the present value of future free cash flow
    # Thats the estimated FFCF / (1+DiscountRate)^year_out
    for future_yr in range(1, 10):

        pv_of_ffcf = round(dcf_estimated_fcf_dict[str(future_yr+ int(current_year))] / ( 1 + discount_rate)**future_yr, 2)
        dcf_present_value_of_FCFF[str(future_yr+ int(current_year))] = pv_of_ffcf 
    
    terminal_val_pv_ffcf = round(terminal_val / (1 + discount_rate)**(future_yr+1), 2)

    sum_of_pv_of_FFCF = sum(dcf_present_value_of_FCFF.values()) + terminal_val_pv_ffcf

    equity_value = (sum_of_pv_of_FFCF + cash_and_cash_equiv) - total_debt

    dcf_val = equity_value / shares_outstanding

    data_to_return = {
        "PrevCashFlows" : prev_cash_flows,
        "AverageGrowthRate" : average_growth_rate, 
        "EstimatedFFCF" : dcf_estimated_fcf_dict,
        "TerminalVal" : terminal_val,
        "TerminalValPVFFCF" : terminal_val_pv_ffcf,
        "PVFFCF" : dcf_present_value_of_FCFF,
        "SumOfFFCF" : sum_of_pv_of_FFCF,
        "EquityVal" : equity_value,
        "DCFVal" : dcf_val
    }

    # Return a dictionary that includes all the useful info
    return data_to_return




if __name__ == '__main__':
    try:
        test_data = Ticker(TICKER)
        success = True
    except Exception as e:
        print("ERROR getting company data: " + str(e))
        
        
    if success:
        modules_to_retrieve = "assetProfile price recommendationTrend financialData incomeStatementHistory cashflowStatementHistory earningsHistory earnings defaultKeyStatistics earningsTrend industryTrend sectorTrend balanceSheetHistory balanceSheetHistoryQuarterly"

        modules = test_data.get_modules(modules_to_retrieve)[TICKER]
        # print("All needed modules: ", json.dumps(modules, sort_keys=True, indent=4))
        # print to file
        # Serializing json
        json_object = json.dumps(modules, indent=4)
        
        # Writing to sample.json
        with open("test.json", "w") as outfile:
            outfile.write(json_object)
        
        # discount_rate = 0.10
        # perpetual_growth_rate = 0.025
        # cash_and_cash_equiv = modules['balanceSheetHistory']['balanceSheetStatements'][0]['cashAndCashEquivalents']
        
        # I think we will have to grab the balance sheet in order to get ttm data for cash...which is fine, one more call
        
        # print("DCF: ", test_calculate_dcf_with_obj(modules['cashflowStatementHistory']['cashflowStatements'],))
        # test_obj = CompanyData(TICKER, test_data)
        # print("Name: ", test_data.price[TICKER]["longName"])
        # print("Price: ", test_data.financial_data[TICKER]["currentPrice"])
        # print("Asset profile: ", test_data.asset_profile[TICKER])
        # print("shares outstanding: ", test_data.key_stats[TICKER]["sharesOutstanding"])
        # print("income statement: ", test_data.income_statement())
        # print("balance sheet: ", test_data.balance_sheet(trailing=True))
        # print("cash flow statement: ", test_data.cash_flow())
        

        # print("Price: ", test_obj.current_price)
        # print("eps growth current quarter: ", test_obj.eps_growth_current_quarter)
        # print("eps growth next five years: ", test_obj.eps_growth_next_five_years)
        
        
        
