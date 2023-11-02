from flask import Flask, render_template, request, jsonify, session
from data_collection import *

app = Flask(__name__)

app.secret_key = 'my_flask_app'  # Replace with your own secret key

# Define a route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Define a route to handle form submission
@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    ticker = request.form['ticker']  # Get the ticker symbol from the form
    company_data = get_company_data(ticker)
    # company_data['income_statement'] = company_data['income_statement'].to_dict(orient="records")
    # company_data['cash_flow_statement'] = company_data['cash_flow_statement'].to_dict(orient="records")
    # company_data['balance_sheet'] = company_data['balance_sheet'].to_dict(orient="records")

    session['fetched_data'] = company_data  # Store fetched data in session
    return "Data has been fetched."



@app.route('/display_data', methods=['GET'])
def display_data():
    fetched_data = session.get('fetched_data', None)
    response_html = f"<p>Company Name: {fetched_data['company_full_name']}</p>"
    response_html += f"<p>Current Price: {fetched_data['current_price']}</p>"
    response_html += f"<p>Shares Outstanding: {fetched_data['shares_outstanding']}</p>"
    response_html += f"<p>Trailing EPS (TTM): {fetched_data['trailing_eps_ttm']}%</p>"
    response_html += f"<p>Net Income (TTM): {fetched_data['net_income_ttm']}</p>"
    response_html += f"<p>EPS Growth Estimate next 5 Years: {fetched_data['eps_growth_next_five_years']:.2f}%</p>"
    return response_html

if __name__ == '__main__':
    app.run(debug=True)


