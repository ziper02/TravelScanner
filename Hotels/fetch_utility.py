import os
from datetime import datetime
from pathlib import Path
from enum import Enum
from Trip import Trip
import traceback
import platform
import selenium
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import booking_automation
import booking_requests
import json


class ByTechnique(Enum):
    selenium = 1
    requests = 2


def save_hotels_order_data_to_json(accommodations_data, trip):
    """
    create JSON file with the order data of location hotels in dates
    at: /Order Data/{MM-YYYY of Check-in}/{Destination}/{Check-in}_{Check-out}.json
    :param accommodations_data:
    :type accommodations_data: dict
    :param trip:Trip object with Destination,Check-in and Check-out
    :type trip: Trip
    """
    start_date_dt = datetime.strptime(trip.start_date, '%Y-%m-%d')  # write the data to json files
    Path(os.path.dirname(__file__) + '/../Data/Hotels/Order Data/' + datetime.strftime(start_date_dt,
                                                                                       "%Y-%m")).mkdir(
        parents=True,
        exist_ok=True)
    Path(os.path.dirname(__file__) + '/../Data/Hotels/Order Data/' + datetime.strftime(
        start_date_dt, "%Y-%m") + '/' + trip.destination).mkdir(parents=True, exist_ok=True)
    my_file = Path(
        os.path.dirname(
            __file__) + '/../Data/Hotels/Order Data/{selected_month}/{location}/{start_date}_{end_date}.json'.format(
            selected_month=datetime.strftime(start_date_dt, "%Y-%m"), location=trip.destination,
            start_date=trip.start_date,
            end_date=trip.end_date))
    if my_file.is_file():
        with open(os.path.dirname(
                __file__) + '/../Data/Hotels/Order Data/{selected_month}/{location}/{start_date}_{end_date}.json'.format
                      (selected_month=datetime.strftime(start_date_dt, "%Y-%m"), location=trip.destination,
                       start_date=trip.start_date, end_date=trip.end_date), 'r') as JSON:
            location_dict = json.load(JSON)
        accommodations_data.update(location_dict)
    accommodations_data = json.dumps(accommodations_data, indent=4)
    with open(os.path.dirname(
            __file__) + '/../Data/Hotels/Order Data/{selected_month}/{location}/{start_date}_{end_date}.json'.format(
            selected_month=datetime.strftime(start_date_dt, "%Y-%m"), location=trip.destination,
            start_date=trip.start_date, end_date=trip.end_date), 'w') as f:
        f.write(accommodations_data)


def get_hotel_data(page, key, location_dict, by_technique=ByTechnique.selenium):
    """
    get the hotel data, if the data exist in data folder , just return the exist
    information , if not fetch from booking.com,save it and return the information
    :param page: if technique is selenium then the its the driver of hotelpage
    else the technique is requests and then its the html page of hotel
    :type page: if technique is selenium selenium.webdriver.chrome.webdriver.WebDriver
                else str
    :param key:full hotel name
    :type key: str
    :param location_dict:data of all hotels that exist in data folder
    :type location_dict: dict
    :param by_technique:fetch data if hotel not found in data folder
    :type by_technique: ByTechnique
    :return: hotel data
    :rtype: dict
    """
    if key in location_dict:  # if the hotel data exist in our data folder,loading the data from data
        accommodation_fields = copy.deepcopy(location_dict[key])
    else:  # if not exist in our data fetch the data from booking and save him to data folder
        if by_technique == ByTechnique.selenium:
            accommodation_fields = booking_automation.scrape_accommodation_data_without_price(
                driver=page, accommodation_url=accommodation_url, need_fetch=False)
        else:
            accommodation_fields = booking_requests.scrape_accommodation_data_without_price(
                page=page, accommodation_url=accommodation_url, need_fetch=False)
        if accommodation_fields is not None:
            location_dict[key] = accommodation_fields
            with open(os.path.dirname(__file__) + '/../Data/Hotels/Locations Data/{location}.json'.format(
                    location=trip.destination), 'w') as f:
                json.dump(location_dict, f, indent=4)
        else:
            return None
    return accommodation_fields


def fetch_data_for_trip(driver, n_results, trip, by_technique=ByTechnique.selenium):
    """
    Fetch data including price from Booking.com of Trip.destination between between two dates
    (trip.start_date until trip.end_date)
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver
    :param n_results: how much hotel to scrape
    :type n_results: int
    :param trip:the destination with check-in and check-out
    :type trip: Trip
    :param by_technique: which technique use for fetch data selenium/get
    :type: ByTechnique
    :return: dict{"hotel_name":data} of hotels with all the the data that required
    :rtype: dict
    """
    accommodations_urls = fetch_utility.get_all_hotel_links_per_driver(driver, n_results)
    accommodations_data = list()
    with open(os.path.dirname(__file__) + '/../Data/Hotels/Locations Data/{location}.json'.format(
            location=trip.destination), 'r') as JSON:
        location_dict = json.load(JSON)
    my_range = list(range(0, len(accommodations_urls)))
    for url in my_range:
        if by_technique == ByTechnique.selenium:
            url_data, can_order = booking_automation.scrape_accommodation_data(driver, accommodations_urls[url], trip,
                                                                               location_dict)
        else:
            url_data, can_order = booking_requests.scrape_accommodation_data(accommodations_urls[url], trip,
                                                                             location_dict)
        if url_data is not None:
            accommodations_data.append(url_data)
    return accommodations_data


