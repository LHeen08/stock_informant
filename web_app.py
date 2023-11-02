from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from data_collection import *

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# app.secret_key = 'my_flask_app'  # Replace with your own secret key

# Initialize a variable to store the fetched data
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
            'current_price': fetched_data.current_price,
            # Add other data here
        }
    else:
        response_data = {
            'company_name': 'N/A',
            'current_price': 'N/A',
            # Add other data here
        }
    
    return jsonify(response_data)


@app.route('/display_data', methods=['POST'])
def display_data():  
    global fetched_data
    response_html = f"<p>Shares Outstanding: {fetched_data.shares_outstanding}</p>"
    response_html += f"<p>Trailing EPS (TTM): {fetched_data.trailing_eps_ttm}%</p>"
    response_html += f"<p>Net Income (TTM): ${fetched_data.net_income_ttm:,.2f}</p>"
    response_html += f"<p>EPS Growth Estimate next 5 Years: {fetched_data.eps_growth_next_five_years * 100:.2f}%</p>"
    
    return response_html



if __name__ == '__main__':
    app.run(debug=True, host='10.0.2.15', port='5000')


