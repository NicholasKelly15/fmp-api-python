from time import perf_counter
from urllib import response

from pandas import json_normalize
import pandas as pd
from fmp import FMPClient

import json
import csv

import requests



client = FMPClient()

# response = client.batch_request_end_of_day_prices('2020-01-01')
response = client.historical_price_full('AAPL', return_type='df')

print(response)
print(type(response))
