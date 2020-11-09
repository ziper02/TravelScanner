import json
import os
from datetime import datetime

from Hotel import Hotel
from Entity.Trip import Trip


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


def filter_by_score(hotels_data, score: int) :
    """
    :rtype: list(Hotels)
    :type hotels_data: list(Hotels)
    """
    hotels_data = [hotel for hotel in hotels_data if float(hotel.score) >= score]
