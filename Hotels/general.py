import json
import os
from datetime import datetime
from pathlib import Path
from threading import Semaphore, Thread
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import fetch_utility
from fetch_utility import ByTechnique
from Hotel import Hotel
from Entity.Trip import Trip
from Flights import general as flight_general


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
    if not isinstance(destination, str) or not isinstance(by_technique, ByTechnique) or \
            not isinstance(multi_thread, int):
        raise ValueError("Wrong parameters type")
    sem = None
    if multi_thread is not None and multi_thread > 1:
        sem = Semaphore(int(multi_thread))
    if destination == 'all':
        airports_list = flight_general.get_list_of_all_destinations()
        if not airports_list:
            return
        destinations = {airport.city for airport in airports_list}
        threads = list()
        for location in destinations:
            if multi_thread is not None and multi_thread > 1:
                sem.acquire()
                thread = Thread(target=fetch_utility.update_data_per_location_hotels_without_dates,
                                args=(location, sem, by_technique))
                thread.start()
                threads.append(thread)
            else:
                fetch_utility.update_data_per_location_hotels_without_dates(location_name=location,
                                                                            by_technique=by_technique)
        if multi_thread is not None:
            for thread in threads:
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
        start_date_dt = datetime.strptime(trip.start_date, '%Y-%m-%d')
        already_fetched_check = Path(os.path.dirname(__file__) + '/../Data/Hotels/Order Data/{selected_month}/'
                                                                 '{location}/''{start_date}_{end_date}.json'.format(
            selected_month=datetime.strftime(start_date_dt, "%Y-%m"), location=trip.destination,
            start_date=trip.start_date, end_date=trip.end_date))
        if already_fetched_check.is_file():
            return
    except Exception:
        pass
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


def get_location_data_by_city_name(city_name, with_json_file=False):
    """
    give all the hotels with their information that store in data folder
    :param city_name: the name of city
    :type city_name: str
    :param with_json_file: decide if return only flight or
    append him his json path,by default is just return flight list
    :type with_json_file: bool
    :return: list with all hotels and their in information
    if json_file is true return list of [...,(hotel,json_path),....]
    else(by default) return list of [....,hotel,....]
    :rtype: list[Hotel]
    """

    if not isinstance(city_name, str) or not isinstance(with_json_file, bool):
        raise ValueError("Wrong types of parameters")
    path_to_json = os.path.dirname(__file__) + '//..//Data//Hotels//Locations Data//' + city_name + '.json'
    try:
        with open(path_to_json, 'r', encoding='utf-8') as f:
            hotels_data_dict = json.load(f)
    except FileNotFoundError:
        print(city_name + " not found(" + path_to_json + ")")
        return []
    hotels_data = []
    for key, val in hotels_data_dict.items():
        if with_json_file:
            hotels_data.append((Hotel(**val), path_to_json))
        else:
            hotels_data.append(Hotel(**val))
    return hotels_data


def get_all_location_data(with_json_file=False):
    """
    give all the hotels of all destinations with their information
    that store in data folder
    :param with_json_file: decide if return only flight or
    append him his json path,by default is just return flight list
    :type with_json_file: bool
    :return: list with all hotels and their in information
    if json_file is true return list of [...,(hotel,json_path),....]
    else(by default) return list of [....,hotel,....]
    :rtype: list[Hotel]
    """
    if not isinstance(with_json_file, bool):
        raise ValueError("with_json_file suppose to be boolean type")

    dest_list = flight_general.get_list_of_all_destinations()
    if not dest_list:
        return list()
    city_list = list(set([airport.city for airport in dest_list]))

    hotels_data = []
    for city in city_list:
        hotels_data.extend(get_location_data_by_city_name(city, with_json_file))
    return hotels_data
