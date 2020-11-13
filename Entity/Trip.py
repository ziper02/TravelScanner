from datetime import datetime
from Hotels import general as general_hotel
from Entity.Hotel import Hotel
from Entity.Flight import Flight
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
    __price: int
    __alternative_hotels: list

    def __init__(self, flight: Flight = None, start_date: str = '', end_date: str = '', hotel: Hotel = None,
                 price: int = -1):
        if flight is not None and end_date == '' and start_date == '' and hotel is None and price == -1:
            self.__flight = flight
            self.__end_date = self.__flight.return_date
            self.__start_date = self.__flight.depart_date
            self.__hotel = Hotel(city=self.flight.destination.city)
            self.__update_hotels()
            self.__price = 2 * self.__flight.price + self.__hotel.price
        else:
            self.__flight = flight
            self.__end_date = end_date
            self.__start_date = start_date
            self.__hotel = hotel
            self.__alternative_hotels = []
            self.__price = price

    def __update_hotels(self, fetch_date: str = datetime.today().strftime('%Y-%m-%d')):
        """
        update the hotel that selected for trip in Hotel and also offer other alternative hotels
        for this trip in alternative_hotels 
        :param fetch_date:the date that the data fetched
        :type fetch_date: Datetime
        """
        hotel_general.get_data_of_location_hotel_in_dates(self)
        hotels_data = general_hotel.get_data_by_name(self, fetch_date)
        hotels_data = [hotel for hotel in hotels_data if hotel.price != 'no available']
        hotels_data = [hotel for hotel in hotels_data if not isinstance(hotel.price, str)]
        hotels_data.sort(key=lambda x: int(x.price), reverse=False)
        self.__hotel = hotels_data.pop(0)
        self.__alternative_hotels = hotels_data

    @property
    def hotel(self) -> Hotel:
        return self.__hotel

    @property
    def flight(self) -> Flight:
        return self.__flight

    @property
    def price(self) -> int:
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
        return self.__hotel.city

    def __repr__(self):
        return "Flight:\n" + str(self.__flight) + "\n" + "Hotel:\n" + str(self.__hotel)

    def __str__(self):
        return "Flight:" + self.__flight + "\n" + "Hotel:\n" + self.__hotel + \
               "\n Total price: " + str(self.__price)
