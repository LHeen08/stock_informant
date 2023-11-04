from flask import Flask, render_template, request, jsonify, session
from data_collection import *
from helper_functions import *

app = Flask(__name__)


app.secret_key = 'my_flask_app'  # Replace with your own secret key

# Initialize a variable to store the fetched data ( this is the acutal object of the stock )
fetched_company_data = None

# Define a route to render the HTML page
@app.route('/')
def index():
    # Start at our home page (ticker entry)
    return render_template('start_page.html')


# Define a route to the ticker to fetch, this just tries to fetch the data, if successful it populated global data and rerturns success
@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    global fetched_company_data # Using global fetched data
    ticker = request.form['ticker']  # Get the ticker symbol from the form
    
    # Try to fetch the data
    try:
        fetched_company_data = CompanyData(ticker)
        if fetched_company_data:
            return jsonify({'success': True}), 200
        else:
            # Return an error response with an appropriate status code
            return jsonify({'error': 'Company data not found'}), 404
    except Exception as e:
        # Handle any exceptions and return an error response with a status code
        return jsonify({'error': str(e)}), 500



@app.route('/main_page', methods=['GET','POST'])
def display_main_page():
    global fetched_company_data


    return render_template('main_page.html')



@app.route('/calculate_dcf', methods=['POST'])
def calculate_dcf():
    global fetched_company_data

    #  Get the discount rate, growth rate and terminal growth rate from the user

    dcf_response = calculate_dcf_with_obj(fetched_company_data)

    return dcf_response

if __name__ == '__main__':
    # For VM
    # app.run(debug=True, host='10.0.2.15', port='5000')
    app.run(debug=True, host='127.0.0.1', port='8000')




