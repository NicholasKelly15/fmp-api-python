from time import perf_counter

from pandas import json_normalize
import pandas as pd
from fmp import FMPClient

import json
import csv

import requests



client = FMPClient()

# response = client.historical_price_interval('AAPL', start_date='2020-01-01', return_type='df')
response = client.historical_price_full('AAPL', 'df')

print(response)
print(type(response))
