import json
import os
from datetime import datetime

from Hotel import Hotel
from Entity.Trip import Trip
from enum import Enum
import traceback
import platform
import selenium
from selenium.webdriver import Chrome, DesiredCapabilities
from selenium.webdriver.chrome.options import Options



class ByTechnique(Enum):
    selenium = 1
    requests = 2




def get_data_by_name(trip: Trip, fetch_date: str = datetime.today().strftime('%Y-%m-%d')):
    """
    :rtype: list(Hotels)
    """
    start_date_dt = datetime.strptime(trip.start_date, '%Y-%m-%d')
    with open(os.path.dirname(__file__) + '/../Data/Hotels/Order Data/'
                                          '{selected_month}/{location}/{start_date}_{end_date}.json'.format(
        selected_month=datetime.strftime(start_date_dt, "%Y-%m"), location=trip.destination,
        start_date=trip.start_date, end_date=trip.end_date), 'r') as f:
        hotels_data = json.load(f)
    hotels: list[Hotel] = []
    for hotel_key, hotel_val in hotels_data.items():
        if hotels_data[hotel_key]['_fetch_date'] == fetch_date:
            hotels.append(Hotel(**hotels_data[hotel_key]))
    return hotels


def filter_by_location(hotels_data, score: int):
    """
    :rtype: list(Hotels)
    :type hotels_data: list(Hotels)
    """
    hotels_data = [hotel for hotel in hotels_data if float(hotel.location) >= score]


def filter_by_score(hotels_data, score: int):
    """
    :rtype: list(Hotels)
    :type hotels_data: list(Hotels)
    """
    hotels_data = [hotel for hotel in hotels_data if float(hotel.score) >= score]



'''Returns a Chrome Webdriver.'''

def prepare_driver_chrome(url,prof=None):
    options = Options()
    options.add_argument('-headless')
    options.add_argument("--lang=en-gb");
    options.add_argument('window-size=1920x1080')
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"
    if platform.system()=='Windows':
        driver = selenium.webdriver.Chrome(executable_path='C:\\Users\\Ziv\\PycharmProjects\\TravelScanner\\chromedriver.exe', options=options,desired_capabilities=caps)
    else:
        driver = selenium.webdriver.Chrome(
            executable_path='/usr/bin/chromedriver', options=options,
            desired_capabilities=caps)
    try:
        driver.get(url)
    except Exception:
        traceback.print_exc()
    driver.implicitly_wait(0)
    return driver


# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
#
#
# def prepare_driver_firefox(url):
#     options = Options()
#     options.headless = True
#     if platform.system() == 'Windows':
#         driver = webdriver.Firefox(options=options, executable_path=r'C:\\Users\\Ziv\\PycharmProjects\\TravelScanner\\geckodriver.exe')
#     try:
#         driver.get(url)
#     except Exception:
#         traceback.print_exc()
#     driver.implicitly_wait(0)
#     return driver
