import os
import time
from datetime import datetime
from pathlib import Path
import requests
from dateutil.relativedelta import relativedelta
import moderator
from DataManager import DataManager
from Entity.Airport import Airport
from Entity.Flight import Flight
from tqdm import tqdm

from Flights import general

def export_whole_month_all_dest():
    """
    Fetch data from SkyScanner.com for all the detentions from TLV,
    and save the data as json in Data\\Flights folder.
    """
    date_selected = datetime.today()
    dates = []
    flight_data = []
    depart_list = [Airport(code=o) for o in moderator.depart_list]
    destination_list = [Airport(code=o) for o in moderator.destination_list_skyscanner]
    for i in range(11):
        dates.append(date_selected)
        date_selected = date_selected + relativedelta(months=1)
    t_progress_bar_destination = tqdm(dates, leave=True)
    for date in t_progress_bar_destination:
        for depart in depart_list:
            for destination in destination_list:
                t_progress_bar_destination.set_description(
                    "SkyScanner " + date.strftime('%Y-%m') + " " + destination.name)
                t_progress_bar_destination.refresh()
                flight_to_dest = export_whole_month(depart=depart,
                                                    destination=destination, date=date)
                if len(flight_to_dest) != 0:
                    flight_data.extend(flight_to_dest)
                time.sleep(0.6)
    general.update_most_updated_flights(flight_data)


def export_whole_month(depart=None, destination=None, date=None):
    """
    Fetch data from SkyScanner.com for destination's airport from departure's airport of the selected month
    :param depart: The airport that the flight depart
    :type depart: Airport
    :param destination: The destination of the flight
    :type destination: Airport
    :param date: Date of the required month for fetch
    :type date: datetime
    :return list of flights of this month
    :rtype: list[Flight]
    """
    selected_month = date.strftime('%Y-%m')
    Path(os.path.dirname(__file__) + '/../../Data/Flights/Whole Month/' + selected_month).mkdir(parents=True,
                                                                                                exist_ok=True)
    Path(
        os.path.dirname(__file__) + '/../../Data/Flights/Whole Month/' + selected_month + '/' + destination.name).mkdir(
        parents=True, exist_ok=True)
    request_whole_month_url = DataManager.SkyScanner_whole_month_request.format(depart=depart.code,
                                                                                destination=destination.code,
                                                                                selected_month=selected_month)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
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
                flight = Flight(flying_out=depart, flying_back=destination, flying_out_date=depart_date,
                                flying_back_date=return_date, price_per_adult=price, source_site="SkyScanner")
                flights.append(flight)
            j = j + 1
        i = i + 1
    general.update_json_files(flights=flights, year_month_date_depart=selected_month, destination=destination)
    return flights
