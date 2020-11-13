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
    __price: float
    __score: float
    __location: float
    __address: str
    __staff: float
    __popular_facilities: list
    __facilities: float
    __value_for_money: float
    __free_wifi: float
    __cleanliness: float
    __comfort: float
    __link: str

    def __init__(self, name_of_hotel: str = '', city_located: str = '', value_for_money: float = -1,
                 staff_score: float = -1, facilities_score: float = -1,  location_score: float = -1,
                 free_wifi_score: float = -1, cleanliness_score: float = -1, general_score: float = -1,
                 popular_facilities: list = None, comfort_score: float = -1, url: str = '', address_of_hotel: str = '',
                 price_for_one_room: float = -1, check_in: str = '', check_out: str = '', fetch_date: str = '',
                 **json_text: dict):
        if city_located != '':
            self.__name = name_of_hotel
            self.__city = city_located
            self.__value_for_money = value_for_money
            self.__staff = staff_score
            self.__facilities = facilities_score
            self.__location = location_score
            self.__free_wifi = free_wifi_score
            self.__cleanliness = cleanliness_score
            self.__score = general_score
            if popular_facilities is not None:
                self.__popular_facilities = copy.copy(popular_facilities)
            else:
                self.__popular_facilities = []
            self.__comfort = comfort_score
            self.__link = url
            self.__address = address_of_hotel
            self.__price = price_for_one_room
            self.__check_in = check_in
            self.__check_out = check_out
            self.__fetch_date = fetch_date
        else:  # the data come as json
            self.__name = str(json_text["name"])
            try:
                self.__value_for_money = json_text["value for money"]
            except Exception:
                self.__value_for_money = -1
            try:
                self.__staff = json_text["staff"]
            except Exception:
                self.__staff = -1
            try:
                self.__facilities = json_text["facilities"]
            except Exception:
                self.__facilities = -1
            try:
                self.__location = json_text["location"]
            except Exception:
                self.__location = -1
            try:
                self.__free_wifi = json_text["free wifi"]
            except Exception:
                self.__free_wifi = -1
            try:
                self.__cleanliness = json_text["cleanliness"]
            except Exception:
                self.__cleanliness = -1
            self.__score = json_text["score"]
            try:
                self.__comfort = json_text["comfort"]
            except Exception:
                self.__comfort = -1
            self.__link = str(json_text["link"])
            self.__address = str(json_text["address"])
            self.__popular_facilities = list()
            for item in json_text["popular facilities"]:
                self.__popular_facilities.append(item)
            if 'city' in json_text.keys():
                self.__city = str(json_text["city"])
                self.__check_in = str(json_text["check in"])
                self.__check_out = str(json_text["check out"])
                self.__price = json_text["price"]
                self.__fetch_date = json_text["fetch date"]
            else:
                self.__city = ''
                self.__check_in = ''
                self.__check_out = ''
                self.__price = -1
                self.__fetch_date = ''

    def to_json(self):
        """
        :return dictionary with all attributes
        :rtype: dict
        """
        dict_to_json = {
            "name": self.__name,
            "value for money": self.__value_for_money,
            "staff": self.__staff,
            "facilities": self.__facilities,
            "location": self.__location,
            "free wifi": self.__free_wifi,
            "cleanliness": self.__cleanliness,
            "score": self.__score,
            "comfort": self.__comfort,
            "link": self.__link,
            "address": self.__address,
            "popular facilities": []
        }
        for item in self.__popular_facilities:
            dict_to_json["popular facilities"].append(item)
        if self.__city != '':
            dict_to_json["city"] = self.__city
            dict_to_json["check in"] = self.__check_in
            dict_to_json["check out"] = self.__check_out
            dict_to_json["price"] = self.__price
            dict_to_json["fetch date"] = self.__fetch_date
        return dict_to_json

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
    def fetch_date(self) -> str:
        return self.__fetch_date

    @property
    def city(self) -> str:
        return self.__city

    @property
    def value_for_money(self) -> float:
        return self.__value_for_money

    @property
    def staff(self) -> float:
        return self.__staff

    @property
    def facilities(self) -> float:
        return self.__facilities

    @property
    def location(self) -> float:
        return self.__location

    @property
    def free_wifi(self) -> float:
        return self.__free_wifi

    @property
    def cleanliness(self) -> float:
        return self.__cleanliness

    @property
    def score(self) -> float:
        return self.__score

    @property
    def popular_facilities(self) -> list:
        return self.__popular_facilities

    @property
    def comfort(self) -> float:
        return self.__comfort

    @property
    def link(self) -> str:
        return self.__link

    @property
    def price(self) -> float:
        return self.__price

    def __str__(self):
        return "name: " + str(self.__name) + " city: " + str(self.__city) + "\nscore: " \
               + str(self.__score) + " location: " + str(self.__location) + " price: " \
               + str(self.__price)

    def __repr__(self):
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
