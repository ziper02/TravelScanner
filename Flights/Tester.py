from datetime import date
from decimal import Decimal
from time import strptime

import requests
from forex_python.converter import CurrencyRates

from DataManager import data_manager
from Entity.Airport import Airport
from Utilities import SkyScanner as ss
from Utilities import EasyJet as ej

ej.export_whole_months_all_dest()
#ss.export_whole_month_all_dest()

