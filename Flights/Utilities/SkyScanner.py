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

whole_month_url = data_manager.SkyScanner_whole_month_request


def export_whole_month_all_dest():
    date_selected = datetime.today()
    dates = []
    depart_list=[Airport(code=o) for o in Moderator.depart_list]
    destination_list=[Airport(code=o) for o in Moderator.destination_list]
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
    Path(os.path.dirname(__file__) + '/../Data/Whole Month/' + selected_month).mkdir(parents=True, exist_ok=True)
    Path(os.path.dirname(__file__) + '/../Data/Whole Month/' + selected_month + '/' + destination.name).mkdir(
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
                                return_date=return_date, price=price)
                flights.append(flight)
            j = j + 1
        i = i + 1
    if len(flights) != 0:
        file_name = date.strftime('%Y-%m-%d')
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
        json_str = '/../Flights/Data/Whole Month/' + selected_month + '/' + \
                   destination.name + '/' + file_name + ' ' + destination.name + ' ' + selected_month + '.json'
        append_data.append(json_str)
        with open(os.path.dirname(__file__) + '/../../Data/Flights/json_files.json', 'w',encoding='utf-8') as f:
            json.dump(append_data, f, ensure_ascii=False, default=obj_dict, indent=4)


        print('Finished: '+ file_name + ' ' + destination.name + ' ' + selected_month + ".json")

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