import copy
import os
from datetime import datetime
from pathlib import Path
from threading import Thread
import re
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import json
from MyScanner import Scanner
from threading import Semaphore
from Flights.Utilities import General as general
from Data.DataManager import data_manager

sem = Semaphore(3)
req_result = 60


def get_data_of_location_hotel_in_dates(trip):
    '''
    :param trip: Trip object with Destination,Check-in and Check-out
    :return: create JSON file with the data of location hotels in dates
    '''
    try:

        driver = Scanner.prepare_driver_chrome('https://www.booking.com')

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ss')))
        fill_form_with_dates(driver, trip)
        accommodations_data = scrape_results(driver, req_result, trip)
        accommodations_data = {item['_name']: item for item in accommodations_data}  ## max need tp remove

        start_date_dt = datetime.strptime(trip.start_date, '%Y-%m-%d')
        Path(os.path.dirname(__file__) + '/../Data/Hotels/Order Data/' + datetime.strftime(start_date_dt,
                                                                                           "%Y-%m")).mkdir(
            parents=True,
            exist_ok=True)
        Path(os.path.dirname(__file__) + '/../Data/Hotels/Order Data/' + datetime.strftime(start_date_dt,
                                                                                           "%Y-%m") + '/' + trip.destination).mkdir(
            parents=True, exist_ok=True)
        my_file = Path(
            os.path.dirname(
                __file__) + '/../Data/Hotels/Order Data/{selected_month}/{location}/{start_date}_{end_date}.json'.format(
                selected_month=datetime.strftime(start_date_dt, "%Y-%m"), location=trip.destination,
                start_date=trip.start_date,
                end_date=trip.end_date))
        if my_file.is_file():
            with open(os.path.dirname(
                    __file__) + '/../Data/Hotels/Order Data/{selected_month}/{location}/{start_date}_{end_date}.json'.format(
                selected_month=datetime.strftime(start_date_dt, "%Y-%m"), location=trip.destination,
                start_date=trip.start_date,
                end_date=trip.end_date), 'r') as JSON:
                location_dict = json.load(JSON)
            accommodations_data.update(location_dict)
        accommodations_data = json.dumps(accommodations_data, indent=4)
        with open(os.path.dirname(
                __file__) + '/../Data/Hotels/Order Data/{selected_month}/{location}/{start_date}_{end_date}.json'.format(
            selected_month=datetime.strftime(start_date_dt, "%Y-%m"), location=trip.destination,
            start_date=trip.start_date,
            end_date=trip.end_date), 'w') as f:
            f.write(accommodations_data)
    finally:
        driver.quit()


def scrape_accommodation_data(driver, accommodation_url, trip, location_dict):
    """
    Visits an accommodation page and extracts the all the data(score,price,etc..).
    if the trip already in the data get all the info from the dataset and only get the price from site
    else get all the data from the site and also add him to the dataset without price
    :param accommodation_url:
    :param trip:
    :param location_dict:
    :return:
    :type driver: selenium.webdriver.Chrome
    """
    driver.get(accommodation_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'hp_hotel_name')))
    key = driver.find_element_by_id('hp_hotel_name') \
        .text.strip('trip')
    if key in location_dict:
        accommodation_fields = copy.deepcopy(location_dict[key])
    else:
        accommodation_fields = scrape_accommodation_data_without_price(driver, accommodation_url)
        location_dict[key] = accommodation_fields
        with open(os.path.dirname(__file__) + '/../Data/Hotels/Locations Data/{location}.json'.format(
                location=trip.destination), 'w') as f:
            f.write(json.dumps(location_dict, indent=4))
    return scrape_accommodation_data_only_price_and_update_dates(driver, accommodation_fields, trip)


def fill_form_with_dates(driver, trip):
    """
    Receives a search_argument to insert it in the search bar and
    then clicks the search button.(include dates)
    :param driver:
    :param trip:
    """
    search_field = driver.find_element_by_id('ss')
    search_field.send_keys(trip.destination)
    driver.find_element_by_class_name("sb-date-field__icon").click()
    while True:
        try:
            driver.find_element_by_xpath("//td[@data-date='{start_date}']".format(start_date=trip.start_date)).click()
            driver.find_element_by_xpath("//td[@data-date='{end_date}']".format(end_date=trip.end_date)).click()
            break;
        except:
            driver.find_element_by_class_name("bui-calendar__control--next").click()
    driver.find_element_by_class_name('sb-searchbox__button').click()  # We look for the search button and click it
    wait = WebDriverWait(driver, timeout=10).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, 'sr-hotel__title')))  # wait until the elements with the class name
    # sr-trip-title (the one containing the accommodations titles) appear.


def scrape_results(driver, n_results, trip):
    """
    Returns the data from n_results amount of results.
    :param driver:
    :param n_results:
    :param trip:
    :return:
    """
    accommodations_urls = get_all_hotel_links_per_driver(driver, n_results)
    accommodations_data = list()
    with open(os.path.dirname(__file__) + '/../Data/Hotels/Locations Data/{location}.json'.format(
            location=trip.destination), 'r') as JSON:
        location_dict = json.load(JSON)
    my_range = list(range(0, len(accommodations_urls)))
    for url in my_range:
        url_data, can_order = scrape_accommodation_data(driver, accommodations_urls[url], trip, location_dict)
        accommodations_data.append(url_data)
    return accommodations_data


