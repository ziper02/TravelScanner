import json
import os
from datetime import datetime

from Entity.Airport import Airport


class Flight:
    """

    Attributes:
        departure           The departure airport
        destination         The destination airport
        depart_date         The date of the flying out
        return_date         The date of the flying back
        days                The duration between the flights
        price               The price of round-trip for one adult person
        label               How cheap the flight is 1-expensive 4-cheap
        source              From where the data Skyscanner,Wizzair,etc
        data_set            Which Data-set this flight belongs-"train-set","test-set"
        calculated_value    mathematical value for estimate the value of flight - temporarily
        destination_value   The rating of destination-how attractive this destination
    """
    __departure: Airport
    __destination: Airport
    __depart_date: str
    __return_date: str
    __days: int
    __price: int
    __label: int
    __source: str
    __data_set: str
    __calculated_value: int
    __destination_value: int

    def __init__(self, departure: Airport = None, destination: Airport = None, depart_date: str = '',
                 return_date: str = '', price: int = -1,
                 source: str = 'unknown', label: int = -1, data_set: str = 'unknown', **json_text):
        if departure is not None:
            self.__departure = departure
            self.__destination = destination
            self.__depart_date = depart_date
            self.__return_date = return_date
            self.__price = price
            self.__label = label
            self.__source = source
            self.__data_set = data_set
            self.__calculated_value = -1
            self.__destination_value = -1
            self.__days = -1
        else:
            self.__dict__.update(json_text)
            self.__destination = Airport(json_text=json_text["__destination"])
            self.__departure = Airport(json_text=json_text["__departure"])
            with open(os.path.dirname(__file__) + "/../Data/Flights/dict_rate_dest.json", 'r', encoding="utf-8") as f:
                rate_dest = json.load(f)
            self.__destination_value = rate_dest[self.__destination.code]
            self.__days = (datetime.strptime(self.return_date, '%Y-%m-%d') - datetime.strptime(self.depart_date,
                                                                                               '%Y-%m-%d')).days

    def pretty_print(self):
        """
        :return: catchy phrase of flight's information
        :rtype: str
        """
        return "\ndestination:  " + str(self.__destination.name) + " " + str(self.__destination.country.name) + \
               "\ndepart date:  " + str(self.__depart_date) + " return date:  " + str(self.__return_date) + \
               "\nprice:  " + str(self.__price)

    @property
    def departure(self) -> Airport:
        return self.__departure

    @property
    def days(self) -> int:
        if self.__days != -1:
            return self.__days
        elif self.__depart_date != '' and self.__return_date != '':
            self.__days = (datetime.strptime(self.return_date, '%Y-%m-%d') - datetime.strptime(self.depart_date,
                                                                                               '%Y-%m-%d')).days
        return self.__days

    @property
    def destination(self) -> Airport:
        return self.__destination

    @property
    def destination_value(self) -> int:
        if self.__destination_value == -1 and self.__destination is not None:
            with open(os.path.dirname(__file__) + "/../Data/Flights/dict_rate_dest.json", 'r', encoding="utf-8") as f:
                rate_dest = json.load(f)
            self.__destination_value = rate_dest[self.__destination.code]
        return self.__destination_value

    @property
    def depart_date(self) -> str:
        return self.__depart_date

    @property
    def return_date(self) -> str:
        return self.__return_date

    @property
    def price(self) -> int:
        return self.__price

    @property
    def label(self) -> int:
        return self.__label

    @property
    def data_set(self) -> str:
        return self.__data_set

    def __eq__(self, other):
        if isinstance(other, Flight):
            if self.__depart_date == other.__depart_date and self.__departure == other.__departure \
                    and self.__destination == other.__destination and self.__return_date == other.__return_date \
                    and self.__price == other.__price:
                return True
        return False

    def __lt__(self, other):
        if isinstance(other, Flight):
            return self.__price < other.__price

    def __gt__(self, other):
        if isinstance(other, Flight):
            return self.__price > other.__price

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "Flight:: departure:  " + str(self.__departure) + "\ndestination:  " + str(self.__destination) + \
               "\ndepart date:  " + str(self.__depart_date) + " return date:  " + str(self.__return_date) + \
               "\nprice:  " + str(self.__price) + " label:  " + str(self.__label) + " data set:  " + str(
            self.__data_set)
