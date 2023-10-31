# This file holds helper functions for main code

# Formatting functions
def format_value(value):
    if value >= 1e9:
        return f'{value/1e9:.2f}B'
    elif value >= 1e6:
        return f'{value/1e6:.2f}M'
    return str(value)


# Benjamin graham formula 
# Function to calculate benjamin grahams formula (old)
def calc_benjamin_graham_old(eps, pe_no_growth, growth_rate_next_five_yrs, avg_yield_aaa_corp_bond, current_yield_aaa_corp_bond):
	intrinsic_value = ((eps * (pe_no_growth + (2 * growth_rate_next_five_yrs)) * avg_yield_aaa_corp_bond) / current_yield_aaa_corp_bond)
	return intrinsic_value



# Function to calculate benjamin grahams formula new
def calc_benjamin_graham_new(eps, pe_no_growth, growth_rate_next_five_yrs, avg_yield_aaa_corp_bond, current_yield_aaa_corp_bond):
	intrinsic_value = ((eps * (pe_no_growth + (2 * growth_rate_next_five_yrs)) * avg_yield_aaa_corp_bond) / current_yield_aaa_corp_bond)
	return intrinsic_value



# Calculate dcf based off last 5 years of cash flow
def calculate_dcf(data_for_dcf):
    # extract this data for easier usage
    prev_cash_flows = data_for_dcf['PreviousCashFlows']
    discount_rate = data_for_dcf['DiscountRate']
    perpetual_growth_rate = data_for_dcf['PerpetualGrowthRate']
    cash_and_cash_equiv = data_for_dcf['CashAndCashEquivalentsAndShortTermInvestments']
    total_debt = data_for_dcf['TotalDebt']
    shares_outstanding = data_for_dcf['SharesOutstanding']
    projected_growth_rate = data_for_dcf['ProjectedGrowthRate']


    # Return a dictionary of all my values
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

    current_year = prev_cash_flows[len(prev_cash_flows) - 1][0].year
    previous_year_fcf = most_recent_FCF_val # set previous to most recent

    dcf_estimated_fcf_dict = {}

    for yr in range(1, 10):
        # caculate estimated fcf: previous year * (1+projected growth rate)
        estimated_fcf = round(previous_year_fcf * ( 1 + projected_growth_rate), 2)
        previous_year_fcf = estimated_fcf
        # print("Year: ", yr + current_year, " Estimated FCF: ", estimated_fcf)
        dcf_estimated_fcf_dict[yr+current_year] = estimated_fcf 
    

    last_estimated_fcf = dcf_estimated_fcf_dict[max(dcf_estimated_fcf_dict.keys())]    

    terminal_val = last_estimated_fcf * (1+perpetual_growth_rate)/(discount_rate - perpetual_growth_rate)

    dcf_present_value_of_FCFF = {}

    # Now using that, calculate the present value of future free cash flow
    # Thats the estimated FFCF / (1+DiscountRate)^year_out
    for future_yr in range(1, 10):

        pv_of_ffcf = round(dcf_estimated_fcf_dict[future_yr+current_year] / ( 1 + discount_rate)**future_yr, 2)
        dcf_present_value_of_FCFF[future_yr+current_year] = pv_of_ffcf 
    
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
