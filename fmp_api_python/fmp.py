"""Financial Modeling Prep API Wrapper.

An API key may be obtained here: https://site.financialmodelingprep.com/.
"""


import requests
import os
import csv
import json
import pandas as pd

from constants import BASE_URL_V3, BASE_URL_V4


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
                return pd.DataFrame(list(content))
            elif (return_type == 'json'):
                raise Exception('API returned csv format, unable to convert to JSON')

    """------- STOCK FUNDAMENTALS -------"""

    def financial_statement_symbol_lists(self, return_type='json'):
        """List of symbols that have financial statements.
        
        Args:
            return_type (str): 'json' | 'df' depending on the desired return format.

        Returns: 
            Either a list or pandas.DataFrame with the response content.
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
            Either a list or pandas.DataFrame with the response content.
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

    '''
    symbol - stock ticker symbol
    period - quarter | annual
    limit - # limit on statements returned
    '''
    def balance_sheet_statement(self, symbol, period='annual', limit=None):
        endpoint = r'{}/balance-sheet-statement/{}'.format(BASE_URL_V3, symbol)
        payload = {
            'apikey': self._api_key, 
            'period': period
        }
        if limit is not None:
            payload['limit'] = limit
        response = requests.get(url=endpoint, params=payload)
        return self._convert_response(response, response_type='json')

    '''
    symbol - stock ticker symbol
    period - quarter | annual
    limit - # limit on statements returned
    '''
    def cash_flow_statement(self, symbol, period='annual', limit=None):
        endpoint = r'{}/cash-flow-statement/{}'.format(BASE_URL_V3, symbol)
        payload = {
            'apikey': self._api_key, 
            'period': period
        }
        if limit is not None:
            payload['limit'] = limit
        response = requests.get(url=endpoint, params=payload)
        return self._convert_response(response, response_type='json')

    '''
    symbol - stock ticker symbol
    '''
    def financial_report_dates(self, symbol):
        endpoint = r'{}/financial-reports-dates'.format(BASE_URL_V4)
        payload = {
            'apikey': self._api_key, 
            'symbol': symbol
        }
        response = requests.get(url=endpoint, params=payload)
        return self._convert_response(response, response_type='json')

    '''
    STOCK FUNDAMENTAL ANALYSIS
    '''

    '''
    INSTITUTIONAL STOCK OWNERSHIP
    '''

    '''
    ESG SCORE
    '''

    '''
    PRICE TARGET
    '''

    '''
    UPGRADES & DOWNGRADES
    '''

    '''
    HISTORICAL ETF AND MUTUAL FUND HOLDINGS
    '''

    '''
    HISTORICAL NUMBER OF EMPLOYEES
    '''

    '''
    EXECUTIVE COMPENSATION
    '''

    '''
    INDIVIDUAL BENEFICIAL OWNERSHIP
    '''

    '''
    STOCK CALENDARS
    '''

    '''
    STOCK LOOK UP TOOL
    '''

    '''
    COMPANY INFORMATION
    '''

    def company_profile(self, symbol):
        endpoint = r'{}/profile/{}'.format(BASE_URL_V3, symbol)
        response = requests.get(url=endpoint, params=self._empty_payload)
        return self._convert_response(response, response_type='json')

    def market_capitalization(self, symbol):
        endpoint = r'{}/market-capitalization/{}'.format(BASE_URL_V3, symbol)
        response = requests.get(url=endpoint, params=self._empty_payload)
        return self._convert_response(response, response_type='json')

    def historical_market_capitalization(self, symbol, limit=None):
        endpoint = r'{}/historical-market-capitalization/{}'.format(BASE_URL_V3, symbol)
        payload = {
            'apikey': self._api_key
        }
        if limit is not None:
            payload['limit'] = limit
        response = requests.get(url=endpoint, params=payload)
        return self._convert_response(response, response_type='json')

    def stock_peers(self, symbol):
        endpoint = r'{}/stock_peers'.format(BASE_URL_V4)
        payload = {
            'apikey': self._api_key, 
            'symbol': symbol
        }
        response = requests.get(url=endpoint, params=payload)
        return self._convert_response(response, response_type='json')

    def is_the_market_open(self):
        endpoint = r'{}/is-the-market-open'.format(BASE_URL_V3)
        response = requests.get(url=endpoint, params=self._empty_payload)
        print(response.json())
        return self._convert_response(response, response_type='json')

    def company_core_information(self, symbol):
        endpoint = r'{}/company-core-information'.format(BASE_URL_V4)
        payload = {
            'apikey': self._api_key, 
            'symbol': symbol
        }
        return requests.get(url=endpoint, params=payload).json()

    '''
    STOCK NEWS
    '''

    '''
    MARKET PERFORMANCE
    '''

    '''
    ADVANCED DATA
    '''

    '''
    STOCK STATISTICS
    '''

    '''
    INSIDER TRADING
    '''

    '''
    ECONOMICS
    '''

    '''
    STOCK PRICE
    '''

    def historical_price_full(self, symbol):
        endpoint = r'{}/historical-price-full/{}'.format(BASE_URL_V3, symbol)
        return requests.get(url=endpoint, params=self._empty_payload).json()

    '''
    FUND HOLDINGS
    '''

    '''
    WEBSOCKET
    '''

    '''
    STOCK LIST
    '''

    def symbols_list(self):
        endpoint = r'{}/stock/list'.format(BASE_URL_V3)
        return requests.get(url=endpoint, params=self._empty_payload).json()

    def tradable_symbols_list(self):
        endpoint = r'{}/available-traded/list'.format(BASE_URL_V3)
        return requests.get(url=endpoint, params=self._empty_payload).json()

    def etf_list(self):
        endpoint = r'{}/etf/list'.format(BASE_URL_V3)
        return requests.get(url=endpoint, params=self._empty_payload).json()



    '''
    BULK AND BATCH
    '''

    def batch_quote_prices(self, symbols_list):
        endpoint = r'{}/quote/'.format(BASE_URL_V3)
        for symbol in symbols_list:
            endpoint = endpoint + symbol + ','
        return requests.get(url=endpoint, params=self._empty_payload).json()

    def batch_request_end_of_day_prices(self, date):
        endpoint = r'{}/batch-request-end-of-day-prices'.format(BASE_URL_V4)
        payload = {
            'apikey': self._api_key, 
            'date': date
        }
        return requests.get(url=endpoint, params=payload)

    '''
    MARKET INDEXES
    '''

    '''
    EURONEXT
    '''

    '''
    TSX
    '''

    '''
    CRYPTO & FOREX & COMMODITIES
    '''