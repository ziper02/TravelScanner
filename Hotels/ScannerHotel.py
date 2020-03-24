import copy
import os
from pathlib import Path
from threading import Thread

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import json
from MyScanner import Scanner
from threading import Semaphore
import Moderator as mod

sem = Semaphore(3)
req_result = 15

'''Receives a search_argument to insert it in the search bar and 
then clicks the search button.(include dates)'''


def fill_form_with_dates(driver, h):
    search_field = driver.find_element_by_id('ss')
    search_field.send_keys(h.dest)
    driver.find_element_by_class_name("sb-date-field__icon").click()
    while True:
        try:
            driver.find_element_by_xpath("//td[@data-date='{start_date}']".format(start_date=h.start_date)).click()
            driver.find_element_by_xpath("//td[@data-date='{end_date}']".format(end_date=h.end_date)).click()
            break;
        except:
            driver.find_element_by_class_name("bui-calendar__control--next").click()
    driver.find_element_by_class_name('sb-searchbox__button').click()  # We look for the search button and click it
    wait = WebDriverWait(driver, timeout=10).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, 'sr-hotel__title')))  # wait until the elements with the class name
    # sr-hotel-title (the one containing the accommodations titles) appear.


'''Receives a search_argument to insert it in the search bar and 
then clicks the search button.(without dates)'''


def fill_form_without_dates(driver, location_name):
    search_field = driver.find_element_by_id('ss')
    search_field.send_keys(location_name)
    driver.find_element_by_class_name('sb-searchbox__button').click()  # We look for the search button and click it
    WebDriverWait(driver, timeout=10).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, 'sr-hotel__title')))  # wait until the elements with the class name
    # sr-hotel-title (the one containing the accommodations titles) appear.


'''Returns the data from n_results amount of results.'''


def scrape_results(driver, n_results, h):
    accommodations_urls = get_all_hotel_links_per_driver(driver, n_results)
    accommodations_data = list()
    with open(os.path.dirname(__file__)+'/../Data/Hotels/Locations_Data/{location}_data.json'.format(location=h.dest), 'r') as JSON:
        location_dict = json.load(JSON)
    my_range = list(range(0, n_results))
    for url in my_range:
        url_data, can_order = scrape_accommodation_data(driver, accommodations_urls[url], h, location_dict)
        accommodations_data.append(url_data)
        if not can_order:
            n_results = n_results + 1
            my_range.append(n_results)
        print(url)
    return accommodations_data


'''return all the hotels in dest'''


def scrape_results_without_price(driver):
    accommodations_urls = get_all_hotel_links_per_driver(driver)
    accommodations_data = list()
    for url in range(0, len(accommodations_urls)):
        print(url)
        url_data = scrape_accommodation_data_without_price(driver, accommodations_urls[url])
        accommodations_data.append(url_data)
    return accommodations_data


'''Visits an accommodation page and extracts the data without price.'''


def scrape_accommodation_data_without_price(driver, accommodation_url):
    if driver == None:
        driver = Scanner.prepare_driver(accommodation_url)
    print(accommodation_url)
    driver.get(accommodation_url)
    accommodation_fields = dict()
    # Get the accommodation name
    accommodation_fields['name'] = driver.find_element_by_id('hp_hotel_name') \
        .text.strip('Hotel')
    # Get the accommodation score
    try:
        accommodation_fields['score'] = driver.find_element_by_class_name(
            'bui-review-score--end').find_element_by_class_name(
            'bui-review-score__badge').text
        try:
            all_box_grades = driver.find_element_by_class_name('v2_review-scores__body').find_elements_by_tag_name("li")
            driver.find_element_by_class_name('bui-review-score__title').click()
            for box_grade in all_box_grades:
                temp_title_score = box_grade.find_element_by_class_name('c-score-bar__title').text
                temp_grade_score = box_grade.find_element_by_class_name('c-score-bar__score').text
                accommodation_fields[temp_title_score] = temp_grade_score
        except:
            accommodation_fields['Location'] = '0'
    except:
        accommodation_fields['score'] = 'not enough reviews'
    # Get the accommodation location
    accommodation_fields['location'] = driver.find_element_by_id('showMap2') \
        .find_element_by_class_name('hp_address_subtitle').text
    # Get the most popular facilities
    try:
        accommodation_fields['popular_facilities'] = list()
        facilities = driver.find_element_by_class_name('hp_desc_important_facilities')
        for facility in facilities.find_elements_by_class_name('important_facility'):
            accommodation_fields['popular_facilities'].append(facility.text)
    except Exception:
        accommodation_fields['popular_facilities'].append('unknown')
    accommodation_fields['link'] = accommodation_url
    return accommodation_fields


