import platform
from enum import Enum

import requests

import DataManager

if platform.system() == 'Windows':
    add_for_folders = ''
else:
    add_for_folders = '/home/ubuntu/TravelScanner/'

destination_list_skyscanner = ["LOND", "PRAG", "BERL", "MUC", "ZRH", "BCN", "MAD", "AMS", "MAN",
                    "BUD", "GVA", "PARI", "BOJ", "VAR", "MILA", "SOF", "SKG", "DUB", "LIS", "BELI"]

destination_list_easyjet = ["AMS", "BSL", "SXF", "TXL", "BOD", "GVA", "LTN", "LYS", "MAN",
                    "MXP", "NTE", "NAP", "NCE", "CDG", "TLS", "VCE"]
depart_list = ["TLV"]


def transfer_airport_cod_names_to_all(short_name):
    m={
        'SXF':'BERL',
        'TXL':'BERL',
        'LTN': 'LOND',
        'CDG': 'PARI'
    }
    if short_name in m:
        return m[short_name]
    else:
        return short_name





def month_string_to_number(string):
    m = {
        'jan': "01",
        'feb': "02",
        'mar': "03",
        'apr':"04",
         'may':"05",
         'jun':"06",
         'jul':"07",
         'aug':"08",
         'sep':"09",
         'oct':"10",
         'nov':"11",
         'dec':"12"
        }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

class set(Enum):
    train = 1
    validation = 2
    test = 3


def RealTimeCurrencyExchangeRate(from_currency, to_currency):
    base_url = r"https://www.alphavantage.co/query?function = CURRENCY_EXCHANGE_RATE"
    api_key=DataManager.data_manager.currency_exchange_api_key
    main_url = base_url + "&from_currency =" + from_currency + "&to_currency =" + to_currency + "&apikey =" + api_key
    req_ob = requests.get(main_url)
    result = req_ob.json()
    print("\n After parsing : \n Realtime Currency Exchange Rate for",
          result["Realtime Currency Exchange Rate"]
          ["2. From_Currency Name"], "TO",
          result["Realtime Currency Exchange Rate"]
          ["4. To_Currency Name"], "is",
          result["Realtime Currency Exchange Rate"]
          ['5. Exchange Rate'], to_currency)