def scrape_accommodation_data_only_price_and_update_dates(driver, accommodation_fields, trip):
    """
    Visits an accommodation page and extracts the price only , also update the dates for this price.
    :param driver:
    :param accommodation_fields:
    :param trip:
    :return:
    """
    accommodation_fields['_city'] = trip.destination
    accommodation_fields['_check_in'] = trip.start_date
    accommodation_fields['_check_out'] = trip.end_date
    # driver.execute_script("window.scrollTo(0, 2000)")
    try:
        temp_price = driver.find_element_by_class_name('bui-price-display__value').text
        can_order = True
    except Exception:
        try:
            temp = driver.current_url.replace('.html', '.en-gb.html') + data_manager.Booking_order_address.format(
                start_date=trip.start_date, end_date=trip.end_date)
            headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.149 Safari/537.36'}
            request = requests.get(url=temp, headers=headers)
            m = re.search(r'"b_price":"₪\s*([^\n$"]+)', request.text)
            temp_price = int(m.group(1).replace(',', ''))
            can_order = True
        except Exception:
            temp_price = 'no available'
            can_order = False
    accommodation_fields['_fetch_date'] = datetime.today().strftime('%Y-%m-%d')
    accommodation_fields['_price'] = temp_price
    return accommodation_fields, can_order


def fill_form_without_dates(driver, location_name):
    """
    Receives a search_argument to insert it in the search bar and
    then clicks the search button.(without dates)
    :param driver:
    :param location_name:
    """
    search_field = driver.find_element_by_id('ss')
    search_field.send_keys(location_name)
    driver.find_element_by_class_name('sb-searchbox__button').click()  # We look for the search button and click it
    WebDriverWait(driver, timeout=10).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, 'sr-hotel__title')))  # wait until the elements with the class name
    # sr-trip-title (the one containing the accommodations titles) appear.


def scrape_results_without_price(driver):
    """
    return all the hotels in dest
    :param driver:
    :return:
    """
    accommodations_urls = get_all_hotel_links_per_driver(driver)
    accommodations_data = list()
    for url in range(0, len(accommodations_urls)):
        url_data = scrape_accommodation_data_without_price(driver, accommodations_urls[url])
        accommodations_data.append(url_data)
    return accommodations_data


def scrape_accommodation_data_without_price(driver, accommodation_url):
    """
    Visits an accommodation page and extracts the data without price.
    :param driver:
    :param accommodation_url:
    :return:
    """
    if driver == None:
        driver = Scanner.prepare_driver(accommodation_url)
    print(accommodation_url)
    driver.get(accommodation_url)
    accommodation_fields = dict()
    # Get the accommodation name
    accommodation_fields['_name'] = driver.find_element_by_id('hp_hotel_name') \
        .text.strip('trip')
    # Get the accommodation score
    try:
        accommodation_fields['_score'] = driver.find_element_by_class_name(
            'bui-review-score--end').find_element_by_class_name(
            'bui-review-score__badge').text
        try:
            all_box_grades = driver.find_element_by_class_name('v2_review-scores__body').find_elements_by_tag_name("li")
            driver.find_element_by_class_name('bui-review-score__title').click()
            for box_grade in all_box_grades:
                temp_title_score = box_grade.find_element_by_class_name('c-score-bar__title').text
                temp_grade_score = box_grade.find_element_by_class_name('c-score-bar__score').text
                accommodation_fields["_" + temp_title_score.lower().rstrip().replace(" ", "_")] = temp_grade_score
        except:
            accommodation_fields['_location'] = '0'
    except:
        accommodation_fields['_score'] = 'not enough reviews'
    # Get the accommodation location
    accommodation_fields['_address'] = driver.find_element_by_id('showMap2') \
        .find_element_by_class_name('hp_address_subtitle').text
    # Get the most popular facilities
    try:
        accommodation_fields['_popular_facilities'] = list()
        facilities = driver.find_element_by_class_name('hp_desc_important_facilities')
        for facility in facilities.find_elements_by_class_name('important_facility'):
            accommodation_fields['_popular_facilities'].append(facility.text)
    except Exception:
        accommodation_fields['_popular_facilities'].append('unknown')
    accommodation_fields['_link'] = accommodation_url
    return accommodation_fields


def get_all_hotel_links_per_driver(driver, n=None):
    """
    return list of all the links of hotels in location,need to be already after searching the dest
    :param driver:
    :param n:
    :return:
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
        for accomodation_title in driver.find_elements_by_class_name('sr-hotel__title'):
            accommodations_urls.append(accomodation_title.find_element_by_class_name(
                'hotel_name_link').get_attribute('href'))
        driver.get(page_list[page + 1])
    accommodations_urls = list(dict.fromkeys(accommodations_urls))
    return accommodations_urls


def update_data_hotels(st='all'):
    """
    :param st:The full name of destination to update,the default is to update all
    :return:create data of hotels in location , if choose all - update all the destinations else update the req one
    """
    if st == 'all':
        airports_list = general.get_list_of_all_destinations()
        destinations = {airport.city for airport in airports_list}
        for location in destinations:
            sem.acquire()
            thread = Thread(target=update_data_per_location_hotels_without_dates, args=(location, sem))
            thread.start()
        thread.join()
    else:
        update_data_per_location_hotels_without_dates(st)


def update_data_per_location_hotels_without_dates(location_name, sem=None):
    """
    create JSON file with all the hotels of choosen location
    :param location_name:
    :param sem:
    """
    try:
        driver = Scanner.prepare_driver('https://www.booking.com')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ss')))
        fill_form_without_dates(driver, location_name)
        accommodations_data = scrape_results_without_price(driver)
        accommodations_data = {item['_name']: item for item in accommodations_data}  ## max need tp remove
        with open(os.path.dirname(__file__) + '/../Data/Hotels/Locations Data/{location}.json'.format(
                location=location_name), 'w', encoding="utf-8") as f:
            json.dump(accommodations_data, f, indent=4)

    except Exception as e:
        print(e.with_traceback())
    finally:
        if sem is not None:
            sem.release()
        driver.quit()
