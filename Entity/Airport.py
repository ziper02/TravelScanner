import json
import os

from Entity.Country import Country


class Airport:

    def __init__(self, code='', **dict):
        if code != '':
            self._code = code
            self.__config_attributes()
        else:
            self.__dict__.update(dict["dict"])
            self._country = Country(dict=dict["dict"]["_country"])

    @property
    def name(self):
        return self._name


    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value
        self.__config_attributes()

    @property
    def city(self):
        return self._city

    @property
    def country(self):
        return self._country

    def __eq__(self, other):
        if isinstance(other, Airport):
            return self.code == other.name and self.code == other.name and self.country == other.country  and self._city == other._city
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'Airport:: name: ' + self.name + ' code: ' + self.code + ' city: '+ self.city + '\n' + str(self.country)

    def __config_attributes(self, code=None):
        if code == None:
            code = self._code
        with open(os.path.dirname(__file__) + '/../Data/Flights/airports_countries.json') as f:
            data = json.load(f)
            tessss=data[code]
            self._name = data[code]["airportName"]
            self._country = Country(name=data[code]["countryName"],
                                    code=data[code]["countryCode"])
            try:
                self._city=data[code]["city"]
            except:
                self._city=''
