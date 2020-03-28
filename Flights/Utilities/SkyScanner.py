import json
import os
import time
from datetime import datetime
from pathlib import Path
import requests
from dateutil.relativedelta import relativedelta
import Moderator
from DataManager import data_manager
from Entity.Airport import Airport
from Entity.Flight import Flight
from collections import defaultdict

whole_month_url = data_manager.SkyScanner_whole_month_request


def export_whole_month_all_dest():
    date_selected = datetime.today()
    dates = []
    depart_list=[Airport(code=o) for o in Moderator.depart_list]
    destination_list=[Airport(code=o) for o in Moderator.destination_list_skyscanner]
    for i in range(11):
        dates.append(date_selected)
        date_selected = date_selected + relativedelta(months=1)
    for date in dates:
        for depart in depart_list:
            for destination in destination_list:
                export_whole_month(depart=depart, destination=destination, date=date)
                time.sleep(0.6)


def export_whole_month(depart=None, destination=None, date=None):
    selected_month = date.strftime('%Y-%m')
    Path(os.path.dirname(__file__) + '/../../Data/Flights/Whole Month/' + selected_month).mkdir(parents=True, exist_ok=True)
    Path(os.path.dirname(__file__) + '/../../Data/Flights/Whole Month/' + selected_month + '/' + destination.name).mkdir(
        parents=True, exist_ok=True)
    request_whole_month_url = whole_month_url.format(depart=depart.code, destination=destination.code,
                                                     selected_month=selected_month)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    request = requests.get(url=request_whole_month_url, headers=headers)
    data_hash = request.json()
    data = data_hash["PriceGrids"]["Grid"]
    flights = []
    i = 0
    for list_i in data:
        j = 0
        for dict_j in list_i:
            if "Direct" in dict_j.keys():
                price = dict_j["Direct"]["Price"]
                day_depart = ("0" if (j + 1) < 10 else "") + str(j + 1)
                day_return = ("0" if (i + 1) < 10 else "") + str(i + 1)
                depart_date = selected_month + '-' + day_depart
                return_date = selected_month + '-' + day_return
                flight = Flight(departure=depart, destination=destination, depart_date=depart_date,
                                return_date=return_date, price=price,source="SkyScanner")
                flights.append(flight)
            j = j + 1
        i = i + 1
    if len(flights) != 0:
        file_name = datetime.today().strftime('%Y-%m-%d')
        my_file = Path(os.path.dirname(__file__) + '/../../Data/Flights/Whole Month/' + selected_month + '/' +
                  destination.name + '/' + file_name + ' ' + destination.name + ' ' + selected_month + ".json")
        append_data_flights=[]
        if my_file.is_file():
            with open(os.path.dirname(__file__) + '/../../Data/Flights/Whole Month/' + selected_month + '/' +
                      destination.name + '/' + file_name + ' ' + destination.name + ' ' + selected_month + ".json", 'r',
                      encoding='utf-8') as f:
                append_data_flights = json.load(f)
        flights=flights+append_data_flights
        with open(os.path.dirname(__file__) + '/../../Data/Flights/Whole Month/' + selected_month + '/' +
                  destination.name + '/' + file_name + ' ' + destination.name + ' ' + selected_month + ".json", 'w',
                  encoding='utf-8') as f:
            json.dump(flights, f, ensure_ascii=False, default=obj_dict, indent=4)

        with open(os.path.dirname(__file__) + '/../../Data/Flights/json_files.json', 'r',encoding='utf-8') as f:
            append_data=json.load(f)
        json_str = '/Data/Flights/Whole Month/' + selected_month + '/' + \
                   destination.name + '/' + file_name + ' ' + destination.name + ' ' + selected_month + '.json'
        append_data.append(json_str)
        with open(os.path.dirname(__file__) + '/../../Data/Flights/json_files.json', 'w',encoding='utf-8') as f:
            json.dump(append_data, f, ensure_ascii=False, default=obj_dict, indent=4)
        add_to_json_dict(json_str)
        print('Finished: '+ file_name + ' ' + destination.name + ' ' + selected_month + ".json")


