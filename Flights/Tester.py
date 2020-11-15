import time
from datetime import datetime
from Trip import Trip
from Flights import general as flight_general


def test_order_hotel():
    flights_data = flight_general.get_all_updated_data()

    data_in_range = [flight for flight in flights_data if
                     (flight.days == 5 or flight.days == 6) and flight.destination_value <25 and (
                             flight.label == 4 or flight.label == 3)
                     and datetime.strptime(flight.return_date, '%Y-%m-%d') < datetime(2021, 1, 1)]

    data_in_range.sort()
    trip_list = []
    time_start=time.time()
    for i in range(26, 27):
        flight = data_in_range[i]
        trip_list.append(Trip(flight))

    trip_list.sort(reverse=True)
    for trip in trip_list:
        print(trip)

    time_end=time.time()
    print((time_end-time_start)/60)



if __name__ == "__main__":
    #flight_general.label_all_flights_by_price_range()
    test_order_hotel()
