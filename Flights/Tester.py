import json

from Hotels import general as hotel_general
from Flights import general as flight_general

hotels_data = hotel_general.get_all_location_data(with_json_file=True)
counter = 0
write_back_data = []
for hotel, json_file in hotels_data:
    if hotel.link != '':
        counter+=1

print(len(hotels_data))
print(counter)


flights_data=flight_general.get_all_updated_data()
count=0
dest=set()
for flight in flights_data:
    if flight.label==-1:
        dest.update([flight.destination.city])
        count=count+1

print(count)