def add_to_json_dict(json_file):
    with open(os.path.dirname(__file__) + '/../../Data/Flights/json_files_dict.json', 'r') as f:
        dict = json.load(f)
        if len(dict)==0:
            dict=defaultdict(list)
        if "London" in json_file:
            if 'London' in dict.keys():
                dict["London"].append(json_file)
            else:
                dict["London"]=[]
                dict["London"].append(json_file)
        elif "Prague" in json_file:
            if 'Prague' in dict.keys():
                dict["Prague"].append(json_file)
            else:
                dict["Prague"]=[]
                dict["Prague"].append(json_file)
        elif "Geneva" in json_file:
            if 'Geneva' in dict.keys():
                dict["Geneva"].append(json_file)
            else:
                dict["Geneva"]=[]
                dict["Geneva"].append(json_file)
        elif "Schiphol" in json_file:
            if 'Amsterdam' in dict.keys():
                dict["Amsterdam"].append(json_file)
            else:
                dict["Amsterdam"]=[]
                dict["Amsterdam"].append(json_file)
        elif "Barajas" in json_file:
            if 'Madrid' in dict.keys():
                dict["Madrid"].append(json_file)
            else:
                dict["Madrid"]=[]
                dict["Madrid"].append(json_file)
        elif "Franz-Josef-Strauss" in json_file:
            if 'Munich' in dict.keys():
                dict["Munich"].append(json_file)
            else:
                dict["Munich"]=[]
                dict["Munich"].append(json_file)
        elif "Berlin" in json_file:
            if 'Berlin' in dict.keys():
                dict["Berlin"].append(json_file)
            else:
                dict["Berlin"]=[]
                dict["Berlin"].append(json_file)
        elif "Manchester" in json_file:
            if 'Manchester' in dict.keys():
                dict["Manchester"].append(json_file)
            else:
                dict["Manchester"]=[]
                dict["Manchester"].append(json_file)
        elif "Ferihegy" in json_file:
            if 'Budapest' in dict.keys():
                dict["Budapest"].append(json_file)
            else:
                dict["Budapest"]=[]
                dict["Budapest"].append(json_file)
        elif "Zurich" in json_file:
            if 'Zurich' in dict.keys():
                dict["Zurich"].append(json_file)
            else:
                dict["Zurich"]=[]
                dict["Zurich"].append(json_file)
        elif "Barcelona" in json_file:
            if 'Barcelona' in dict.keys():
                dict["Barcelona"].append(json_file)
            else:
                dict["Barcelona"]=[]
                dict["Barcelona"].append(json_file)
        elif "Paris" in json_file:
            if 'Paris' in dict.keys():
                dict["Paris"].append(json_file)
            else:
                dict["Paris"]=[]
                dict["Paris"].append(json_file)
        elif "Bourgas" in json_file:
            if 'Bourgas' in dict.keys():
                dict["Bourgas"].append(json_file)
            else:
                dict["Bourgas"]=[]
                dict["Bourgas"].append(json_file)
        elif "Topoli" in json_file:
            if 'Varna' in dict.keys():
                dict["Varna"].append(json_file)
            else:
                dict["Varna"]=[]
                dict["Varna"].append(json_file)
        elif "Milano" in json_file:
            if 'Milano' in dict.keys():
                dict["Milano"].append(json_file)
            else:
                dict["Milano"]=[]
                dict["Milano"].append(json_file)
        elif "Vrazhdebna" in json_file:
            if 'Sofia' in dict.keys():
                dict["Sofia"].append(json_file)
            else:
                dict["Sofia"]=[]
                dict["Sofia"].append(json_file)
        elif "Thessaloniki" in json_file:
            if 'Thessaloniki' in dict.keys():
                dict["Thessaloniki"].append(json_file)
            else:
                dict["Thessaloniki"]=[]
                dict["Thessaloniki"].append(json_file)
        elif "Dublin" in json_file:
            if 'Dublin' in dict.keys():
                dict["Dublin"].append(json_file)
            else:
                dict["Dublin"]=[]
                dict["Dublin"].append(json_file)
        elif "Lisbon" in json_file:
            if 'Lisbon' in dict.keys():
                dict["Lisbon"].append(json_file)
            else:
                dict["Lisbon"]=[]
                dict["Lisbon"].append(json_file)
        elif "Belgrade" in json_file:
            if 'Belgrade' in dict.keys():
                dict["Belgrade"].append(json_file)
            else:
                dict["Belgrade"]=[]
                dict["Belgrade"].append(json_file)
    with open(os.path.dirname(__file__) + '/../../Data/Flights/json_files_dict.json', 'w', encoding='utf-8') as f:
        json.dump(dict, f, ensure_ascii=False, indent=4)


def filter_json_flights():
    with open(os.path.dirname(__file__) + '/../../Data/Flights/Whole Month/json_files.json') as f:
        json_files = json.load(f)
    for json_file in json_files:
        flights_data = []
        with open(os.path.dirname(__file__)+ json_file) as f:
            data = json.load(f)
        for temp in data:
            flights_data.append(Flight(**temp))
        Flight.filter_list_of_flights(flights_data)
        with open(os.path.dirname(__file__) +json_file,'w',encoding='utf-8') as f:
            json.dump(flights_data, f, ensure_ascii=False, default=obj_dict, indent=4)

def obj_dict(obj):
    return obj.__dict__
