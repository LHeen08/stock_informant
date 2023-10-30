# Main driver for code
from tabulate import tabulate
from data_collection import *
from helper_functions import *

def main():
    print(tabulate([["Performing analysis on:", str(company_full_name)], ["Ticker: ", str(ticker_sym)]], 
                    headers=['Company Info'],tablefmt='mixed_grid')) # Output a print that we are gathering data for the company name

    basic_data_to_print = [["Current Price", current_price], ["Net Income", format_value(net_income_ttm)], 
                       ["Shares Outstanding", format_value(shares_outstanding)], 
                       ["Preferred Dividends", format_value(preferred_dividends)]] # Basic financial data about the company
    
    print("\n\nBasic Financials for: ", company_full_name)
    print(tabulate(basic_data_to_print, headers=['Attribute', 'Value'], tablefmt="mixed_grid", floatfmt=".2f"))


    print("\n\nEPS Quarters: ")
    print(tabulate(eps_data_to_print, headers, tablefmt="mixed_grid")) # Print the table


    print("\n\n\n")
    print("EPS calc: ", round(net_income_ttm/shares_outstanding, 2)) 
    print("Basic - Trailing EPS: ", trailing_eps_ttm)
    print("Forward PE: ", round(key_stock_stats['forwardPE'], 2))
    print("Current P/E(TTM): ", round(current_price/key_stock_stats['trailingEps'], 2))

    print("Current quarter future eps growth: ", f"{eps_growth_current_quarter:.2%}")
    print("Next 5 years future eps growth: ", f"{eps_growth_next_five_yrs:.2%}")


    ben_graham_old_intrinsic_value = round(calc_benjamin_graham_old(trailing_eps_ttm, 8.5, eps_growth_next_five_yrs, 4.4, 4.8), 2)
    print("Benjamin graham old: ", ben_graham_old_intrinsic_value)

    ben_graham_new_intrinsic_value = round(calc_benjamin_graham_old(trailing_eps_ttm, 7, eps_growth_next_five_yrs, 4.4, 4.8), 2)
    print("Benjamin graham new: ", ben_graham_new_intrinsic_value)


    # for index, row in cash_flow_stmnt.iterrows():
    #     cash_flow = row['FreeCashFlow']
    #     print(f"Row {index}: free cash flow = {cash_flow}")
    cash_flow_years = [(row['asOfDate'].year, row['FreeCashFlow']) for index, row in cash_flow_stmnt.tail(5).iterrows()]

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
    cash_flow_years = [(row['asOfDate'], row['FreeCashFlow']) for index, row in cash_flow_stmnt.tail(5).iterrows()]

    # Calculate DCF values
    discount_rate = .10
    dcf_values = calculate_dcf(cash_flow_years, discount_rate)

    # Print the results
    print(tabulate(dcf_values, headers = ["Year", "DCF"], tablefmt="mixed_grid", floatfmt=".2f"))
    



if __name__=="__main__": 
    main()