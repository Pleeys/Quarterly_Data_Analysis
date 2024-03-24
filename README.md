# Quarterly_Data_Analysis

## Overview
This repository hosts a collection of Python scripts designed to fetch, analyze, and predict quarterly financial data using the Alpha Vantage API. It is aimed at financial analysts, data scientists, and hobbyists interested in stock market trends and earnings data. The toolkit facilitates the downloading of quarterly earnings data, construction of regression models to understand trends, and forecasting future quarterly financial metrics.

### Programs Included:
1. **Data Downloader** - Downloads quarterly earnings data and historical adjusted daily stock prices for specified tickers.
2. **Regression Model Constructor** - Constructs local and moving linear regression models to analyze the relationship between surprise percentage in earnings reports and subsequent stock price changes.
3. **Quarterly Data Forecaster** - Utilizes constructed models to predict future stock price changes based on new earnings data.

## Getting Started

### Prerequisites
- Python 3.6+
- Pandas
- NumPy
- scikit-learn
- An API key from Alpha Vantage

### Installation
1. Clone this repository to your local machine.
2. Install required Python libraries using pip:
3. Sign up for an API key at [Alpha Vantage](https://www.alphavantage.co/support/#api-key) and set it as an environment variable `AV_KEY`.

### Usage

#### Data Downloader
To download quarterly earnings and historical price data, run:
python download_earnings_data.py

### Regression Model Constructor
After downloading the data, you can construct regression models to analyze the data:
python create_moving_model.py

### Quarterly Data Forecaster
To make predictions based on the regression models:
python earnings_forecast.py

### Before running the scripts, ensure you have set your Alpha Vantage API key as an environment variable:
export AV_KEY='YourAlphaVantageAPIKey'
