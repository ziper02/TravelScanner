import json
import os
from datetime import datetime
import fetch_utility
from Entity.Flight import Flight
from Entity.Hotel import Hotel
from Hotels import general as hotel_general


class Trip:
    """

    Attributes:
        flight       The flights to destination and return
        hotel        The hotel for accommodation
        start_date   The date when the trip is start-when need to checkin and  flight to destination
        end_date     The date when the trip is over-when need to checkout and take back flight
        price        The total price for 2 adults for this package
    """
    __flight: Flight
    __hotel: Hotel
    __start_date: str
    __end_date: str
    __price: float
    __alternative_hotels: list

    def __init__(self, flight: Flight = None, start_date: str = '', end_date: str = '', hotel: Hotel = None,
                 price: int = -1):
        if flight is not None and end_date == '' and start_date == '' and hotel is None and price == -1:
            self.__flight = flight
            self.__end_date = self.__flight.return_date
            self.__start_date = self.__flight.depart_date
            self.__hotel = (Hotel(city_located=self.__flight.destination.city) if hotel is None else hotel)
            self.__price = 2 * self.__flight.price + (self.__hotel.price if self.__hotel.price > 0 else 0)
        else:
            self.__flight = flight
            self.__end_date = end_date
            self.__start_date = start_date
            self.__hotel = hotel
            self.__alternative_hotels = []
            self.__price = price

    def get_hotel_for_trip(self, fetch_date: str = datetime.today().strftime('%Y-%m-%d')):
        """
        update the hotel that selected for trip in Hotel and also offer other alternative hotels
        for this trip in alternative_hotels
        :param fetch_date:the date that the data fetched
        :type fetch_date: Datetime
        """
        hotel_general.get_data_of_location_hotel_in_dates(self, by_technique=fetch_utility.ByTechnique.requests)
        hotels_data = self.__get_hotel_order_data_from_data_folder(fetch_date)
        hotels_data = [hotel for hotel in hotels_data if not isinstance(hotel.price, str)]
        hotels_data = [hotel for hotel in hotels_data if hotel.price != 'no available' and hotel.price > 0]
        hotels_data.sort(key=lambda x: int(x.price), reverse=False)
        self.__hotel = hotels_data.pop(0)
        self.__price = 2 * self.__flight.price + (self.__hotel.price if self.__hotel.price > 0 else 0)
        self.__alternative_hotels = hotels_data

    def __get_hotel_order_data_from_data_folder(self, fetch_date=datetime.today().strftime('%Y-%m-%d')):
        """
        get hotels list for the required flight in trip
        :param fetch_date: date of fetch from booking
        :type fetch_date: str
        :return: list of hotels in asked date and flight
        :rtype: list[Hotel]
        """
        start_date_dt = datetime.strptime(self.__start_date, '%Y-%m-%d')
        with open(os.path.dirname(__file__) + '/../Data/Hotels/Order Data/{selected_month}'
                                              '/{location}/{start_date}_{end_date}.json'.format(
            selected_month=datetime.strftime(start_date_dt, "%Y-%m"), location=self.destination,
            start_date=self.__start_date, end_date=self.__end_date), 'r') as f:
            hotels_data = json.load(f)
        hotels = []
        for hotel_key, hotel_val in hotels_data.items():
            if hotels_data[hotel_key]['fetch date'] == fetch_date:
                hotels.append(Hotel(**hotels_data[hotel_key]))
        return hotels

    @property
    def hotel(self) -> Hotel:
        return self.__hotel

    @property
    def flight(self) -> Flight:
        return self.__flight

    @property
    def price(self) -> float:
        return self.__price

    @property
    def alternative_hotels(self):
        return self.__alternative_hotels

    @property
    def end_date(self) -> str:
        return self.__end_date

    @property
    def start_date(self) -> str:
        return self.__start_date

    @property
    def destination(self) -> str:
        return self.__flight.destination.city

    def __repr__(self):
        return "Flight:\n" + str(self.__flight) + "\n" + "Hotel:\n" + str(self.__hotel)

    def __str__(self):
        return "Flight:" + str(self.__flight) + "\n" + "Hotel:\n" + str(self.__hotel) + \
               "\nTotal price: " + str(self.__price)

    def __lt__(self, other):
        if isinstance(other, Trip):
            return self.__price < other.__price

    def __gt__(self, other):
        if isinstance(other, Trip):
            return self.__price > other.__price

    # -----------------------------------------------------------------------------------------------------------------
