from time import perf_counter

from pandas import json_normalize
import pandas as pd
from fmp import FMPClient

import json
import csv

import requests



client = FMPClient()

response = client.income_statement(symbol='AAPL', return_type='json')
print(response)
print(type(response))
