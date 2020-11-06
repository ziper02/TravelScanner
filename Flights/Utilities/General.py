import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import re
import Moderator
from Entity.Airport import Airport
from Entity.Flight import Flight
from Utilities import Statistics as statistics


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



def get_data_by_name(name):
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
            flights_data.append(Flight(**temp))
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
    date_list_re = [re.search(r'\d{4}-\d{2}-\d{2}', item) for item in list]
    date_list = [datetime.strptime(match.group(), '%Y-%m-%d').date() for match in date_list_re]
    max_date = max(date_list).strftime("%Y-%m-%d")
    updated_data_lst = [item for item in list if max_date in item]
    flights_data = []
    for json_file in updated_data_lst:
        with open(os.path.dirname(__file__) + "/../../" + json_file) as f:
            data = json.load(f)
        for temp in data:
            flights_data.append(Flight(**temp))
    return flights_data

