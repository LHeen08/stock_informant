from flask import Flask, render_template, request, jsonify
from data_collection import CompanyData

app = Flask(__name__)

# Define a route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Define a route to handle form submission
@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    ticker = request.form['ticker']  # Get the ticker symbol from the form
    
    company_data = CompanyData(ticker)
    company_data_dict = company_data.to_dict()

    return jsonify(company_data_dict)

if __name__ == '__main__':
    app.run(debug=True)
