# from datetime import datetime
#
#
# from Utilities import General as general
#
# data=general.get_all_updated_data()
# data_in_range=[flight for flight in data if (flight.days==5 or flight.days==6) and flight.destination_value<=25 and  (flight.label==4 or flight.label==3) and  datetime.strptime(flight.depart_date, '%Y-%m-%d')>datetime(2020,11,8) and datetime.strptime(flight.return_date, '%Y-%m-%d')<datetime(2021,3,1)]
# dict={}
# count=0
# for i in range(0,len(data_in_range)):
#     flight=sorted(data_in_range)[i]
#     if flight.destination.code not in dict.keys():
#         print(flight.pretty_print())
#         print()
#         dict[flight.destination.code]='1'
#         count=count+1
#         if count==15:
#             break

import os,json
with open(os.path.dirname(__file__)+"/../Data/Flights/airports.json",'r') as f:
    airports=json.load(f)


with open(os.path.dirname(__file__)+"/../Data/Flights/airports_countries.json","r") as f:
    dict_toupdate=json.load(f)


for key_dict in dict_toupdate.keys():
    for key_airports,value_airports in airports.items():
        if key_dict==value_airports["iata"]:
            dict_toupdate[key_dict]["city"]=value_airports["city"]

with open(os.path.dirname(__file__)+"/../Data/Flights/airports_countries.json",'w',encoding='utf-8') as f:
    json.dump(dict_toupdate,f,indent=4)