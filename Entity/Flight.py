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
                 source: str = 'unknown', label: int = -1, data_set: str = 'unknown', **json_text: dict):
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
            try:
                json_text = json_text["json_text"]
            except Exception:
                pass
            self.__depart_date = str(json_text["depart date"])
            self.__return_date = str(json_text["return date"])
            self.__price = json_text["price"]
            self.__label = json_text["label"]
            self.__source = str(json_text["source"])
            self.__data_set = str(json_text["data set"])
            self.__destination = Airport(**json_text.pop("destination"))
            self.__departure = Airport(**json_text.pop("departure"))
        try:
            with open(os.path.dirname(__file__) + "/../Data/Flights/dict_rate_dest.json", 'r', encoding="utf-8") as f:
                rate_dest = json.load(f)
            self.__destination_value = rate_dest[self.__destination.code]
        except Exception:
            pass
        if self.__depart_date != '' and self.__return_date != '':
            self.__days = (datetime.strptime(self.__return_date, '%Y-%m-%d') - datetime.strptime(
                self.__depart_date, '%Y-%m-%d')).days

    def to_json(self):
        """
        :return dictionary with all attributes
        :rtype: dict
        """
        return {
            "destination": self.__destination.to_json(),
            "departure": self.__departure.to_json(),
            "depart date": self.__depart_date,
            "return date": self.__return_date,
            "price": self.__price,
            "label": self.__label,
            "source": self.__source,
            "data set": self.__data_set
        }

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

    def __str__(self):
        return "\ndestination:  " + str(self.__destination.name) + " " + str(self.__destination.country.name) + \
               "\ndepart date:  " + str(self.__depart_date) + " return date:  " + str(self.__return_date) + \
               "\nprice:  " + str(self.__price)

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

    def __repr__(self):
        return "Flight:: departure:  " + str(self.__departure) + "\ndestination:  " + str(self.__destination) + \
               "\ndepart date:  " + str(self.__depart_date) + " return date:  " + str(self.__return_date) + \
               "\nprice:  " + str(self.__price) + " label:  " + str(self.__label) + " data set:  " + str(
            self.__data_set)
