"""Financial Modeling Prep API Wrapper.

An API key is needed and may be obtained at the [FMP website](https://site.financialmodelingprep.com/).

The package may be installed with the command: 
```
pip install fmp_api_python
```
"""


import requests
import os
import csv
import pandas as pd

from constants import BASE_URL_V3, BASE_URL_V4
from constants import TODAY


class FMPClient:
    """Python wrapper for the Financial Modeling Prep (FMP) API.
    
    Makes call requests to the FMP API and returns the results. Currently, 
    only some of the endpoints under the personal plan are implemented, and none 
    from the professional or enterprise versions. Most requests can have the response
    be formatted either in the original json or as a pandas.DataFrame, although 
    some enpoints do not have support for a DataFrame return.

    In order to use the API, an API key must be used. This can either be passed into 
    the constructor or added to the environmental variables under the name FMP_API_KEY.

    Args:
        api_key (str): FMP API key.
    """


    def __init__(self, api_key=None):
        self._api_key = api_key or os.getenv('FMP_API_KEY')
        self._empty_payload = {
            'apikey': self._api_key
        }

    def _convert_response(self, response, response_type, return_type):
        """Converts the response from the API into the given response type.
        
        Args:
            response (requests.models.response): API response from the requests.get method.
            response_type (str): 'json' | 'csv' depending on the type of API response.
            return_type (str): 'json' | 'df' depending on the desired return format.

        Returns: 
            Either a list or pandas.DataFrame with the response content.
        """
        if (response_type == 'json'):
            content = response.json()

            if (return_type == 'json'):
                return content
            elif (return_type == 'df'):
                return pd.DataFrame(content)

        elif (response_type == 'csv'):
            content = list(csv.reader(response.content.decode('utf-8').splitlines(), delimiter=','))

            if (return_type == 'df'):
                df = pd.DataFrame(list(content), )
                df = df.rename(columns=df.iloc[0], inplace=False).loc[1:]
                return df
            elif (return_type == 'json'):
                raise Exception('API returned csv format, unable to convert to JSON')

    def _merge_symbols_for_url(self, symbols):
        if (type(symbols) == str):
            return symbols
        elif (type(symbols) == list):
            return_string = ''
            for symbol in symbols:
                return_string += symbol + ','
            return return_string
        else:
            raise Exception('Unknown type given for symbols.')

    """------- STOCK FUNDAMENTALS -------"""

    def financial_statement_symbol_lists(self, return_type='json'):
        """List of symbols that have financial statements.
        
        Args:
            return_type (str): 'json' | 'df' depending on the desired return format.

        Returns: 
            Either a list or pandas.DataFrame with the stock symbols.
        """
        endpoint = r'{}/financial-statement-symbol-lists'.format(BASE_URL_V3)
        response = requests.get(url=endpoint, params=self._empty_payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    def income_statement(self, symbol, period='annual', limit=None, return_type='json'):
        """List of historical income statements for the symbol.
        
        Args:
            symbol (str): Stock ticker symbol.
            period (str): 'annual' | 'quarter'.
            limit (int): Maximum number of periods to return.
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the income statements.
        """
        endpoint = r'{}/income-statement/{}'.format(BASE_URL_V3, symbol)
        payload = {
            'apikey': self._api_key, 
            'period': period
        }
        if limit is not None:
            payload['limit'] = limit
        response = requests.get(url=endpoint, params=payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    def balance_sheet_statement(self, symbol, period='annual', limit=None, return_type='json'):
        """List of historical balance sheets for the symbol.
        
        Args:
            symbol (str): Stock ticker symbol.
            period (str): 'annual' | 'quarter'.
            limit (int): Maximum number of periods to return.
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the balance sheets.
        """
        endpoint = r'{}/balance-sheet-statement/{}'.format(BASE_URL_V3, symbol)
        payload = {
            'apikey': self._api_key, 
            'period': period
        }
        if limit is not None:
            payload['limit'] = limit
        response = requests.get(url=endpoint, params=payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    def cash_flow_statement(self, symbol, period='annual', limit=None, return_type='json'):
        """List of historical balance sheets for the symbol.
        
        Args:
            symbol (str): Stock ticker symbol.
            period (str): 'annual' | 'quarter'.
            limit (int): Maximum number of periods to return.
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the cash flow statements.
        """
        endpoint = r'{}/cash-flow-statement/{}'.format(BASE_URL_V3, symbol)
        payload = {
            'apikey': self._api_key, 
            'period': period
        }
        if limit is not None:
            payload['limit'] = limit
        response = requests.get(url=endpoint, params=payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    def financial_report_dates(self, symbol, return_type='json'):
        """Returns dates and links to data.
        
        Args:
            symbol (str): Stock ticker symbol.
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the report dates.
        """
        endpoint = r'{}/financial-reports-dates'.format(BASE_URL_V4)
        payload = {
            'apikey': self._api_key, 
            'symbol': symbol
        }
        response = requests.get(url=endpoint, params=payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    """------- STOCK FUNDAMENTAL ANALYSIS -------"""

    """------- INSTITUTIONAL STOCK OWNERSHIP -------"""

    """------- ESG SCORE -------"""

    """------- PRICE TARGET -------"""

    """------- UPGRADES & DOWNGRADES -------"""

    """------- HISTORICAL ETF AND MUTUAL FUND HOLDINGS -------"""

    """------- HISTORICAL NUMBER OF EMPLOYEES -------"""

    """------- EXECUTIVE COMPENSATION -------"""

    """------- INDIVIDUAL BENEFICIAL OWNERSHIP -------"""

    """------- STOCK CALENDARS -------"""

    """------- STOCK LOOK UP TOOL -------"""

    """------- COMPANY INFORMATION -------"""

    def company_profile(self, symbol, return_type):
        """General information about a company.
        
        Args:
            symbol (str): Stock ticker symbol.
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the company's profile information.
        """
        endpoint = r'{}/profile/{}'.format(BASE_URL_V3, symbol)
        response = requests.get(url=endpoint, params=self._empty_payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    def key_executives(self, symbol, return_type='json'):
        """Information about company executives.
        
        Args:
            symbol (str): Stock ticker symbol.
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the executive information.
        """
        endpoint = r'{}/key-executives/{}'.format(BASE_URL_V3, symbol)
        response = requests.get(url=endpoint, params=self._empty_payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    def market_capitalization(self, symbol, return_type='json'):
        """Gets the symbols market capitalization.
        
        Args:
            symbol (str): Stock ticker symbol.
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the market cap.
        """
        endpoint = r'{}/market-capitalization/{}'.format(BASE_URL_V3, symbol)
        response = requests.get(url=endpoint, params=self._empty_payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    def historical_market_capitalization(self, symbol, limit=None, return_type='json'):
        """Gets the history of the company's market capitalization.
        
        Args:
            symbol (str): Stock ticker symbol.
            limit (int): Number of days returned.
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the historicals capitalizations.
        """
        endpoint = r'{}/historical-market-capitalization/{}'.format(BASE_URL_V3, symbol)
        payload = {
            'apikey': self._api_key
        }
        if limit is not None:
            payload['limit'] = limit
        response = requests.get(url=endpoint, params=payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    def company_outlook(self, symbol):
        """Returns a variety of current metrics on the given company.
        
        Args:
            symbol (str): Stock ticker symbol.

        Returns: 
            A dict with the company's metrics.
        """
        endpoint = r'{}/company-outlook'.format(BASE_URL_V4)
        payload = {
            'apikey': self._api_key, 
            'symbol': symbol
        }
        response = requests.get(url=endpoint, params=payload)
        return self._convert_response(response, response_type='json', return_type='json')

    def stock_peers(self, symbol, return_type='json'):
        """Stock peers based on sector, exchange and market cap.
        
        Args:
            symbol (str): Stock ticker symbol.
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the stocks peers.
        """
        endpoint = r'{}/stock_peers'.format(BASE_URL_V4)
        payload = {
            'apikey': self._api_key, 
            'symbol': symbol
        }
        response = requests.get(url=endpoint, params=payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    def is_the_market_open(self):
        """Returns the hours that the market is open and which markets currently are.
        
        Returns: 
            A dict with information about the market hours.
        """
        endpoint = r'{}/is-the-market-open'.format(BASE_URL_V3)
        response = requests.get(url=endpoint, params=self._empty_payload)
        return self._convert_response(response, response_type='json', return_type='json')

    def company_core_information(self, symbol, return_type='json'):
        """Returns a company's core information.
        
        Args:
            symbol (str): Stock ticker symbol.
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the stocks peers.
        """
        endpoint = r'{}/company-core-information'.format(BASE_URL_V4)
        payload = {
            'apikey': self._api_key, 
            'symbol': symbol
        }
        response = requests.get(url=endpoint, params=payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    """------- STOCK NEWS -------"""

    """------- MARKET PERFORMANCE -------"""

    """------- ADVANCED DATA -------"""

    """------- STOCK STATISTICS -------"""

    """------- INSIDER TRADING -------"""

    """------- ECONOMICS -------"""

    """------- STOCK PRICE -------"""

    def quote(self, symbols, return_type='json'):
        """Gets the most recent price quote for one or more stock symbols.
        
        Args:
            symbols (str | str list): Stock ticker symbol or symbols.
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the stock quotes.
        """
        endpoint = r'{}/quote/{}'.format(BASE_URL_V3, self._merge_symbols_for_url(symbols))
        response = requests.get(url=endpoint, params=self._empty_payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    def otc_quote(self, symbols, return_type='json'):
        """Gets the most recent price quote for one or more OTC stock symbols.
        
        Args:
            symbols (str | str list): Stock ticker symbol or symbols.
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the stock quotes.
        """
        endpoint = r'{}/otc/real-time-price/{}'.format(BASE_URL_V3, self._merge_symbols_for_url(symbols))
        response = requests.get(url=endpoint, params=self._empty_payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    def historical_price_interval(self, symbol, start_date, end_date=TODAY, return_type='json'):
        """Gets the stocks daily history from start_date to end_date.
        
        Args:
            symbols (str | str list): Stock ticker symbol or symbols.
            start_date (str): Start date of the range.
            end_date (str): End date of the range.
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the stock history.
        """
        endpoint = r'{}/historical-price-full/{}'.format(BASE_URL_V3, symbol)
        payload = {
            'apikey': self._api_key, 
            'from': start_date, 
            'to': end_date
        }
        response = requests.get(url=endpoint, params=payload)
        historical_json = response.json()['historical']
        if (return_type == 'json'):
            return response.json()
        elif (return_type == 'df'):
            return pd.DataFrame(historical_json)

    def historical_price_full(self, symbol, return_type='json'):
        """Gets the full daily history for a symbol.
        
        Args:
            symbols (str | str list): Stock ticker symbol or symbols.
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the stock history.
        """
        return self.historical_price_interval(symbol, '1900-01-01', TODAY, return_type=return_type)

    """------- FUND HOLDINGS -------"""

    """------- WEBSOCKET -------"""

    """------- STOCK LIST -------"""

    def symbols_list(self, return_type='json'):
        """Returns a list of available symbols with their full names, exchanges, and prices.
        
        Args:
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the symbols list.
        """
        endpoint = r'{}/stock/list'.format(BASE_URL_V3)
        response = requests.get(url=endpoint, params=self._empty_payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    def tradable_symbols_list(self, return_type='json'):
        """Returns a list of tradable symbols.
        
        Args:
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the symbols list.
        """
        endpoint = r'{}/available-traded/list'.format(BASE_URL_V3)
        response = requests.get(url=endpoint, params=self._empty_payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    def etf_list(self, return_type='json'):
        """Returns a list of available etf's, a subset of the symbols list.
        
        Args:
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with the etf list.
        """
        endpoint = r'{}/etf/list'.format(BASE_URL_V3)
        response = requests.get(url=endpoint, params=self._empty_payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    """------- BULK AND BATCH -------"""

    def batch_quote_prices(self, symbols_list, return_type='json'):
        """Returns a list of prices for the given symbols.
        
        Args:
            return_type (str): 'json' | 'df'.

        Returns: 
            Either a list or pandas.DataFrame with quotes.
        """
        endpoint = r'{}/quote/{}'.format(BASE_URL_V3, self._merge_symbols_for_url(symbols_list))
        response = requests.get(url=endpoint, params=self._empty_payload)
        return self._convert_response(response, response_type='json', return_type=return_type)

    def batch_request_end_of_day_prices(self, date):
        """Returns a list of prices for the given symbols.
        
        Args:
            return_type (str): 'json' | 'df'.

        Returns: 
            A pandas.DataFrame with quotes.
        """
        endpoint = r'{}/batch-request-end-of-day-prices'.format(BASE_URL_V4)
        payload = {
            'apikey': self._api_key, 
            'date': date
        }
        response = requests.get(url=endpoint, params=self._empty_payload)
        return self._convert_response(response, response_type='csv', return_type='df')

    """------- MARKET INDEXES -------"""

    """------- EURONEXT -------"""

    """------- TSX -------"""

    """------- CRYPTO & FOREX & COMMODITIES -------"""