def get_all_hotel_links_per_driver(driver, n=None):
    """
    get list of currently available links of hotels in location,
    the driver suppose to be already after searching the dest
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver
    :param n:the required amount of hotels
    :type n: int
    :return: list of currently available url's of hotels in location
    :rtype: list(str)
    """
    page_list = list()
    accommodations_urls = list()
    for page in driver.find_elements_by_class_name('bui-pagination__link'):
        page_list.append(page.get_attribute('href'))
    if not n:
        if len(page_list) > 7:
            my_range = range(0, len(page_list) - 3)
        else:
            my_range = range(0, len(page_list) - 1)
    else:
        my_range = range(0, int(n / 15) + 2)
    for page in my_range:
        for accommodation_title in driver.find_elements_by_class_name('sr-hotel__title'):
            accommodations_urls.append(accommodation_title.find_element_by_class_name(
                'hotel_name_link').get_attribute('href'))
        driver.get(page_list[page + 1])
    accommodations_urls = list(dict.fromkeys(accommodations_urls))
    return accommodations_urls


def update_data_per_location_hotels_without_dates(location_name, sem=None, by_technique=ByTechnique.selenium):
    """
    create json with data of hotels in location atData/Hotel/Location/{destination}.json
    for the required one, using automation for fetch all data.
    :param location_name:The full name of destination to update
    :type location_name: str
    :param sem: semaphore for multithreading fetch
    :type sem: threading.Semaphore
    :param by_technique: which technique use for fetch data selenium/get
    :type: ByTechnique
    """
    driver = None
    try:
        driver = prepare_driver_chrome('https://www.booking.com')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ss')))
        try:
            fill_form_without_dates(driver, location_name)
        except Exception:
            print(f'{location_name} accommodations titles not appeared at fill form function')
        accommodations_urls = get_all_hotel_links_per_driver(driver)
        try:
            with open(os.path.dirname(__file__) + '/../Data/Hotels/Locations Data/{location}.json'.format(
                    # store the old data
                    location=location_name), 'r', encoding="utf-8") as f:
                save_accommodations_data = json.load(f)
        except Exception:
            save_accommodations_data = dict()
        new_accommodations_data = []
        for url in range(0, len(accommodations_urls)):
            if by_technique == ByTechnique.selenium:
                url_data = booking_automation.scrape_accommodation_data_without_price(driver, accommodations_urls[url],
                                                                                      need_fetch=True)
            else:
                url_data = booking_requests.scrape_accommodation_data_without_price(
                    accommodation_url=accommodations_urls[url],
                    need_fetch=True)
            if url_data is not None:
                new_accommodations_data.append(url_data)
        try:
            new_accommodations_data = {item['name']: item for item in new_accommodations_data if
                                       'name' in item.keys()}
        except Exception:
            print("ERROR new_accommodations_data in update_data_per_location_hotels_without_dates")
            return
        for key_old in save_accommodations_data.keys():  # merge the old data with new data
            if key_old not in new_accommodations_data.keys():
                new_accommodations_data[key_old] = save_accommodations_data[key_old]
        with open(os.path.dirname(__file__) + '/../Data/Hotels/Locations Data/{location}.json'.format(
                location=location_name), 'w', encoding="utf-8") as f:
            json.dump(new_accommodations_data, f, indent=4)
    except Exception as e:
        print(e.with_traceback())
    finally:
        if sem is not None:
            sem.release()
        if driver:
            driver.quit()


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
    options.add_argument("--lang=en-gb")
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


def fill_form_with_dates(driver, trip):
    """
    Receives a Trip with destination and checkin and checkout to insert
    it in the search bar and then clicks the search button.
    :rtype: object
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver
    :param trip:the destination with check-in and check-out
    :type trip: Trip
    """
    search_field = driver.find_element_by_id('ss')
    search_field.send_keys(trip.destination)
    driver.find_element_by_class_name("sb-date-field__icon").click()
    while True:
        try:
            driver.find_element_by_xpath("//td[@data-date='{start_date}']".format(start_date=trip.start_date)).click()
            driver.find_element_by_xpath("//td[@data-date='{end_date}']".format(end_date=trip.end_date)).click()
            break
        except Exception:
            driver.find_element_by_class_name("bui-calendar__control--next").click()
    driver.find_element_by_class_name('sb-searchbox__button').click()  # We look for the search button and click it
    WebDriverWait(driver, timeout=10).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, 'sr-hotel__title')))  # wait until the elements with the class name
    # sr-trip-title (the one containing the accommodations titles) appear.


def fill_form_without_dates(driver, location_name):
    """
    Receives a city name to insert it in the search bar and
    then clicks the search button.(without dates)
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver
    :param location_name: The name of destination
    :type location_name: str
    """
    search_field = driver.find_element_by_id('ss')
    search_field.send_keys(location_name)
    driver.find_element_by_class_name('sb-searchbox__button').click()  # We look for the search button and click it
    try:
        wait = WebDriverWait(driver, timeout=25).until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'sr-hotel__title')))  # wait until the elements with the class name
        # sr-trip-title (the one containing the accommodations titles) appear.
    except Exception:
        raise Exception("accommodations titles not appeared")
