from Flights import general as flight_general
from Trip import Trip
import json,os
def test_order_hotel():
    flights_data = flight_general.get_all_updated_data()
    data_in_range = [flight for flight in flights_data if
                     (flight.days == 5 or flight.days == 6) and flight.destination_value <25 and (
                             flight.label == 4 or flight.label == 3)]
    data_in_range.sort()
    trip_list = []
    for i in range(0, 3):
        flight = data_in_range[i]
        trip=Trip(flight)
        trip.get_hotel_for_trip()
        trip_list.append(trip)

    trip_list.sort(reverse=True)
    return trip_list

def export_to_site(list_tochange):
    """
    :param dict_tochange:
    :type dict_tochange: list[Trip]
    """
    list_json=[]
    for item in list_tochange:
        list_json.append(item.to_json())
    for item in list_json:
        key_list=[str(key) for key in item.keys()]
        for key in key_list:
            item[key.replace(" ","_")]=item.pop(key)
    with open("bla.json", 'w', encoding='utf-8') as f:
        json.dump(list_json, f, default=flight_general.obj_dict, indent=4)



