import re

import requests
from datetime import datetime, timedelta
from tqdm import tqdm, trange
import json
import moderator
from DataManager import DataManager
from Entity.Airport import Airport
from Entity.Flight import Flight
from Flights import general


def export_whole_month_all_dest():
    """
    Fetch data from Wizzair.com for all the detentions from TLV,
    parse him to Flight format and save the data as json in Data\\Flights folder.
    """
    flights_data = fetch_data()
    destinations = moderator.destination_list_wizzair
    departs = moderator.depart_list
    flights_data_most_updated = []
    for depart in departs:
        depart_flight = Airport(depart)
        t_progress_bar_destination = tqdm(destinations, leave=True)
        for destination in t_progress_bar_destination:
            destination_flight = Airport(destination)
            depart_destination_list = []
            destination_depart_list = []
            t_progress_bar_destination.set_description("Wizzair processing " + destination_flight.name)
            t_progress_bar_destination.refresh()
            for flight_data in flights_data:
                if flight_data["departureStation"] == depart_flight.code and \
                        flight_data["arrivalStation"] == destination_flight.code:
                    depart_destination_list.append(flight_data)
                elif flight_data["departureStation"] == destination_flight.code \
                        and flight_data["arrivalStation"] == depart_flight.code:
                    destination_depart_list.append(flight_data)
            for flight in depart_destination_list:
                flight["departureDate"] = flight["departureDate"][0:10]
            for flight in destination_depart_list:
                flight["departureDate"] = flight["departureDate"][0:10]
            combination_flights = []
            for item_depart in depart_destination_list:
                for item_return in destination_depart_list:
                    combination_flights.append(Flight(flying_out=depart_flight, flying_back=destination_flight,
                                                      flying_out_date=item_depart["departureDate"],
                                                      flying_back_date=item_return["departureDate"],
                                                      price_per_adult=item_depart["price"]["amount"] + item_return
                                                      ["price"]["amount"], source_site="Wizzair"))
            flights_filter = [flight for flight in combination_flights if
                              3 <= flight.days < 7]
            flights_per_year_month_dict = {}
            if len(flights_filter) != 0:
                flights_data_most_updated.extend(flights_filter)
            for flight_item in flights_filter:
                depart_date_dt = datetime.strptime(flight_item.depart_date, '%Y-%m-%d')
                if datetime.strftime(depart_date_dt, "%Y-%m") in flights_per_year_month_dict:
                    flights_per_year_month_dict[datetime.strftime(depart_date_dt, "%Y-%m")].append(flight_item)
                else:
                    flights_per_year_month_dict[datetime.strftime(depart_date_dt, "%Y-%m")] = []
                    flights_per_year_month_dict[datetime.strftime(depart_date_dt, "%Y-%m")].append(flight_item)

            # update json files
            for key in flights_per_year_month_dict:
                general.update_json_files(flights=flights_per_year_month_dict[key],
                                          year_month_date_depart=key, destination=destination_flight)
    general.update_most_updated_flights(flights_data_most_updated)


def alter_price(flights):
    [flight.update({"priceType": "regular"}) for flight in flights]
    return flights


def fetch_data():
    """
    Send GET request to Wizzair.com in the required format for all destinations
    :rtype: list[str]
    :return:data of all destination's flights
    """
    data = DataManager.Wizzair_data_structure
    data_list = []
    base = datetime.today()
    t_progress_bar_destination = trange(6, leave=True)
    for period in t_progress_bar_destination:
        # Only a maximum of 42 days is supported by wizzair.
        data["flightList"][0]["from"] = (base + timedelta(days=period * 42)).strftime("%Y-%m-%d")
        data["flightList"][1]["from"] = (base + timedelta(days=period * 42)).strftime("%Y-%m-%d")
        data["flightList"][0]["to"] = (base + timedelta(days=(period + 1) * 42)).strftime("%Y-%m-%d")
        data["flightList"][1]["to"] = (base + timedelta(days=(period + 1) * 42)).strftime("%Y-%m-%d")
        price_type = "regular"
        data["priceType"] = price_type
        destinations = moderator.destination_list_wizzair
        for destination in destinations:
            t_progress_bar_destination.set_description("Wizzair fetch " + destination)
            t_progress_bar_destination.refresh()
            data["flightList"][0]["arrivalStation"] = destination
            data["flightList"][1]["departureStation"] = destination
            url_request_get = DataManager.Wizzair_whole_month_request.format(api_version=get_current_wizzair_api())
            response = requests.post(url_request_get,
                                     headers=DataManager.Wizzair_headers, data=json.dumps(data))
            if response.status_code == 200:
                data_list.append(alter_price(response.json()["outboundFlights"]))
                data_list.append(alter_price(response.json()["returnFlights"]))

    flat_list = [item for sublist in data_list for item in sublist]
    return flat_list


def get_current_wizzair_api():
    """
    get the current api version of wizzair
    :return: api version
    :rtype: str
    """
    url_request_wizzair_api_version = DataManager.url_request_wizzair_api_version
    request_wizzair_api = requests.get(url=url_request_wizzair_api_version)
    api_version = re.search(r' https://be.wizzair.com/(.*?) ', request_wizzair_api.text).group(1).replace(' ', '')
    return api_version
