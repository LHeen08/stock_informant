from flask import Flask, render_template, request, jsonify, session
from data_collection import *
from helper_functions import *

app = Flask(__name__)


app.secret_key = 'my_flask_app'  # Replace with your own secret key

# Initialize a variable to store the fetched data ( this is the acutal object of the stock )
fetched_data = None

# Define a route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')


# Define a route to handle form submission
@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    global fetched_data
    ticker = request.form['ticker']  # Get the ticker symbol from the form
    fetched_data = CompanyData(ticker)
    if fetched_data:
        response_data = {
            'company_name': fetched_data.company_full_name,
            'ticker' : ticker.upper(),
            'current_price': fetched_data.current_price,
            'shares_outstanding': fetched_data.shares_outstanding,
            'trailing_eps_ttm' : fetched_data.trailing_eps_ttm,
            'eps_growth_next_five_years' : fetched_data.eps_growth_next_five_years,
            'net_income_ttm' : fetched_data.net_income_ttm,
            'ben_graham_new' : fetched_data.ben_graham_new,
            'ben_graham_old' : fetched_data.ben_graham_old,
        }
    else:
        response_data = None
    
    return response_data


@app.route('/calculate_dcf', methods=['POST'])
def calculate_dcf():
    global fetched_data

    dcf_response = calculate_dcf_with_obj(fetched_data)

    return dcf_response

if __name__ == '__main__':
    # For VM
    app.run(debug=True, host='10.0.2.15', port='5000')
    # app.run(debug=True, host='127.0.0.1', port='5000')




