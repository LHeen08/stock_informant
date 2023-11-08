# This file will hold the functions for all valuation methods

# Peter Lynch evaluation:
# Methods: 
#           - guru focus: peg * eps growth * eps
#           - nasdaq: eps growth * eps
#           - my method: (eps growth + dividend yield) / pe
def calculate_peter_lynch_formulas(eps, eps_growth_rate, peg_ratio, pe_ratio, dividend_yield):
    peter_lynch_dict = {} # Dict for each method
    
    gurufocus_formula = (peg_ratio * eps_growth_rate * eps) # Calculate the GuruGocus formula
    peter_lynch_dict['gurufocus'] = gurufocus_formula
    
    nasdaq_formula = (eps_growth_rate * eps) # Calculate the NASDAQ formula
    peter_lynch_dict['nasdaq'] = nasdaq_formula
    
    if pe_ratio == "N/A":
         my_method = "N/A"
    else: 
        my_method = ((eps_growth_rate + dividend_yield) / pe_ratio) * 100 # Calculate the My method formula

    peter_lynch_dict['my_method'] = my_method
    
    return peter_lynch_dict
    
    

# Graham number calculation for calculating undervalued stocks
# Shows the maximum price that should be paid for a stock
# extermely defensive
def calculate_graham_number(eps, book_value_per_share):
    graham_number = (22.5 * eps * book_value_per_share)**(1/2)
    if isinstance(graham_number, complex):
         graham_number = "N/A: Negative Number"
    return graham_number    


# Benjamin graham formula
def calculate_benjamin_graham_new(eps, growth_rate_next_five_yrs, avg_yield_aaa_corp_bond, current_yield_aaa_corp_bond):
    intrinsic_value = ((eps * (7 + (1 * growth_rate_next_five_yrs)) * avg_yield_aaa_corp_bond) / current_yield_aaa_corp_bond)
    return intrinsic_value


# Discounted Cash Flow: 
# Discounted Free Cash Flow: returns dict of data calculated from function
def calculate_dcf_free_cash_flow(input_cashflow_stmnts, cash_and_cash_equiv, 
                                 total_debt, shares_outstanding, 
                                 projected_growth_rate, discount_rate, 
                                 perpetual_growth_rate):

    # Get the last few years of cash flow with their associated date
    # prev_cash_flows = [(entry['asOfDate'][:4], entry['FreeCashFlow']) for entry in input_cashflow_stmnts]
    prev_cash_flows = input_cashflow_stmnts

    # Calculate the growth rate for each previous year 
    for i in range(1, len(prev_cash_flows)):
            growth_rate = ((prev_cash_flows[i][1] - prev_cash_flows[i-1][1]) / abs(prev_cash_flows[i-1][1])) * 100
            prev_cash_flows[i] = (prev_cash_flows[i][0], prev_cash_flows[i][1],round(growth_rate, 2))

    total_growth_rate = 0 # init total growth rate to 0
    # For every year in the given previous cash flow years, calculate the total growth rate
    for i in range(1, len(prev_cash_flows)):
         total_growth_rate = total_growth_rate + prev_cash_flows[i][2]
    
    # Determine the average growth rate from the total growth rate 
    average_growth_rate = round(total_growth_rate / (len(prev_cash_flows) - 1), 2)  # Subtract 1 to exclude the first row

    most_recent_FCF_val = prev_cash_flows[len(prev_cash_flows) - 1][1] # Get the most recent free cash flow value

    current_year = prev_cash_flows[len(prev_cash_flows) - 1][0] # Get the current year: ex - '2023'
    previous_year_fcf = most_recent_FCF_val # set previous to most recent

    dcf_estimated_fcf_dict = {} # init dictionary to hold {'year': value}

    # For 10 years into the future, calculate the estimated free cash flow
    for yr in range(1, 10):
        estimated_fcf = round(previous_year_fcf * ( 1 + projected_growth_rate), 2) # calculate estimated fcf
        previous_year_fcf = estimated_fcf # set the previous year fcf to be the current estimated free cash flow as a placeholder for next iteration
        dcf_estimated_fcf_dict[str(yr + int(current_year))] = estimated_fcf # Set the next year in dictionary to be the estimated fcf for that year

    last_estimated_fcf = dcf_estimated_fcf_dict[max(dcf_estimated_fcf_dict.keys())] # Get the last estimated FCF     

    terminal_val = last_estimated_fcf * (1+perpetual_growth_rate)/(discount_rate - perpetual_growth_rate) # Calculate the terminal value estimated FCF

    dcf_present_value_of_FFCF = {} # init dictionary to hold present value future free cash flow {'year': value}

    # Now using that, calculate the present value of future free cash flow
    # Thats the estimated FFCF / (1+DiscountRate)^year_out
    for future_yr in range(1, 10):
        pv_of_ffcf = round(dcf_estimated_fcf_dict[str(future_yr+ int(current_year))] / (( 1 + discount_rate)**future_yr), 2) # Calculate present value of FFCF
        dcf_present_value_of_FFCF[str(future_yr+ int(current_year))] = pv_of_ffcf # Insert this year and amount into dictionary
    
    terminal_val_pv_ffcf = round(terminal_val / (1 + discount_rate)**(future_yr+1), 2) # Calculate the terminal value of present value FFCF

    sum_of_pv_of_FFCF = sum(dcf_present_value_of_FFCF.values()) + terminal_val_pv_ffcf # Calculate the sum of the present value future free cash flows

    equity_value = (sum_of_pv_of_FFCF + cash_and_cash_equiv) - total_debt # Calculate the equity value

    dcf_val = round(equity_value / shares_outstanding, 2) # Calculate the DCF value

    # TODO: Should this just return the DCF Val? 
    data_to_return = {
        "PrevCashFlows" : prev_cash_flows,
        "AverageGrowthRate" : average_growth_rate, 
        "EstimatedFFCF" : dcf_estimated_fcf_dict,
        "TerminalVal" : terminal_val,
        "TerminalValPVFFCF" : terminal_val_pv_ffcf,
        "PVFFCF" : dcf_present_value_of_FFCF,
        "SumOfFFCF" : sum_of_pv_of_FFCF,
        "EquityVal" : equity_value,
        "DCFVal" : dcf_val
    }

    # Return a dictionary that includes all the useful info
    return data_to_return
