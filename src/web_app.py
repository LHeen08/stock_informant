from flask import Flask, render_template, request, jsonify
from data_collection import try_fetch_stock_data
from valuation_functions import calculate_dcf_free_cash_flow, calculate_peter_lynch_formulas, calculate_benjamin_graham_new
import platform


app = Flask(__name__)


app.secret_key = "my_flask_app"  # Replace with your own secret key

# Initialize a variable to store the fetched data ( this is the actual object of the stock )
fetched_company_data = None

# Define a route to render the HTML page
@app.route("/")
def index():
    # Start at our home page (ticker entry)
    return render_template("ticker-entry-page.html")


# Define a route to the ticker to fetch, this just tries to fetch the data, if successful it populated global data and returns success
@app.route("/fetch_data", methods=["POST"])
def fetch_data():
    global fetched_company_data # Using global fetched data
    ticker = request.form["ticker"]  # Get the ticker symbol from the form
    
    # Try to fetch the data
    try:
        fetched_company_data = try_fetch_stock_data(ticker)
        if fetched_company_data:
            # Get modules to retrieve
            return jsonify({"success": True}), 200
        else:
            # Return an error response with an appropriate status code
            return jsonify({"error": "Company data not found"}), 404
    except Exception as e:
        # Handle any exceptions and return an error response with a status code
        return jsonify({"error": str(e)}), 500



@app.route("/data_page", methods=["GET", "POST"])
def display_main_page():
    global fetched_company_data

    return render_template("data-page.html", data=fetched_company_data)


@app.route("/calculate_dcf", methods=["POST"])
def calculate_dcf():
    global fetched_company_data
    
    # Convert the values from the request
    eps_growth = float(request.values["epsGrowth"]) / 100 # Divide by 100
    discount_rate = float(request.values["discountRate"]) / 100 # Divide by 100
    terminal_growth_rate = float(request.values["terminalGrowthRate"]) / 100 # Divide by 100
    margin_of_safety = float(request.values["marginOfSafety"])
    
    calc_func_return_data = calculate_dcf_free_cash_flow(fetched_company_data["cash_flow_data"], 
                                                         fetched_company_data["cash_and_cash_equiv"], 
                                                         fetched_company_data["total_debt"], 
                                                         fetched_company_data["shares"], 
                                                         eps_growth, discount_rate, 
                                                         terminal_growth_rate, margin_of_safety)
    
    # just get the dcf value from the return of the function
    dcfVal = calc_func_return_data["DCFVal"]

    
    # print("web app:", dcfVal)
    dcfVal = round(dcfVal, 2) # Round to 2 decimal places
    print("calculate_dcf() return:", dcfVal)

    return jsonify({"dcfVal": dcfVal})




@app.route("/calculate_peter_lynch", methods=["POST"])
def calculate_peter_lynch():
    global fetched_company_data

    # Convert the values from the request 
    eps_growth = float(request.values["epsGrowth"]) / 100

    calc_peter_lynch = calculate_peter_lynch_formulas(fetched_company_data["eps"], 
                                                      eps_growth, 
                                                      fetched_company_data["peg_ratio"], 
                                                      fetched_company_data["pe_ratio"], 
                                                      fetched_company_data["dividend_yield"])
    print("calculate peter lynch")
    return calc_peter_lynch

@app.route("/calculate_ben_graham", methods=["POST"])
def calculate_ben_graham():
    global fetched_company_data

    # Convert the values from the request 
    eps_growth = float(request.values["epsGrowth"]) / 100

    calc_bg = calculate_benjamin_graham_new(fetched_company_data["eps"], 
                                            eps_growth,
                                            fetched_company_data["avg_treasury_aaa"],
                                            fetched_company_data["current_treasury_aaa"])
    
    calc_bg = round(calc_bg, 2)
    
    print("ben graham")

    return jsonify({"bg_val": calc_bg})





if __name__ == "__main__":
    if platform.system() == "Darwin" :
        app.run(debug=True, host="127.0.0.1", port="8000") # Using port 8000 for mac...
    # else:
        # app.run(debug=True, host="127.0.0.1", port="5000")
    
    # Used for VM
    app.run(debug=True, host="10.0.2.15", port="5000")




