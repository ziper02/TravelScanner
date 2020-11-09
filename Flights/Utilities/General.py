import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import re
import Moderator
from Entity.Airport import Airport
from Entity.Flight import Flight


def update_json_files(flights, year_month_date_depart, destination):
    if len(flights) != 0:
        file_name = datetime.today().strftime('%Y-%m-%d')
        dest_all_for_name = Airport(Moderator.transfer_airport_cod_names_to_all(destination.code))
        Path(os.path.dirname(__file__) + '/../../Data/Flights/Whole Month/' + year_month_date_depart).mkdir(
            parents=True,
            exist_ok=True)
        Path(os.path.dirname(
            __file__) + '/../../Data/Flights/Whole Month/' + year_month_date_depart + '/' + dest_all_for_name.name).mkdir(
            parents=True, exist_ok=True)
        my_file = Path(
            os.path.dirname(__file__) + '/../../Data/Flights/Whole Month/' + year_month_date_depart + '/' +
            dest_all_for_name.name + '/' + file_name + ' ' + dest_all_for_name.name + ' ' + year_month_date_depart + ".json")
        append_data_flights = []
        if my_file.is_file():
            with open(
                    os.path.dirname(
                        __file__) + '/../../Data/Flights/Whole Month/' + year_month_date_depart + '/' +
                    dest_all_for_name.name + '/' + file_name + ' ' + dest_all_for_name.name + ' ' + year_month_date_depart + ".json",
                    'r',
                    encoding='utf-8') as f:
                append_data_flights = json.load(f)
        flights = flights + append_data_flights
        with open(
                os.path.dirname(__file__) + '/../../Data/Flights/Whole Month/' + year_month_date_depart + '/' +
                dest_all_for_name.name + '/' + file_name + ' ' + dest_all_for_name.name + ' ' + year_month_date_depart + ".json",
                'w',
                encoding='utf-8') as f:
            json.dump(flights, f, ensure_ascii=False, default=obj_dict, indent=4)

        with open(os.path.dirname(__file__) + '/../../Data/Flights/json_files.json', 'r',
                  encoding='utf-8') as f:
            append_data = json.load(f)
        json_str = '/Data/Flights/Whole Month/' + year_month_date_depart + '/' + \
                   dest_all_for_name.name + '/' + file_name + ' ' + dest_all_for_name.name + ' ' + year_month_date_depart + '.json'
        append_data.append(json_str)
        append_data = list(set(append_data))
        with open(os.path.dirname(__file__) + '/../../Data/Flights/json_files.json', 'w',
                  encoding='utf-8') as f:
            json.dump(append_data, f, ensure_ascii=False, default=obj_dict, indent=4)
        add_to_json_dict(json_str)


def obj_dict(obj):
    return obj.__dict__


def add_to_json_dict(json_file):
    with open(os.path.dirname(__file__) + '/../../Data/Flights/json_files_dict.json', 'r') as f:
        dict = json.load(f)
        if len(dict) == 0:
            dict = defaultdict(list)
        bool = True
        for dest in Moderator.destination_list_easyjet:
            name = Airport(Moderator.transfer_airport_cod_names_to_all(Airport(dest).code)).name
            if name in json_file:
                if name in dict:
                    dict[name].append(json_file)
                    dict[name] = list(set(dict[name]))
                else:
                    dict[name] = []
                    dict[name].append(json_file)
                    dict[name] = list(set(dict[name]))
                bool = False
        if bool:
            for dest in Moderator.destination_list_skyscanner:
                name = Airport(Moderator.transfer_airport_cod_names_to_all(Airport(dest).code)).name
                if name in json_file:
                    if name in dict:
                        dict[name].append(json_file)
                        dict[name] = list(set(dict[name]))
                    else:
                        dict[name] = []
                        dict[name].append(json_file)
                        dict[name] = list(set(dict[name]))
                    bool = False
        if bool:
            for dest in Moderator.destination_list_wizzair:
                name = Airport(Moderator.transfer_airport_cod_names_to_all(Airport(dest).code)).name
                if name in json_file:
                    if name in dict:
                        dict[name].append(json_file)
                        dict[name] = list(set(dict[name]))
                    else:
                        dict[name] = []
                        dict[name].append(json_file)
                        dict[name] = list(set(dict[name]))

    with open(os.path.dirname(__file__) + '/../../Data/Flights/json_files_dict.json', 'w', encoding='utf-8') as f:
        json.dump(dict, f, ensure_ascii=False, indent=4)



