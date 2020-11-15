import json
import os
from datetime import datetime

from DataManager import DataManager
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
    __price: float
    __label: int
    __source: str
    __data_set: str
    __calculated_value: int
    __destination_value: int

    with open(os.path.dirname(__file__) + "/../Data/Flights/dict_rate_dest.json", 'r', encoding="utf-8") as f:
        __rate_dest = json.load(f)

    def __init__(self, flying_out: Airport = None, flying_back: Airport = None, flying_out_date: str = '',
                 flying_back_date: str = '', price_per_adult: int = -1,
                 source_site: str = 'unknown', rating_of_flight: int = -1, data_set_of_flight: str = 'unknown',
                 **json_text: dict):
        if flying_out is not None:
            self.__departure = flying_out
            self.__destination = flying_back
            self.__depart_date = flying_out_date
            self.__return_date = flying_back_date
            self.__price = price_per_adult
            self.__label = rating_of_flight
            self.__source = source_site
            self.__data_set = data_set_of_flight
            self.__calculated_value = -1
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
            self.__destination_value = self.__rate_dest[self.__destination.code]
        except Exception:
            self.__destination_value = -1
        if self.__depart_date != '' and self.__return_date != '':
            self.__days = (datetime.strptime(self.__return_date, '%Y-%m-%d') - datetime.strptime(
                self.__depart_date, '%Y-%m-%d')).days
        else:
            self.__days = -1

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
    def source(self):
        return self.__source

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
            self.__destination_value = self.__rate_dest[
                DataManager.transfer_airport_cod_names_to_all(self.__destination.code)]
        return self.__destination_value

    @property
    def depart_date(self) -> str:
        return self.__depart_date

    @property
    def return_date(self) -> str:
        return self.__return_date

    @property
    def price(self) -> float:
        return self.__price

    @property
    def label(self) -> int:
        return self.__label

    @label.setter
    def label(self, value):
        if isinstance(value, int):
            if -1 < value < 5:
                self.__label = value

    @property
    def data_set(self) -> str:
        return self.__data_set

    @data_set.setter
    def data_set(self, value):
        if isinstance(value, str):
            if value == "Train" or value == "Test":
                self.__data_set = value

    def __str__(self):
        if self.__destination.city != '':
            return "\ndestination: " + str(self.__destination.city) + "(" + str(self.__destination.code) + ") " \
                   + str(self.__destination.country.name) + "\ndepart date: " + str(self.__depart_date) \
                   + " return date: " + str(self.__return_date) + "\nprice: " + str(self.__price) + " site source: " \
                   + str(self.__source)
        else:
            return "\ndestination: " + str(self.__destination.name) + "(" + str(self.__destination.code) + ") " \
                   + str(self.__destination.country.name) + "\ndepart date: " + str(self.__depart_date) \
                   + " return date: " + str(self.__return_date) + "\nprice: " + str(self.__price) + " site source: " \
                   + str(self.__source)

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
