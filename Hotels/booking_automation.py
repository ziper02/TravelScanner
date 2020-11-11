from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import booking_requests
import fetch_utility


def scrape_accommodation_data(driver, accommodation_url, trip, location_dict):
    """
    Visits an accommodation page and extracts the all the data(score,price,etc..).
    if the trip already in the data get all the info from the dataset and only get the price from site
    else get all the data from the site and also add him to the dataset without price
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver
    :param accommodation_url:list of all the url's that need to scrape
    :type accommodation_url: list(str)
    :param trip:the destination with check-in and check-out
    :type trip: Entity.Trip.Trip
    :param location_dict:dict with all known data from Location data
    :type location_dict: dict()
    :return:Hotel with all his data including prices between the dates
    :rtype: dict()
    """
    driver.get(accommodation_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'hp_hotel_name')))
    key = driver.find_element_by_id('hp_hotel_name') \
        .text.strip('trip').replace('\n', ' ')
    accommodation_fields = fetch_utility.get_hotel_data(driver, key, location_dict, fetch_utility.ByTechnique.selenium)
    if accommodation_fields is not None:
        return scrape_accommodation_data_only_price_and_update_dates(driver, accommodation_fields, trip)
    else:
        return None, None


def scrape_accommodation_data_without_price(driver, accommodation_url, need_fetch=False):
    """
    Visits an accommodation page and extracts the all the data(without price).
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver
    :param accommodation_url:the hotel's url
    :type accommodation_url: str
    :param need_fetch: True if need to use selenium for fetch data of hotel,otherwise false
    :type need_fetch: bool
    :return:Hotel with all his data without price
    :rtype: dict()
    """
    if driver is None:
        driver = fetch_utility.prepare_driver_chrome(accommodation_url)
    elif need_fetch:
        driver.get(accommodation_url)
    accommodation_fields = dict()
    # Get the accommodation name
    try:
        accommodation_fields['_name'] = driver.find_element_by_id('hp_hotel_name') \
            .text.strip('trip').replace('\n', ' ')
        # Get the accommodation score
    except Exception:
        return None
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
        except Exception:
            accommodation_fields['_location'] = '0'
    except Exception:
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


def scrape_accommodation_data_only_price_and_update_dates(driver, accommodation_fields, trip):
    """
    Visits an accommodation page and extracts the price only , also update the dict fields
    (price,checkin and checkout).
    if the scrape failed by selenium making GET request for get the data
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver
    :param accommodation_fields:The data of specific hotel dict{"hotel_name":data} without price and dates
    :type accommodation_fields: dict
    :param trip:the destination with check-in and check-out
    :type trip: Entity.Trip.Trip
    :return: dict{"hotel_name":data} of the specific hotel with price and dates and if hotel is available
    :rtype: dict,bool
    """
    accommodation_fields['_city'] = trip.destination
    accommodation_fields['_check_in'] = trip.start_date
    accommodation_fields['_check_out'] = trip.end_date
    try:
        temp_price = driver.find_element_by_class_name('bui-price-display__value').text
        can_order = True
    except Exception:
        try:
            return booking_requests.scrape_accommodation_data_only_price_and_update_dates(
                accommodation_fields, trip, page=driver.current_url, make_get_request=True)
        except Exception:
            temp_price = 'no available'
            can_order = False
    accommodation_fields['_fetch_date'] = datetime.today().strftime('%Y-%m-%d')
    accommodation_fields['_price'] = temp_price
    return accommodation_fields, can_order
