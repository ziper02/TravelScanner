from datetime import datetime

from Entity.Airport import Airport


class Flight:

    def __init__(self, departure=None, destination=None, depart_date=None, return_date=None, price=None,
                 source=None,label=-1,set=-1,**dict):
        if departure!=None:
            self._departure = departure
            self._destination = destination
            self._depart_date = depart_date
            self._return_date = return_date
            self._price = price
            self._label = label
            self._source = source
            self._set=set
            self._calculated_value=-1

        else:
            self.__dict__.update(dict)
            self._destination=Airport(dict=dict["_destination"])
            self._departure = Airport(dict=dict["_departure"])


    @classmethod
    def filter_list_of_flights(cls,flights):
        for flight in flights:
            if flight.label== -1:
                if isinstance(flight.depart_date,str):
                    depart_date_temp = datetime.strptime(flight.depart_date, '%Y-%m-%d')
                else:
                    depart_date_temp=flight.depart_date
                if isinstance(flight.return_date,str):
                    return_date_temp = datetime.strptime(flight.return_date, '%Y-%m-%d')
                else:
                    return_date_temp=flight.return_date
                delta=return_date_temp-depart_date_temp
                if delta.days>7 or delta.days<3:
                    flight.label=1
                elif flight.price>1050:
                    flight.label=1

    def __eq__(self, other):
        if isinstance(other, Flight):
            if self._depart_date == other._depart_date and self._departure == other._departure \
                    and self._destination == other._destination and self._return_date == other._return_date \
                    and self._price == other._price:
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "Flight:: departure:  " + str(self._departure) + "\ndestination:  " + str(self._destination) + \
               "\ndepart date:  " + str(self._depart_date) + " return date:  " + str(self._return_date) + \
               "\nprice:  " + str(self._price) + " label:  " + str(self._label)

    @property
    def departure(self):
        return self._departure

    @property
    def destination(self):
        return self._destination

    @property
    def depart_date(self):
        return self._depart_date

    @property
    def return_date(self):
        return self._return_date


    @return_date.setter
    def return_date(self, value):
        self._return_date = value


    @depart_date.setter
    def depart_date(self, value):
        self._depart_date = value

    @property
    def price(self):
        return self._price

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def calculated_value(self):
        return self._calculated_value


    @calculated_value.setter
    def calculated_value(self, value):
        self._calculated_value = value