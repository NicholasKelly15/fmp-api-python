# Financial Modeling Prep API Wrapper
Python wrapper package to request historical, real-time, and fundamental stock data from the Financial Modeling Prep API. Currently only supports a subset of the endpoints available under the personal plan. 

# Install
An API key is needed and may be obtained at the [FMP website](https://site.financialmodelingprep.com/).

The package may be installed with the command: 
```
pip install fmp_api_python
```

# Usage

## Creating the Client
To make calls to the api, first import the package and create an instance of the client:
```
from fmp_api_python.fmp import FMPClient
client = FMPClient(<your api key>)
```
Alternatively, your api key may be stored in the environment variable under the name FMP_API_KEY. In this case, creating the instance may be done simply with:
```
client = FMPClient()
```

## Making API Calls
The full documentation of existing methods for the FMPClient class can be viewed [here](https://nicholaskelly15.github.io/fmp_api_python_documentation/). Note that while most methods take a parameter 'return_type' which can be either 'json' or 'df' for pandas.DataFrame, some do not and can only return one of these types. The default return type is usually json if left unspecified. The following are a few example calls: 
```
response = client.income_statement(symbol='AAPL', period='quarter', limit=10, return_type='json')
response = client.balance_sheet(symbol='AAPL', period='annual', limit=None, return_type='df')
response = client.quote('AAPL', 'df')
response = client.historical_price_full('AAPL', return_type='df')
response = client.batch_request_end_of_day_prices('2020-01-01')   # Returns pd.DataFrame, json not supported
response = client.is_the_market_open()    # Returns json, pd.DataFrame not supported
```

