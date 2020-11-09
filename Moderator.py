import platform
from enum import Enum

if platform.system() == 'Windows':
    add_for_folders = ''
else:
    add_for_folders = '/home/ubuntu/TravelScanner/'

destination_list_skyscanner = ["LOND", "PRAG", "BERL", "MUC", "ZRH", "BCN", "MAD", "AMS", "MAN",
                    "BUD", "GVA", "PARI", "BOJ", "VAR", "MILA", "SOF", "SKG", "DUB", "LIS", "BELI","MLA"]
destination_list_easyjet = ["AMS", "BSL", "SXF", "TXL", "BOD", "GVA", "LTN", "LYS", "MAN",
                    "MXP", "NTE", "NAP", "NCE", "CDG", "TLS", "VCE"]
destination_list_wizzair = ["VAR","SOF","VIE","BUD","DEB","RIX","VNO","KTW","KRK","WAW","OTP","CLJ","IAS","SBZ","TSR","LTN"]

##temp need to be removed
destination_booking = ['Berlin', 'London', 'Prague', 'Rome', 'Amsterdam', 'Belgrade', 'Milano', 'Madrid', 'Barcelona',
                'Burgas', 'Sofia', 'Paris', 'Varna', 'Budapest', 'Bucharest', 'Thessaloniki', 'Kishinev']

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
