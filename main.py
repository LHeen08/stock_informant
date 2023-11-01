# Main driver for code
from tabulate import tabulate
from data_collection import *
from helper_functions import *

def main():

    company_data = CompanyData('AAPL')

    


    print(tabulate([["Performing analysis on:", str()], ["Ticker: ", str(ticker_sym)]], 
                    headers=["Company Info"],tablefmt="mixed_grid")) # Output a print that we are gathering data for the company name

    basic_data_to_print = [["Current Price", current_price], ["Net Income", format_value(net_income_ttm)], 
                       ["Shares Outstanding", format_value(shares_outstanding)], 
                       ["Preferred Dividends", format_value(preferred_dividends)]] # Basic financial data about the company
    
    print("\n\nBasic Financials for: ", company_full_name)
    print(tabulate(basic_data_to_print, headers=["Attribute", "Value"], tablefmt="mixed_grid", floatfmt=".2f"))


    print("\n\nEPS Quarters: ")
    print(tabulate(eps_data_to_print, headers, tablefmt="mixed_grid")) # Print the table


    print("\n\n\n")
    print("EPS calc: ", round(net_income_ttm/shares_outstanding, 2)) 
    print("Basic - Trailing EPS: ", trailing_eps_ttm)
    print("Forward PE: ", round(key_stock_stats["forwardPE"], 2))
    print("Current P/E(TTM): ", round(current_price/key_stock_stats["trailingEps"], 2))

    print("Current quarter future eps growth: ", f"{eps_growth_current_quarter:.2%}")
    print("Next 5 years future eps growth: ", f"{eps_growth_next_five_yrs:.2%}")


    ben_graham_old_intrinsic_value = round(calc_benjamin_graham_old(trailing_eps_ttm, 8.5, eps_growth_next_five_yrs, 4.4, 4.8), 2)
    print("Benjamin graham old: ", ben_graham_old_intrinsic_value)

    ben_graham_new_intrinsic_value = round(calc_benjamin_graham_old(trailing_eps_ttm, 7, eps_growth_next_five_yrs, 4.4, 4.8), 2)
    print("Benjamin graham new: ", ben_graham_new_intrinsic_value)




    # for index, row in cash_flow_stmnt.iterrows():
    #     cash_flow = row["FreeCashFlow"]
    #     print(f"Row {index}: free cash flow = {cash_flow}")
    cash_flow_years = [(row["asOfDate"].year, row["FreeCashFlow"]) for index, row in cash_flow_stmnt.tail(5).iterrows()]

    for i in range(1, len(cash_flow_years)):
            growth_rate = ((cash_flow_years[i][1] - cash_flow_years[i-1][1]) / cash_flow_years[i-1][1]) * 100
            cash_flow_years[i] = (*cash_flow_years[i], round(growth_rate, 2))

    total_growth_rate = 0
    for i in range(1, len(cash_flow_years)):
         total_growth_rate = total_growth_rate + cash_flow_years[i][2]


    average_growth_rate = total_growth_rate / (len(cash_flow_years) - 1)  # Subtract 1 to exclude the first row

    # Append the "Average Growth Rate" to the list
    cash_flow_years.append(("", "AVG Growth Rate", average_growth_rate))    
    print(tabulate(cash_flow_years, headers=["Year", "Free Cash Flow", "Growth Rate", "Average Growth Rate"], tablefmt="mixed_grid", floatfmt=".2f"))
    
    
    # Create a list of (year, cash_flow) pairs from the DataFrame
    cash_flow_years = [(row["asOfDate"], row["FreeCashFlow"]) for index, row in cash_flow_stmnt.tail(5).iterrows()]

    # Calculate DCF values
    discount_rate = .10
    perpetual_growth_rate = .025
    data_for_dcf = {
         "PreviousCashFlows" : cash_flow_years,
         "DiscountRate" : discount_rate,
         "PerpetualGrowthRate" : perpetual_growth_rate,
         "CashAndCashEquivalentsAndShortTermInvestments" : balance_sheet["CashCashEquivalentsAndShortTermInvestments"].iloc[-1],
         "TotalDebt" : balance_sheet["TotalDebt"].iloc[-1],
         "SharesOutstanding" : shares_outstanding,
         "ProjectedGrowthRate" : eps_growth_next_five_yrs
    }
    dcf_table = calculate_dcf(data_for_dcf)
    # print(dcf_table)

#     df = pd.DataFrame(dcf_table.items(), columns=["Year" , "Amount"])
#     print(tabulate(df, tablefmt="mixed_grid", floatfmt=".2f"))

    dcf_table["PrevCashFlows"] = [(entry[0].year, entry[1]) if len(entry) == 2 else (entry[0].year, entry[1], entry[2]) for entry in dcf_table["PrevCashFlows"]]

    # Create the table for Previous Cash Flows and Growth Rate
    prev_cash_flows_table = pd.DataFrame(dcf_table["PrevCashFlows"], columns=["Year", "Free Cash Flow", "Growth Rate"])
    avg_growth_rate = {"Year": "Average Growth Rate", "Free Cash Flow": dcf_table["AverageGrowthRate"]}
    prev_cash_flows_table = pd.concat([prev_cash_flows_table, pd.DataFrame([avg_growth_rate])], ignore_index=True)
    prev_cash_flows_table.index += 1

    # Create the table for Estimated FFCF, PVFFCF, Terminal Val, and Terminal Val PVFFCF
    est_ffcf_table = pd.DataFrame(dcf_table["EstimatedFFCF"].items(), columns=["Year", "Estimated FFCF"])
    est_ffcf_table["PVFFCF"] = est_ffcf_table["Year"].map(dcf_table["PVFFCF"])
    terminal_row = {"Year": "Terminal Val", "Estimated FFCF": dcf_table["TerminalVal"], "PVFFCF": dcf_table["TerminalValPVFFCF"]}
    terminal_row_df = pd.DataFrame([terminal_row])

    # Concatenate the DataFrames
    est_ffcf_table = pd.concat([est_ffcf_table, terminal_row_df], ignore_index=True)
    est_ffcf_table.index += 1

    # Print or display the tables
    print("Table 1: Previous Cash Flows and Growth Rate")
    print(tabulate(prev_cash_flows_table, headers="keys", tablefmt="mixed_grid", floatfmt=".2f", showindex=False))

    print("\nTable 2: Estimated FFCF, PVFFCF, Terminal Val, and Terminal Val PVFFCF")
    print(tabulate(est_ffcf_table, headers="keys", tablefmt="mixed_grid", floatfmt=".2f"))

    summary_data = {
        "Row": ["Sum of FFCF", "Cash and Cash Equivalents + Short Term Investments", "Total Debt", "Equity Value", "Shares Outstanding", "DCF Value"],
        "Amount": [
            dcf_table["SumOfFFCF"],  # Use .values to extract the scalar value from the Series
            data_for_dcf["CashAndCashEquivalentsAndShortTermInvestments"],
            data_for_dcf["TotalDebt"],
            dcf_table["EquityVal"],
            shares_outstanding,
            dcf_table["DCFVal"]
        ]
    }

    summary_table = pd.DataFrame(summary_data)
    print(tabulate(summary_table, headers="keys", tablefmt="mixed_grid", floatfmt=".2f", showindex=False))

if __name__=="__main__": 
    main()