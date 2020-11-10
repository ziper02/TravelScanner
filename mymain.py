from datetime import datetime
import json,os
from Entity.Airport import Airport
import Moderator as mod
from Flights.Utilities import General as flight_general
from Trip import Trip



# flights_data=flight_general.get_all_updated_data()
#
# data_in_range=[flight for flight in flights_data if (flight.days==5 or flight.days==6) and flight.destination_value==5 and  (flight.label==4 or flight.label==3)
#                and datetime.strptime(flight.return_date, '%Y-%m-%d')<datetime(2021,1,1)]
# dict={}
# count=0
# data_in_range.sort()
# trip_list=[]
# for i in range(0,3):
#     flight=data_in_range[i]
#     trip_list.append(Trip(flight))
#
#
# for trip in trip_list:
#     print(trip.pretty_print())
#
