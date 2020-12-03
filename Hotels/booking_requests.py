import re
from datetime import datetime
import fetch_utility
import requests
from DataManager import DataManager
from bs4 import BeautifulSoup


def scrape_accommodation_data(accommodation_url, trip, location_dict):
    """
    Visits an accommodation page and extracts the all the data(score,price,etc..).
    if the trip already in the data get all the info from the dataset and only get the price from site
    else get all the data from the site and also add him to the dataset without price
    :param accommodation_url:list of all the url's that need to scrape
    :type accommodation_url: list[str]
    :param trip:the destination with check-in and check-out
    :type trip: Trip.Trip
    :param location_dict:dict with all known data from Location data
    :type location_dict: dict()
    :return:Hotel with all his data including prices between the dates
    :rtype: dict()
    """
    request_url = accommodation_url.replace('.html', '.en-gb.html') + DataManager.booking_order_address.format(
        start_date=trip.start_date, end_date=trip.end_date)
    request_url=accommodation_url
    request = requests.get(url=request_url, headers=DataManager.booking_headers)
    page = request.text
    html_page = page.split('\n')
    key = None
    for i in range(len(html_page)):
        line = html_page[i]
        if 'id="hp_hotel_name"' in line:
            lst = []
            while '</h2>' not in line:
                lst.append(line)
                i = i + 1
                line = html_page[i]
            pre = re.search(r'>(.*?)<', lst[-2]).group(1).replace('\n', ' ')
            hotel_name = lst[-1].rstrip()
            key = pre + ' ' + hotel_name
    accommodation_fields = fetch_utility.get_hotel_data(page=page, key=key, trip=trip, location_dict=location_dict,
                                                        by_technique=fetch_utility.ByTechnique.requests,
                                                        accommodation_url=accommodation_url)
    if accommodation_fields is not None:
        return scrape_accommodation_data_only_price_and_update_dates(accommodation_fields, trip, page)
    else:
        return None


def scrape_accommodation_data_without_price(page='', accommodation_url='', need_fetch=False):
    """
    extracts the all the data(without price) from HTML page.
    :param page:html page of hotel from booking.com
    :type page: str
    :param accommodation_url: the url of page hotel in booking
    :type accommodation_url: str
    :param need_fetch: True if need to use selenium for fetch data of hotel,otherwise false
    :type need_fetch: bool
    :return:Hotel with all his data without price
    :rtype: dict()
    """
    if need_fetch:
        request_url = accommodation_url.replace('.html', '.en-gb.html')
        try:
            request = requests.get(url=request_url, headers=DataManager.booking_headers)
        except Exception:
            return None
        page = request.text
    accommodation_fields = dict()
    accommodation_fields['link'] = accommodation_url
    found = False
    count = 0
    html_page = page.splitlines()
    for i in range(len(html_page)):
        line = html_page[i]
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
                score = float(temp[0])
                title = title.lower().rstrip().lstrip()
                accommodation_fields[title] = score
            if 'hp_address_subtitle' in line:
                lst = []
                while '</span>' not in line:
                    lst.append(line)
                    i = i + 1
                    line = html_page[i]
                address = lst[-1].rstrip()
                accommodation_fields['address'] = address
            if 'important_facility  "' in line:
                i = i + 1
                line = html_page[i]
                if 'popular facilities' not in accommodation_fields.keys():
                    accommodation_fields['popular facilities'] = []
                facility = re.findall('"([^"]*)"', line)[0]
                accommodation_fields['popular facilities'].append(facility)
            if 'id="hp_hotel_name"' in line:
                lst = []
                while '</h2>' not in line:
                    lst.append(line)
                    i = i + 1
                    line = html_page[i]
                pre = re.search(r'>(.*?)<', lst[-2]).group(1).replace('\n', ' ')
                hotel_name = lst[-1].rstrip()
                accommodation_fields['name'] = pre + ' ' + hotel_name
            if found:
                count = count + 1
            if '<div class="bui-review-score c-score bui-review-score--end">' in line:
                soup = BeautifulSoup(line, 'html.parser')
                accommodation_fields['score'] = float(soup.find(class_="bui-review-score__badge")
                                                      .get_text().lstrip().rstrip())
        elif found:
            break
    return accommodation_fields


def scrape_accommodation_data_only_price_and_update_dates(accommodation_fields, trip, page='', make_get_request=False):
    """
    Visits an accommodation page and extracts the price only , also update the dict fields
    (price,checkin and checkout).
    :param accommodation_fields:The data of specific hotel dict{"hotel_name":data} without price and dates
    :type accommodation_fields: dict
    :param trip:the destination with check-in and check-out
    :type trip: Trip.Trip
    :param page: if make_get_request is false its html page of hotel from booking.com
                else its url of hotel from booking.com
    :type page: str
    :param make_get_request: True is need new GET request else use page as html mage
    :type make_get_request: bool
    :return: dict{"hotel_name":data} of the specific hotel with price and dates and if hotel is available
    :rtype: dict,bool
    """
    accommodation_fields['city'] = trip.destination
    accommodation_fields['check in'] = trip.start_date
    accommodation_fields['check out'] = trip.end_date
    try:
        if make_get_request:  # if need to send request for get price, its insert
            # the price to page else use page from input
            request_url = page.replace('.html', '.en-gb.html') + DataManager.booking_order_address.format(
                start_date=trip.start_date, end_date=trip.end_date)
            request = requests.get(url=request_url, headers=DataManager.booking_headers)
            page = request.text
        m = re.search(r'"b_price":"₪\s*([^\n$"]+)', page)
        price = float(m.group(1).replace(',', ''))
        can_order = True
    except Exception:
        price = -1
        can_order = False
    accommodation_fields['fetch date'] = datetime.today().strftime('%Y-%m-%d')
    accommodation_fields['price'] = price
    return accommodation_fields, can_order
