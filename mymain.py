
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

from Entity.Flight import Flight
from Flights import general
from Entity.Hotel import Hotel
import os,json


with open(os.path.dirname(__file__)+"/Data/Hotels/Locations Data/Berlin.json",'r',encoding='utf-8') as f:
    data:dict=json.load(f)

hotels_data=[]
for temp in data.keys():
    dict_hotel=data[temp]
    hotels_data.append(Hotel(**dict_hotel))

with open(os.path.dirname(__file__)+"/Data/test.json",'w',encoding='utf-8') as f:
    json.dump(hotels_data,f,default=general.obj_dict,indent=4)