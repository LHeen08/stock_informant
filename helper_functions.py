# This file holds helper functions for main code

# Formatting functions
def format_value(value):
    if value >= 1e9:
        return f"{value/1e9:.2f}B"
    elif value >= 1e6:
        return f"{value/1e6:.2f}M"
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
