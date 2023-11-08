from flask import Flask, render_template, request, jsonify
from data_collection import try_fetch_stock_data

app = Flask(__name__)


app.secret_key = 'my_flask_app'  # Replace with your own secret key

# Initialize a variable to store the fetched data ( this is the actual object of the stock )
fetched_company_data = None

# Define a route to render the HTML page
@app.route('/')
def index():
    # Start at our home page (ticker entry)
    return render_template('ticker-entry-page.html')


# Define a route to the ticker to fetch, this just tries to fetch the data, if successful it populated global data and rerturns success
@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    global fetched_company_data # Using global fetched data
    ticker = request.form['ticker']  # Get the ticker symbol from the form
    
    # Try to fetch the data
    try:
        fetched_company_data = try_fetch_stock_data(ticker)
        if fetched_company_data:
            # Get modules to retrieve
            return jsonify({'success': True}), 200
        else:
            # Return an error response with an appropriate status code
            return jsonify({'error': 'Company data not found'}), 404
    except Exception as e:
        # Handle any exceptions and return an error response with a status code
        return jsonify({'error': str(e)}), 500



@app.route('/data_page', methods=['GET', 'POST'])
def display_main_page():
    global fetched_company_data

    return render_template('data-page.html', data=fetched_company_data)


@app.route('/calculate_valuation_methods', methods=['POST'])
def calculate_valuation_methods():
    global fetched_company_data
    # TODO: Need to take into account a margin of safety



    # return dcf_response


if __name__ == '__main__':
    # For VM
    app.run(debug=True, host='10.0.2.15', port='5000')
    # app.run(debug=True, host='127.0.0.1', port='8000')




