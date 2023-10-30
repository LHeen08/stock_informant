# Main driver for code
from tabulate import tabulate
from data_collection import *
from helper_functions import *

def main():
    print(tabulate([["Performing analysis on:", str(company_full_name)], ["Ticker: ", str(ticker_sym)]], 
                    headers=['Company Info'],tablefmt='mixed_grid')) # Output a print that we are gathering data for the company name

    basic_data_to_print = [["Current Price", current_price], ["Net Income", format_value(net_income)], 
                       ["Shares Outstanding", format_value(shares_outstanding)], 
                       ["Preferred Dividends", format_value(preferred_dividends)]] # Basic financial data about the company
    
    print("\n\nBasic Financials for: ", company_full_name)
    print(tabulate(basic_data_to_print, headers=['Attribute', 'Value'], tablefmt="mixed_grid", floatfmt=".2f"))


    print("\n\nEPS Quarters: ")
    print(tabulate(eps_data_to_print, headers, tablefmt="mixed_grid")) # Print the table


    print("\n\n\n")
    print("EPS calc: ", round(net_income/shares_outstanding, 2)) 
    print("Basic - Trailing EPS: ", trailing_eps_ttm)
    print("Forward PE: ", round(key_stock_stats['forwardPE'], 2))
    print("Current P/E(TTM): ", round(current_price/key_stock_stats['trailingEps'], 2))

    print("Current quarter future eps growth: ", f"{eps_growth_current_quarter:.2%}")
    print("Next 5 years future eps growth: ", f"{eps_growth_next_five_yrs:.2%}")


    ben_graham_old_intrinsic_value = round(calc_benjamin_graham_old(trailing_eps_ttm, 8.5, eps_growth_next_five_yrs, 4.4, 4.8), 2)
    print("Benjamin graham old: ", ben_graham_old_intrinsic_value)

    ben_graham_new_intrinsic_value = round(calc_benjamin_graham_old(trailing_eps_ttm, 7, eps_growth_next_five_yrs, 4.4, 4.8), 2)
    print("Benjamin graham new: ", ben_graham_new_intrinsic_value)




if __name__=="__main__": 
    main()