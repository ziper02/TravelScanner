import requests
from datetime import datetime, timedelta
from tqdm import tqdm, trange
import json

import Moderator
from DataManager import data_manager
from Entity.Airport import Airport
from Entity.Flight import Flight
from Utilities import General

data = data_manager.Wizzair_data_structure
whole_month_url = data_manager.Wizzair_whole_month_request
headers=data_manager.Wizzair_headers

def export_whole_month_all_dest():
    flights_data=fetch_data()
    destinations = Moderator.destination_list_wizzair
    departs=Moderator.depart_list
    for depart in departs:
        depart_flight=Airport(depart)
        t_progress_bar_destination = tqdm(destinations, leave=True)
        for destination in t_progress_bar_destination:
            destination_flight = Airport(destination)
            depart_destination_list = []
            destination_depart_list = []
            t_progress_bar_destination.set_description("Wizzair processing " + destination_flight.name)
            t_progress_bar_destination.refresh()
            for flight_data in flights_data:
                if flight_data["departureStation"]==depart_flight.code and flight_data["arrivalStation"]==destination_flight.code:
                    depart_destination_list.append(flight_data)
                elif flight_data["departureStation"]==destination_flight.code and flight_data["arrivalStation"]==depart_flight.code:
                    destination_depart_list.append(flight_data)
            for flight in depart_destination_list:
                flight["departureDate"]=datetime.strptime(flight["departureDate"][0:10],'%Y-%m-%d')
            for flight in destination_depart_list:
                flight["departureDate"]=datetime.strptime(flight["departureDate"][0:10],'%Y-%m-%d')
            combination_flights=[]
            for item_depart in depart_destination_list:
                for item_return in destination_depart_list:
                    combination_flights.append(Flight(departure=depart_flight,destination=destination_flight,
                                                      depart_date=item_depart["departureDate"],return_date=item_return["departureDate"],
                                                      price=item_depart["price"]["amount"]+item_return["price"]["amount"],
                                                      source="Wizzair"))
            flights_filter=[flight for flight in combination_flights if
                              3 <= (flight.return_date - flight.depart_date).days < 7]
            dict={}
            for flight_item in flights_filter:
                if datetime.strftime(flight_item.depart_date,"%Y-%m") in dict:
                    dict[datetime.strftime(flight_item.depart_date,"%Y-%m")].append(flight_item)
                    flight_item.depart_date = datetime.strftime(flight_item.depart_date, "%Y-%m-%d")
                    flight_item.return_date = datetime.strftime(flight_item.return_date, "%Y-%m-%d")
                else:
                    dict[datetime.strftime(flight_item.depart_date,"%Y-%m")]=[]
                    dict[datetime.strftime(flight_item.depart_date, "%Y-%m")].append(flight_item)
                    flight_item.depart_date=datetime.strftime(flight_item.depart_date,"%Y-%m-%d")
                    flight_item.return_date = datetime.strftime(flight_item.return_date, "%Y-%m-%d")
            for key in dict:
                General.update_json_files(flights=dict[key],year_month_date_depart=key,destination=destination_flight)



def alter_price(flights):
	[flight.update({"priceType": "regular"}) for flight in flights]
	return flights

def fetch_data():
    data_list = []
    base = datetime.today()
    t_progress_bar_destination = trange(6, leave=True)
    for period in t_progress_bar_destination:
        # Only a maximum of 42 days is supported by wizzair.
        data["flightList"][0]["from"] = (base + timedelta(days=period * 42)).strftime("%Y-%m-%d")
        data["flightList"][1]["from"] = (base + timedelta(days=period * 42)).strftime("%Y-%m-%d")
        data["flightList"][0]["to"] = (base + timedelta(days=(period + 1) * 42)).strftime("%Y-%m-%d")
        data["flightList"][1]["to"] = (base + timedelta(days=(period + 1) * 42)).strftime("%Y-%m-%d")
        price_type="regular"
        data["priceType"] = price_type
        destinations=Moderator.destination_list_wizzair
        for destination in destinations:
            t_progress_bar_destination.set_description("Wizzair fetch "+ destination)
            t_progress_bar_destination.refresh()
            data["flightList"][0]["arrivalStation"] = destination
            data["flightList"][1]["departureStation"] = destination
            response = requests.post(whole_month_url, headers=headers,data=json.dumps(data))
            if response.status_code == 200:
                data_list.append(alter_price(response.json()["outboundFlights"]))
                data_list.append(alter_price(response.json()["returnFlights"]))

    flat_list = [item for sublist in data_list for item in sublist]
    return flat_list