# For data manipulation
import pandas as pd
from fredapi import Fred
import json
from pathlib import Path
import os
import quandl

# # To extract fundamental data
# from bs4 import BeautifulSoup as bs
# import requests

# auth
basepath = Path(__file__).parent.parent

with open(str(basepath)+'/keys/keys.json', 'r') as key_file:
    keys = json.load(key_file)

fred = Fred(api_key=keys['fred'])
quandl.ApiConfig.api_key = keys['quandl']


def fundamental_metric(soup, metric):
    return soup.find(text = metric).find_next(class_='snapshot-td2').text

def get_fundamental_data(df):
    for symbol in df.index:
        try:
            url = ("http://finviz.com/quote.ashx?t=" + symbol.lower())
            soup = bs(requests.get(url).content) 
            for m in df.columns:                
                df.loc[symbol,m] = fundamental_metric(soup,m)                
        except Exception as e:
            print (symbol, 'not found')
    return df

def convert_date_format(d, format):
    """"
    input format for date should be 'YYYY-MM-DD'
    """
    y, m, d = d.split('-')

    if format == 'MDY':
        return m+'/'+d+'/'+y
    elif format == 'YMD':
        return y+'-'+m+'-'+d

def fred_quandl(indx, start_date, end_date):
    """
    indx
    start_date, end_date: 'YYYY-MM-DD'
    """
    df = quandl.get('FRED/'+indx, start_date=start_date, end_date=end_date)
    df = df.reset_index()
    df.columns = ['Date', indx]
    return df

def fred_fred(code, column_name='v', observation_start=None, observation_end=None):
    """
    date: 'MM/DD/YYY'
    """
    df = fred.get_series(code, observation_start=observation_start, observation_end=observation_end)
    df = pd.DataFrame(df).reset_index()
    df.columns = ['date', column_name]
    return df