# Test file for testing stock predition
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from yahooquery import Ticker
from datetime import timezone

# Defining main function 
def main(): 

    stock_data = Ticker('googl')
    stock_hist = stock_data.history(period='10y', interval='1mo')
    stock_hist = stock_hist.reset_index()

    extracted_hist = stock_hist[['date', 'close']].copy()

    # Convert 'date' column to datetime
    extracted_hist['date'] = pd.to_datetime(extracted_hist['date'])

    # Remove timezone information from the 'date' column
    extracted_hist['date'] = extracted_hist['date'].dt.tz_localize(None)

    # Remove timezone information from the 'date' column
    # print(extracted_hist)

    m = Prophet(weekly_seasonality=True, yearly_seasonality=True)
    m.fit(extracted_hist.rename(columns={'date': 'ds', 'close': 'y'}))

    future = m.make_future_dataframe(periods=365, include_history=True)
    future.tail()

    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    plot = plot_components_plotly(m, forecast)
    plot.write_html("forcast_components.html")

  
# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main() 