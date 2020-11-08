from Entity.Hotel import Hotel
from Entity.Flight import Flight
#hotel.destination
class Trip:
    
    def __init__(self,flight,hotel=None,alternative_hotels=[]):
        self._flight=flight
        self._hotel = hotel
        self._alternative_hotels = alternative_hotels
        self._price=-1
        
    @property
    def hotel(self):
        return self._hotel 
    
    @property
    def flight(self):
        return self._flight
    
    @property
    def price(self):
        return 
    
    @price.setter
    def price(self, value):
        self._price=value
    
    @property
    def end_date(self):
        return self._flight.return_date

    @property
    def start_date(self):
        return self._flight.departe_date

        
    @property
    def destination(self):
        return self._hotel.city
    
    @destination.setter
    def destination(self, value):
        self._hotel.city=value