import copy


class Hotel:
    """

    Attributes:
        name                    The full name of  hotel
        city                    The city that hotel located
        price                   Total price for 2 adults for one room
        score                   The general score for this hotel by users
        location                The location score for this hotel by users
        address                 The address of hotel
        staff                   The staff score for this hotel by users
        popular_facilities      Which facilities this hotel offer
        facilities              The facilities score for this hotel by users
        value_for_money         The value for money score for this hotel by users
        free_wifi               The wifi score for this hotel by users
        cleanliness             The cleanliness score for this hotel by users
        comfort                 The comfort score for this hotel by users
        link                    Url of Booking.com for this site
    """
    __name: str
    __city: str
    __price: int
    __score: int
    __location: int
    __address: str
    __staff: int
    __popular_facilities: list
    __facilities: int
    __value_for_money: int
    __free_wifi: int
    __cleanliness: int
    __comfort: int
    __link: str

    def __init__(self, name: str = '', city: str = '', value_for_money: int = -1, staff: int = -1, facilities: int = -1,
                 location: int = -1, free_wifi: int = -1, cleanliness: int = -1, score: int = -1,
                 popular_facilities: list = [],
                 comfort: int = -1, link: str = '', address: str = '', price: int = -1, check_in: str = '',
                 check_out: str = '', **json_text):
        if city != '':
            self.__name = name
            self.__city = city
            self.__value_for_money = value_for_money
            self.__staff = staff
            self.__facilities = facilities
            self.__location = location
            self.__free_wifi = free_wifi
            self.__cleanliness = cleanliness
            self.__score = score
            self.__popular_facilities = copy.copy(popular_facilities)
            self.__comfort = comfort
            self.__link = link
            self.__address = address
            self.__price = price
            self.__check_in = check_in
            self.__check_out = check_out
        else:
            self.__dict__.update(json_text)

    def pretty_print(self):
        """
        :return: catchy phrase of hotel's information
        :rtype: str
        """
        return "name: " + str(self.__name) + " city: " + str(self.__city) + "\nscore: " \
               + str(self.__score) + " location: " + str(self.__location) + " price: " \
               + str(self.__price)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def check_in(self) -> str:
        return self.__check_in

    @property
    def address(self) -> str:
        return self.__address

    @property
    def check_out(self) -> str:
        return self.__check_out

    @property
    def city(self) -> str:
        return self.__city

    @property
    def value_for_money(self) -> int:
        return self.__value_for_money

    @property
    def staff(self) -> int:
        return self.__staff

    @property
    def facilities(self) -> int:
        return self.__facilities

    @property
    def location(self) -> int:
        return self.__location

    @property
    def free_wifi(self) -> int:
        return self.__free_wifi

    @property
    def cleanliness(self) -> int:
        return self.__cleanliness

    @property
    def score(self) -> int:
        return self.__score

    @property
    def popular_facilities(self) -> list:
        return self.__popular_facilities

    @property
    def comfort(self) -> int:
        return self.__comfort

    @property
    def link(self) -> str:
        return self.__link

    @property
    def price(self) -> int:
        return self.__price

    def __str__(self):
        return "Hotel:: name: " + self.__name + " city: " + self.__city + " score: " + str(self.__score) \
               + " location: " + str(self.__location) + " price: " + str(self.__price) + "\nvalue for money: " \
               + str(self.__value_for_money) + " staff: " + str(self.__staff) + " location: " + str(self.__location) \
               + " free wifi: " + str(self.__free_wifi) + "\ncleanliness: " + str(self.__cleanliness) + " comfort: " \
               + str(self.__comfort) + " link: " + str(self.__link) + " address: " + self.__address

    def __eq__(self, other):
        if isinstance(other, Hotel):
            return self.name == other.name and self.__city == other.__city
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