'''return list of all the links of hotels in location,need to be already after searching the dest'''


def get_all_hotel_links_per_driver(driver, n=None):
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
    # Iterate over a defined range and scrape the links
    print('Finished get all the links %d' % len(accommodations_urls))

    return accommodations_urls


'''Visits an accommodation page and extracts the all the data(score,price,etc..).
    if the hotel already in the data get all the info from the dataset and only get the price from site
    else get all the data from the site and also add him to the dataset without price '''


def scrape_accommodation_data(driver, accommodation_url, h, location_dict):
    driver.get(accommodation_url)
    key = driver.find_element_by_id('hp_hotel_name') \
        .text.strip('Hotel')
    if key in location_dict:
        accommodation_fields = copy.deepcopy(location_dict[key])
    else:
        accommodation_fields = scrape_accommodation_data_without_price(driver, accommodation_url)
        location_dict[key] = accommodation_fields
        with open(os.path.dirname(__file__)+'/../Data/Hotels/Locations_Data/{location}_data.json'.format(location=h.dest), 'w') as f:
            f.write(json.dumps(location_dict, indent=4))
    return scrape_accommodation_data_only_price_and_update_dates(driver, accommodation_fields, h)


'''Visits an accommodation page and extracts the price only , also update the dates for this price.'''


def scrape_accommodation_data_only_price_and_update_dates(driver, accommodation_fields, h):
    accommodation_fields['Country'] = h.dest
    accommodation_fields['Check in'] = h.start_date
    accommodation_fields['Check out'] = h.end_date
    try:
        temp_price = driver.find_element_by_class_name('bui-price-display__value').text
        can_order = True
    except Exception:
        temp_price = 'no available'
        can_order = False
    accommodation_fields['price'] = temp_price
    return accommodation_fields, can_order


'''create JSON file with the data of location hotels in dates'''


def get_data_of_location_hotel_in_dates(h):
    try:
        driver = Scanner.prepare_driver('https://www.booking.com')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ss')))
        fill_form_with_dates(driver, h)
        accommodations_data = scrape_results(driver, req_result, h)
        accommodations_data = {item['name']: item for item in accommodations_data}  ## max need tp remove

        my_file = Path(
            os.path.dirname(__file__)+'/../Data/Hotels/Order_Data/{location}_{start_date}_{end_date}.json'.format(location=h.dest, start_date=h.start_date,
                                                                         end_date=h.end_date))
        if my_file.is_file():
            with open(os.path.dirname(__file__)+'/../Data/Hotels/Order_Data/{location}_{start_date}_{end_date}.json'.format(location=h.dest,
                                                                                   start_date=h.start_date,
                                                                                   end_date=h.end_date), 'r') as JSON:
                location_dict = json.load(JSON)
            accommodations_data.update(location_dict)
        accommodations_data = json.dumps(accommodations_data, indent=4)
        with open(os.path.dirname(__file__)+'/../Data/Hotels/Order_Data/{location}_{start_date}_{end_date}.json'.format(location=h.dest, start_date=h.start_date,
                                                                               end_date=h.end_date), 'w') as f:
            f.write(accommodations_data)
    finally:
        driver.quit()


'''create data of hotels in location , if choose all - update all the destinations else update the req one'''


def update_data_hotels(st='all'):
    if st == 'all':
        destinations = ['Berlin', 'London', 'Prague', 'Rome', 'Amsterdam', 'Belgrade', 'Milano', 'Madrid', 'Barcelona',
                        'Burgas', 'Sofia', 'Paris', 'Varna', 'Budapest', 'Bucharest', 'Thessaloniki', 'Kishinev']
        for location in destinations:
            sem.acquire()
            thread = Thread(target=update_data_per_location_hotels_without_dates, args=(location, sem))
            thread.start()
        thread.join()
    else:
        update_data_per_location_hotels_without_dates(st)


'''create JSON file with all the hotels of choosen location'''


def update_data_per_location_hotels_without_dates(location_name, sem=None):
    try:
        driver = Scanner.prepare_driver('https://www.booking.com')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ss')))
        fill_form_without_dates(driver, location_name)
        accommodations_data = scrape_results_without_price(driver)
        accommodations_data = {item['name']: item for item in accommodations_data}  ## max need tp remove
        accommodations_data = json.dumps(accommodations_data, indent=4)
        with open(os.path.dirname(__file__)+'/../Data/Hotels/Locations_Data/{location}_data.json'.format(location=location_name), 'w') as f:
            f.write(accommodations_data)

    except Exception as e:
        print(e.with_traceback())
    finally:
        if sem is not None:
            sem.release()
        driver.quit()
