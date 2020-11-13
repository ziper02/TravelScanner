import json
import os

from Entity.Country import Country


class Airport:
    """

    Attributes:
        name        The full name of airport
        code        Shortcut name of airport
        city        Airport's city, where the airport located
        country     Airport's country,where the airport located
    """
    __code: str
    __name: str
    __city: str
    __country: Country

    def __init__(self, code: str = '', **json_text: dict):
        if code != '':
            self.__code = code
            self.__config_attributes()
        else:
            try:
                json_text = json_text["json_text"]
            except Exception:
                pass
            self.__code = str(json_text["code"])
            self.__name = str(json_text["name"])
            self.__city = str(json_text["city"])
            self.__country = Country(**json_text.pop("country"))

    def __config_attributes(self):
        """
        initialize the details of airports according to his shortcut name(code)
        from local data
        """
        with open(os.path.dirname(__file__) + '/../Data/Flights/airports_countries.json') as f:
            data = json.load(f)
            self.__name = data[self.__code]["airportName"]
            self.__country = Country(name=data[self.__code]["countryName"],
                                     code=data[self.__code]["countryCode"])
            try:
                self.__city = data[self.__code]["city"]
            except Exception:
                self.__city = ''

    def to_json(self):
        """
        :return dictionary with all attributes
        :rtype: dict
        """
        return {
            "code": self.__code,
            "name": self.__name,
            "city": self.__city,
            "country": self.__country.to_json()
        }

    @property
    def name(self) -> str:
        return self.__name

    @property
    def code(self) -> str:
        return self.__code

    @code.setter
    def code(self, value: str):
        self.__code = value
        self.__config_attributes()

    @property
    def city(self) -> str:
        return self.__city

    @property
    def country(self) -> Country:
        return self.__country

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'Airport:: name: ' + self.name + ' code: ' + self.code + ' city: ' + self.city + '\n' + str(self.country)

    def __eq__(self, other):
        if isinstance(other, Airport):
            return self.code == other.name and self.code == other.name and \
                   self.country == other.country and self.__city == other.__city
        return False
