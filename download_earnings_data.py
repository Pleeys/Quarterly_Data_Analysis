import os
import pandas as pd
import requests
from datetime import datetime, timedelta

api_key = os.getenv('AV_KEY')

def date_to_quarter(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    year = date_obj.year
    month = date_obj.month
    quarter = (month - 1) // 3 + 1
    return f'Q{quarter}-{year}'

def get_data(tickers, api_key):
    quarterly_earnings = []

    for ticker in tickers:
        earnings_url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={api_key}'
        earnings_response = requests.get(earnings_url)
        earnings_data = earnings_response.json().get('quarterlyEarnings', [])

        historical_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={api_key}&outputsize=full&datatype=json'
        historical_response = requests.get(historical_url)
        historical_data = historical_response.json().get('Time Series (Daily)', {})

        for quarter in earnings_data:
            date = quarter['reportedDate']
            surprise_percentage = round(float(quarter.get('surprisePercentage', 0) or 0), 2)
            quarter_date = date_to_quarter(date)

            if date in historical_data:
                close_price = float(historical_data[date]['4. close'])
                next_day = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                percentage_change = None

                if next_day in historical_data:
                    next_day_open = float(historical_data[next_day]['1. open'])
                    percentage_change = round(((next_day_open - close_price) / close_price) * 100, 2)

                if percentage_change is not None:
                    quarterly_earnings.append({
                        'Date': quarter_date,
                        'SurprisePercentage': surprise_percentage,
                        'PercentageChange': percentage_change
                    })

    return quarterly_earnings

def download_quarterly_earnings(tickers, api_key, file_name):
    data = get_data(tickers, api_key)
    processed_df = pd.DataFrame(data, columns=['Date', 'SurprisePercentage', 'PercentageChange'])
    processed_df.to_csv(file_name, index=False)
    print(f'Created CSV file: {file_name}')

tickers = ["GOOGL"]
download_quarterly_earnings(tickers, api_key, 'earnings_data.csv')
