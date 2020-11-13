import json
import os
from datetime import datetime
from threading import Semaphore, Thread
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import fetch_utility
from fetch_utility import ByTechnique
from Hotel import Hotel
from Entity.Trip import Trip
from Flights import general as flight_general


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
    with open(os.path.dirname(__file__) + '/../Data/Hotels/Order Data/{selected_month}'
                                          '/{location}/{start_date}_{end_date}.json'.format(
            selected_month=datetime.strftime(start_date_dt, "%Y-%m"),
            location=trip.destination, start_date=trip.start_date,
            end_date=trip.end_date), 'r') as f:
        hotels_data = json.load(f)
    hotels = []
    for hotel_key, hotel_val in hotels_data.items():
        if hotels_data[hotel_key]['fetch date'] == fetch_date:
            hotels.append(Hotel(**hotels_data[hotel_key]))
    return hotels


def update_data_hotels(destination='all', by_technique=ByTechnique.selenium, multi_thread=None):
    """
    create json with data of hotels in location at Data/Hotel/Location/{destination}.json,
    if chose all(by default)- update all the destinations else update the required one.
    :param destination:The full name of destination to update,the default is to update all
    :type destination: str
    :param by_technique: which technique use for fetch data selenium/get
    :type by_technique: ByTechnique
    :param multi_thread: how much threads use for fetch data or none for single thread
    :type multi_thread: int
    """
    sem = None
    if multi_thread is not None and multi_thread>1:
        sem = Semaphore(int(multi_thread))
    if destination == 'all':
        airports_list = flight_general.get_list_of_all_destinations()
        destinations = {airport.city for airport in airports_list}
        thread = None
        for location in destinations:
            if multi_thread is not None and multi_thread>1:
                sem.acquire()
                thread = Thread(target=fetch_utility.update_data_per_location_hotels_without_dates,
                                args=(location, sem, by_technique))
                thread.start()
            else:
                fetch_utility.update_data_per_location_hotels_without_dates(location_name=location,
                                                                            by_technique=by_technique)
        if multi_thread is not None:
            sem.acquire()
        thread.join()
    else:
        fetch_utility.update_data_per_location_hotels_without_dates(destination, by_technique=by_technique)


def get_data_of_location_hotel_in_dates(trip, by_technique=ByTechnique.selenium):
    """
    get data for order hotel that fitting flight and create JSON file with the data
    of location hotels in dates at: /Order Data/{MM-YYYY of Check-in}/{Destination}/
    {Check-in}_{Check-out}.json
    :type by_technique: ByTechnique
    :param by_technique: which technique use for fetch data selenium/get
    :param trip: Trip object with Destination,Check-in and Check-out
    :type trip: Trip
    """
    req_result = 200
    driver = None
    try:
        driver = fetch_utility.prepare_driver_chrome('https://www.booking.com')  # lunch driver to Booking
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, 'ss')))
        fetch_utility.fill_form_with_dates(driver, trip)
        accommodations_data = fetch_utility.fetch_data_for_trip(driver, req_result, trip,
                                                                by_technique)  # get the data from driver
        accommodations_data = {item['name']: item for item in accommodations_data}  # transfer the list to dict
        fetch_utility.save_hotels_order_data_to_json(accommodations_data, trip)
    finally:
        if driver:
            driver.quit()
