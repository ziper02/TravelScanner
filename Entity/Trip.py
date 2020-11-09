import json
import os
from datetime import datetime
from Hotels import General as general_hotel
from Entity.Hotel import Hotel
from Entity.Flight import Flight
from Hotels import Booking

class Trip:
    
    def __init__(self,flight):
        self._flight=flight
        self._end_date=self._flight.return_date
        self._start_date=self._flight.depart_date
        self._hotel = Hotel(city=self.flight.destination.city)
        self.__update_hotels()
        self._price=2*(self._flight.price)+self._hotel.price
        
    @property
    def hotel(self) -> Hotel:
        return self._hotel
    
    @property
    def flight(self)-> Flight:
        return self._flight
    
    @property
    def price(self) -> int:
        return self._price

    
    @property
    def end_date(self)-> str:
        return self._end_date

    @property
    def start_date(self)-> str:
        return self._start_date

        
    @property
    def destination(self)->str:
        """
        :return: Full name of Airport's city
        """
        return self._hotel.city
    
    @destination.setter
    def destination(self, value:str):
        """
        :param value:Insert Full name of Airport's city
        """
        self._hotel.city=value

    @flight.setter
    def flight(self, value: Flight):
        self._flight=value
        self._hotel=Hotel(city=self.flight.destination.city)
        self.__update_hotels()


    def __update_hotels(self, fetch_date: str = datetime.today().strftime('%Y-%m-%d')) :
        """
        :param fetch_date:get hotel list in selected fetch date
        """
        Booking.get_data_of_location_hotel_in_dates(self)
        hotels_data=general_hotel.get_data_by_name(self,fetch_date)
        hotels_data=[hotel for hotel in hotels_data if hotel.price!='no available']
        general_hotel.filter_by_location(hotels_data,8.5)
        general_hotel.filter_by_location(hotels_data, 8.5)
        hotels_data=[hotel for hotel in hotels_data if not isinstance(hotel.price, str)]
        hotels_data.sort(key=lambda x: int(x.price), reverse=False)
        self._hotel=hotels_data.pop(0)
        self._alternative_hotels=hotels_data


    def __str__(self):
        return "Flight:\n"+self._flight+"\n"+"Hotel:\n"+self._hotel

    def pretty_print(self):
        return "Flight:"+self._flight.pretty_print()+"\n"+"Hotel:\n"+self._hotel.pretty_print()+\
               "\n Total price: "+str(self._price)