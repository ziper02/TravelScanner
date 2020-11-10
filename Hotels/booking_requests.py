import json
import os
import re
from datetime import datetime
from threading import Semaphore

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import booking_automation
from Hotels import general as hotel_general

import requests
from data_manager import data_manager



def update_data_per_location_hotels_without_dates(location_name, sem=None):
    """
    create json with data of hotels in location atData/Hotel/Location/{destination}.json
    for the required one using automation for get hotel links and GET requests for get data of hotels
    :param location_name:The full name of destination to update
    :type location_name: str
    :param sem: semaphore for multithreading fetch
    :type sem: threading.Semaphore
    """
    try:
        driver = hotel_general.prepare_driver_chrome('https://www.booking.com')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ss')))
        booking_automation.fill_form_without_dates(driver, location_name)
        accommodations_urls = booking_automation.get_all_hotel_links_per_driver(driver)
        accommodations_data = list()
        for url in range(0, len(accommodations_urls)):
            url_data = scrape_accommodation_data_without_price(driver, accommodations_urls[url])
            accommodations_data.append(url_data)
        accommodations_data = {item['_name']: item for item in accommodations_data}  ## max need tp remove
        with open(os.path.dirname(__file__) + '/../Data/Hotels/Locations Data/{location}.json'.format(
                location=location_name), 'w', encoding="utf-8") as f:
            json.dump(accommodations_data, f, indent=4)
    finally:
        if sem is not None:
            sem.release()


def scrape_accommodation_data_only_price_and_update_dates(accommodation_fields, trip, page='', make_get_request=False):
    """
    Visits an accommodation page and extracts the price only , also update the dict fields
    (price,checkin and checkout).
    :param accommodation_fields:The data of specific hotel dict{"hotel_name":data} without price and dates
    :type accommodation_fields: dict
    :param trip:the destination with check-in and check-out
    :type trip: Trip
    :param page: if make_get_request is false its html page of hotel from booking.com
                else its url of hotel from booking.com
    :type page: str
    :param make_get_request: True is need new GET request else use page as html mage
    :type make_get_request: bool
    :return: dict{"hotel_name":data} of the specific hotel with price and dates and if hotel is available
    :rtype: dict,bool
    """
    accommodation_fields['_city'] = trip.destination
    accommodation_fields['_check_in'] = trip.start_date
    accommodation_fields['_check_out'] = trip.end_date
    try:
        if make_get_request:
            request_url = page.replace('.html', '.en-gb.html') + data_manager.booking_order_address.format(
                start_date=trip.start_date, end_date=trip.end_date)
            request = requests.get(url=request_url, headers=data_manager.booking_headers)
            page = request.text
        m = re.search(r'"b_price":"₪\s*([^\n$"]+)', page)
        price = int(m.group(1).replace(',', ''))
        can_order = True
    except Exception:
        price = 'no available'
        can_order = False
    accommodation_fields['_fetch_date'] = datetime.today().strftime('%Y-%m-%d')
    accommodation_fields['_price'] = price
    return accommodation_fields, can_order


def scrape_accommodation_data_without_price(page, accommodation_url):
    """
    extracts the all the data(without price) from HTML page.
    :param page:html page of hotel from booking.com
    :type page: str
    :param accommodation_url: the url of page hotel in booking
    :type accommodation_url: str
    :return:Hotel with all his data without price
    :rtype: dict()
    """
    accommodation_fields = dict()
    accommodation_fields['_link'] = accommodation_url
    found = False
    count = 0
    html_page = re.split(page, '\n')
    for line in html_page:
        if count < 500:
            if '<div class="c-score-bar" ><span class="c-score-bar__title">' in line:
                if not found:
                    found = True
                m = re.split('<div class="c-score-bar" ><span class="c-score-bar__title">', line)
                m2 = re.split('<span class="c-score-bar__score">', line)
                if '&nbsp' in m[1]:
                    temp = re.split('&nbsp', m[1])
                    title = temp[0]
                else:
                    temp = re.split('<', m[1])
                    title = temp[0]
                temp = re.split('</span', m2[1])
                score = temp[0]
                title = "_" + title.lower().rstrip().replace(" ", "_")
                accommodation_fields[title] = score
            if 'id="hp_hotel_name"' in line:
                lst = []
                while not '</h2>' in line:
                    lst.append(line)
                    line = next(html_page)
                hotel_name = lst[-1].rstrip()
                accommodation_fields['_name'] = hotel_name
            if 'hp_address_subtitle' in line:
                lst = []
                while not '</span>' in line:
                    lst.append(line)
                    line = next(html_page)
                address = lst[-1].rstrip()
                accommodation_fields['_address'] = address
            if 'important_facility  "' in line:
                line = next(html_page)
                if '_popular_facilities' not in accommodation_fields.keys():
                    accommodation_fields['_popular_facilities'] = []
                facility = re.findall('"([^"]*)"', line)[0]
                accommodation_fields['_popular_facilities'].append(facility)
            if found:
                count = count + 1
        elif found:
            break
    return accommodation_fields



