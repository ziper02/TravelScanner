import time
from datetime import datetime
from Trip import Trip
from Flights import general as flight_general


def test_order_hotel():
    flights_data = flight_general.get_all_updated_data()

    data_in_range = [flight for flight in flights_data if
                     (flight.days == 5 or flight.days == 6) and flight.destination_value ==5 and (
                             flight.label == 4 or flight.label == 3)
                     and datetime.strptime(flight.return_date, '%Y-%m-%d') < datetime(2021, 5, 1)]

    data_in_range.sort()
    trip_list = []
    time_start=time.time()
    i=0
    j=0
    my_set=set()
    while i<3:
        flight = data_in_range[j]
        if flight.destination.city not in my_set:
            trip_list.append(Trip(flight))
            my_set.update([flight.destination.city])
            i+=1
        j=j+1


    for trip in trip_list:
        trip.get_hotel_for_trip()

    trip_list.sort(reverse=True)
    for trip in trip_list:
        print(trip)

    time_end=time.time()
    print((time_end-time_start)/60)



if __name__ == "__main__":
    test_order_hotel()
