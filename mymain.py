import time
from datetime import datetime
from Trip import Trip
from Flights import general as flight_general
from Hotels import general as hotel_general
import os,json
def test_order_hotel():
    flights_data = flight_general.get_all_updated_data()

    data_in_range = [flight for flight in flights_data if
                     (4 <= flight.days <= 6) and flight.destination_value == 10 and (
                             flight.label == 4 or flight.label == 3)
                     and datetime.strptime(flight.return_date, '%Y-%m-%d') < datetime(2021, 5, 1)]

    data_in_range.sort()
    trip_list = []
    time_start = time.time()
    i = 0
    j = 0
    my_set = set()
    while i < 2:
        flight = data_in_range[j]
        if flight.destination.city not in my_set:
            trip_list.append(Trip(flight))
            my_set.update([flight.destination.city])
            i += 1
        j = j + 1

    for trip in trip_list:
        trip.get_hotel_for_trip()

    trip_list.sort(reverse=True)
    for trip in trip_list:
        print(trip)

    time_end = time.time()
    print((time_end - time_start) / 60)





from Flights import general as flight_general

def fetch_flights_for_site():
    flight_general.fetch_data()
    with open(os.path.dirname(__file__)+"\\Data\\Flights\\most_updated_flights.json",'r',encoding='utf-8') as f:
        flight_list=json.load(f)
    for flight in flight_list:
        keys_temp=[str(key) for key in flight]
        for key in keys_temp:
            flight[key.replace(" ","_")]=flight.pop(key)

    with open(os.path.dirname(__file__)+"\\..\\To Site\\flights.json",'w',encoding='utf-8') as f:
        json.dump(flight_list,f,indent=4)





def to_nisim():

    with open(os.path.dirname(__file__)+"\\Data\\Hotels\\Order Data\\2020-12\\Milano\\2020-12-13_2020-12-18.json",'r',encoding='utf-8') as f:
        data_dict=json.load(f)

    data=[val for key,val in data_dict.items()]

    with open(os.path.dirname(__file__)+"\\toNisimWithPrice.json",'w',encoding='utf-8') as f:
        json.dump(data,f,indent=4)


if __name__ == "__main__":
    #test_order_hotel()
    fetch_flights_for_site()
