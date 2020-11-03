import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from Entity.Flight import Flight
from Utilities import General as general

def get_how_much_flights_per_airport():
    with open(os.path.dirname(__file__) + '/../../Data/Flights/json_files_dict.json', 'r') as f:
        dict = json.load(f)

    count = 0
    for key in dict:
        countList = 0
        for item in dict[key]:
            with open(os.path.dirname(__file__) + "/../../" + item, 'r') as f:
                list = json.load(f)
            countList = countList + len(list)
        print(key + " have " + str(countList))
        count = count + countList
    print("total have " + str(count))


def get_statistic_of_destination(name):
    """
    :param name: The shortcut of the airport
    :return: graph of the airport
    """
    flights_data=general.get_data_by_name(name)
    flights_data_filtered = [flight for flight in flights_data if flight.label != -1]
    flights_days = [
        (datetime.strptime(flight.return_date, '%Y-%m-%d') - datetime.strptime(flight.depart_date, '%Y-%m-%d')).days
        for flight in flights_data]
    flights_price = [flight.price for flight in flights_data]
    flights_label = [flight.label for flight in flights_data]
    very_low_price_x = []
    very_low_price_y = []
    low_price_x = []
    low_price_y = []
    mid_price_x = []
    mid_price_y = []
    high_price_x = []
    high_price_y = []
    unknown_price_x = []
    unknown_price_y = []
    for i in range(len(flights_days)):
        if flights_label[i] == 1:
            high_price_y.append(flights_days[i])
            high_price_x.append(flights_price[i])
        elif flights_label[i] == 2:
            mid_price_y.append(flights_days[i])
            mid_price_x.append(flights_price[i])
        elif flights_label[i] == 3:
            low_price_y.append(flights_days[i])
            low_price_x.append(flights_price[i])
        elif flights_label[i] == 4:
            very_low_price_y.append(flights_days[i])
            very_low_price_x.append(flights_price[i])
        else:
            unknown_price_y.append(flights_days[i])
            unknown_price_x.append(flights_price[i])
    cm = plt.cm.get_cmap('RdYlBu')
    plt.scatter(x=high_price_x, y=high_price_y, label="High", c='Red', s=30)
    plt.scatter(x=mid_price_x, y=mid_price_y, label="Mid", c='Yellow', s=30)
    plt.scatter(x=low_price_x, y=low_price_y, label="Low", c='Green', s=30)
    plt.scatter(x=very_low_price_x, y=very_low_price_y, label="Very Low", c='limegreen', s=30)
    plt.scatter(x=unknown_price_x, y=unknown_price_y, label="Unknown", c='Blue', s=30)
    plt.xlabel('price')
    plt.ylabel('days')
    axes = plt.gca()
    axes.set_ylim([2.5, 7.5])
    axes.set_xlim([110, 1050])
    plt.legend(loc='upper right', fontsize=10, bbox_to_anchor=(1.1, 1.05), fancybox=True)
    plt.show()
    #return low_price_x, low_price_y, mid_price_x, mid_price_y, high_price_x, high_price_y


def get_statistic_of_dest_per_days(name, days):

    with open(os.path.dirname(__file__) +
              '/../../Data/Flights/json_files_dict.json', 'r') as f:
        dict = json.load(f)
    with open(os.path.dirname(__file__) +
              '/../../Data/Flights/airports_countries.json', 'r') as f2:
        shortcut_dict = json.load(f2)
    if name in shortcut_dict:
        fullname_airport = shortcut_dict[name]['airportName']
    else:
        return;
    list = dict[fullname_airport]
    flights_data = []
    for json_file in list:
        with open(os.path.dirname(__file__) + "/../../" + json_file) as f:
            data = json.load(f)
        for temp in data:
            flights_data.append(Flight(**temp))
    flight_list = [flight for flight in flights_data if (datetime.strptime(flight.return_date, '%Y-%m-%d')
                                                         - datetime.strptime(flight.depart_date,
                                                                             '%Y-%m-%d')).days == days]
    flight_list.sort(key=lambda x: x.price)
    print(flight_list[0])

def get_calculated_value_for_location(name):
    """
    :param name: The shortcut of the airport
    :return: get list of flights from airport with calculated value
    """
    flights_data=general.get_data_by_name(name)
    with open(os.path.dirname(__file__) +
              '/../../Data/Flights/calculatedValueForLocation.json', 'r') as f:
        dict_val_for_location = json.load(f)
    val_for_spesifc_location=dict_val_for_location[name]
    filtered_flights_data=[]
    for flight in flights_data:
        days_of_trip=datetime.strptime(flight.return_date, '%Y-%m-%d')-datetime.strptime(flight.depart_date, '%Y-%m-%d')
        if days_of_trip.days>2 and days_of_trip.days<8 and flight.price<2000:
            flight.calculated_value=(flight.price/(days_of_trip.days))*val_for_spesifc_location[str(days_of_trip.days)]
            filtered_flights_data.append(flight)
    return filtered_flights_data


def get_statistic_of_destination_temp(name):
    flights_data=get_calculated_value_for_location(name)
    x = [flight.price for flight in flights_data]
    y = [flight.calculated_value for flight in flights_data]
    plt.scatter(x, y, c="blue")
    #plt.show()
    return x,y