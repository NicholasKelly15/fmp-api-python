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


