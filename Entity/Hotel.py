class Hotel():

    def __init__(self,name='',city='',value_for_money=-1,staff=-1,facilities=-1
                 ,location=-1,free_wifi=-1,cleanliness=-1,score=-1,popular_facilities=-1,comfort=-1,link=-1,price=-1):
        self._name=name
        self._city=city
        self._value_for_money=value_for_money
        self._staff=staff
        self._facilities=facilities
        self._location=location
        self._free_wifi=free_wifi
        self._cleanliness=cleanliness
        self._score=score
        self._popular_facilities=popular_facilities
        self._comfort=comfort
        self._link=link
        self._price = price


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name=value

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        self._city=value

    @property
    def value_for_money(self):
        return self._value_for_money

    @value_for_money.setter
    def value_for_money(self, value):
        self._value_for_money=value

    @property
    def staff(self):
        return self._staff

    @staff.setter
    def staff(self, value):
        self._staff = value

    @property
    def facilities(self):
        return self._facilities

    @facilities.setter
    def facilities(self, value):
        self._facilities = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def free_wifi(self):
        return self._free_wifi

    @free_wifi.setter
    def free_wifi(self, value):
        self._free_wifi = value

    @property
    def cleanliness(self):
        return self._cleanliness

    @cleanliness.setter
    def cleanliness(self, value):
        self._cleanliness = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def popular_facilities(self):
        return self._popular_facilities

    @popular_facilities.setter
    def popular_facilities(self, value):
        self._popular_facilities = value

    @property
    def comfort(self):
        return self._comfort

    @comfort.setter
    def comfort(self, value):
        self._comfort = value

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

