import json
import os
from datetime import datetime
from threading import Semaphore, Thread
from Hotel import Hotel
from Entity.Trip import Trip
from enum import Enum
import traceback
import platform
import selenium
from selenium.webdriver import Chrome, DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import booking_requests
import booking_automation
from Flights.Utilities import general as flight_general

class ByTechnique(Enum):
    selenium = 1
    requests = 2


def get_data_by_name(trip, fetch_date=datetime.today().strftime('%Y-%m-%d')):
    """
    get hotels list for the required flight in trip
    :param trip:The required flight that need find hotel list
    :type fetch_date: str
    :param fetch_date: date of fetch from booking
    :type trip: Trip
    :rtype: list(Hotels)
    :return: list of hotels in asked date and flight
    """
    start_date_dt = datetime.strptime(trip.start_date, '%Y-%m-%d')
    with open(os.path.dirname(__file__) + '/../Data/Hotels/Order Data/'
                                          '{selected_month}/{location}/{start_date}_{end_date}.json'.format(
        selected_month=datetime.strftime(start_date_dt, "%Y-%m"), location=trip.destination,
        start_date=trip.start_date, end_date=trip.end_date), 'r') as f:
        hotels_data = json.load(f)
    hotels = []
    for hotel_key, hotel_val in hotels_data.items():
        if hotels_data[hotel_key]['_fetch_date'] == fetch_date:
            hotels.append(Hotel(**hotels_data[hotel_key]))
    return hotels


def filter_by_location(hotels_data, score):
    """
    filter the list by location's score
    :param hotels_data: list of hotels that need to filter
    :type hotels_data: list(Hotels)
    :param score: the minimum location's score of new list
    :type score: int
    """
    hotels_data = [hotel for hotel in hotels_data if float(hotel.location) >= score]


def filter_by_score(hotels_data, score):
    """
    filter the list by general score
    :param hotels_data: list of hotels that need to filter
    :type hotels_data: list(Hotels)
    :param score: the minimum general score of new list
    :type score: int
    """
    hotels_data = [hotel for hotel in hotels_data if float(hotel.score) >= score]


def prepare_driver_chrome(url):
    """
    lunch selenium chrome driver in headless mode of input url
    :param url:the url for browsing
    :type url str
    :return:chrome driver with open
    :rtype:selenium.webdriver.chrome.webdriver.WebDriver
    """
    options = Options()
    options.add_argument('-headless')
    options.add_argument("--lang=en-gb");
    options.add_argument('window-size=1920x1080')
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "normal"
    if platform.system() == 'Windows':
        driver = selenium.webdriver.Chrome(
            executable_path='C:\\Users\\Ziv\\PycharmProjects\\TravelScanner\\chromedriver.exe', options=options,
            desired_capabilities=caps)
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


def update_data_hotels(destination='all',by_technique=ByTechnique.selenium):
    """
    create json with data of hotels in location at Data/Hotel/Location/{destination}.json,
    if chose all(by default)- update all the destinations else update the required one.
    :param destination:The full name of destination to update,the default is to update all
    :type destination: str
    :param by_technique:
    :type by_technique: ByTechnique
    """
    sem = Semaphore(3)
    if by_technique == ByTechnique.selenium:
        fetch_technique_function = booking_automation.update_data_per_location_hotels_without_dates
    else:
        fetch_technique_function = booking_requests.update_data_per_location_hotels_without_dates
    if destination == 'all':
        airports_list = flight_general.get_list_of_all_destinations()
        destinations = {airport.city for airport in airports_list}
        for location in destinations:
            sem.acquire()
            thread = Thread(target=fetch_technique_function, args=(location, sem))
            thread.start()
        thread.join()
    else:
        fetch_technique_function(destination)