def get_data_by_name(name,add_json_file=False):
    """
    :param name: The shortcut of the airport
    :return: list of all flights of destention
    """
    with open(os.path.dirname(__file__) +
              '/../../Data/Flights/json_files_dict.json', 'r') as f:
        dict = json.load(f)
    with open(os.path.dirname(__file__) +
              '/../../Data/Flights/airports_countries.json', 'r') as f2:
        shortcut_dict = json.load(f2)
    if name in shortcut_dict:
        fullname_airport = shortcut_dict[Moderator.transfer_airport_cod_names_to_all(name)]['airportName']
    else:
        return;
    list = dict[fullname_airport]
    flights_data = []
    for json_file in list:
        with open(os.path.dirname(__file__) + "/../../" + json_file) as f:
            data = json.load(f)
        for temp in data:
            if not add_json_file:
                flights_data.append(Flight(**temp))
            else:
                flights_data.append((Flight(**temp),json_file))
    return flights_data


def get_updated_data_by_name(name):
    """
    :param name: The shortcut of the airport
    :return: list of updated flights of destention
    """
    with open(os.path.dirname(__file__) +
              '/../../Data/Flights/json_files_dict.json', 'r') as f:
        dict = json.load(f)
    with open(os.path.dirname(__file__) +
              '/../../Data/Flights/airports_countries.json', 'r') as f2:
        shortcut_dict = json.load(f2)
    if name in shortcut_dict:
        fullname_airport = shortcut_dict[Moderator.transfer_airport_cod_names_to_all(name)]['airportName']
    else:
        return;
    list = dict[fullname_airport]
    today_date = datetime.today().strftime('%Y-%m-%d')
    updated_data_lst = [item for item in list if today_date in item]
    flights_data = []
    for json_file in updated_data_lst:
        with open(os.path.dirname(__file__) + "/../../" + json_file) as f:
            data = json.load(f)
        for temp in data:
            flights_data.append(Flight(**temp))
    return flights_data

def get_all_updated_data():
    with open(os.path.dirname(__file__)+"/../../Data/Flights/dict_rate_dest.json",'r') as f:
        rate_dest=json.load(f)
    flight_data=[]
    for dest_key in rate_dest.keys():
        flight_data.extend(get_updated_data_by_name(dest_key))
    return flight_data


def update_json_dest_by_list(flight_data):
    """
    :param flight_data: list of tuples with all destination's flight (flight,json_file)
    :return: update the files
    """
    json_dict={}
    for flight,json_file in flight_data:
        if json_file not in json_dict.keys():
            json_dict[json_file]=list()
            json_dict[json_file].append(flight)
        else:
            json_dict[json_file].append(flight)
    for json_file,flights_list in json_dict.items():
        with open(os.path.dirname(__file__)+"/../../"+json_file,'w',encoding='utf-8') as f:
            json.dump(flights_list,f,ensure_ascii=False,default=obj_dict,indent=4)

def label_all_flights_by_price_range():
    """
    :return: label all the data by the price_range json
    """
    with open(os.path.dirname(__file__)+"/../../Data/Flights/dict_price_range.json",'r',encoding="utf-8") as f:
        dict_price_range=json.load(f)
    for dest_key,dest_value in dict_price_range.items():
        dest_price_range=dict_price_range[dest_key]
        flights_data=get_data_by_name(dest_key,add_json_file=True)
        for flight_item in flights_data:
            flight=flight_item[0]
            flight.__dict__.pop('_set', None)
            if flight.days < 3 or flight.days > 7:
                flight.label = 0
                flight.data_set="Train"
                continue
            dest_price_range_days=dest_price_range[str(flight.days)]
            for label_key,label_value in dest_price_range_days.items():
                low_price=float(re.split("-",label_value)[0])
                high_price = float(re.split("-", label_value)[1])
                if label_key=="very low price range" and low_price>flight.price:
                    flight.label=4
                elif label_key=="high price range" and high_price<flight.price:
                    flight.label=1
                elif flight.price>= low_price and flight.price<=high_price:
                    if label_key=="very low price range":
                        flight.label=4
                    elif label_key=="low price range":
                        flight.label=3
                    elif label_key=="mid price range":
                        flight.label=2
                    else:
                        flight.label=1
                flight.data_set = "Train"
        update_json_dest_by_list(flight_data=flights_data)

def label_flight_by_price_range(flight):
    with open(os.path.dirname(__file__)+"/../../Data/Flights/dict_price_range.json",'r',encoding="utf-8") as f:
        dict_price_range=json.load(f)

def get_list_of_all_destinations():
    airports_code=set()
    airports_code.update(Moderator.destination_list_wizzair)
    airports_code.update(Moderator.destination_list_skyscanner)
    airports_code.update(Moderator.destination_list_easyjet)
    airports=[]
    for airport_code in airports_code:
        airports.append(Airport(Moderator.transfer_airport_cod_names_to_all(airport_code)))
    return airports