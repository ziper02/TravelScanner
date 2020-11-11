import time
from datetime import datetime
from Data import data_manager

import requests
from dateutil.relativedelta import relativedelta
from tqdm import tqdm
import moderator
from data_manager import data_manager
from Entity.Airport import Airport
from Entity.Flight import Flight
from Flights import general


def export_whole_months_all_dest():
    """
    Fetch data from Easyjet.com for all the detentions from TLV,
    and save the data as json in Data\\Flights folder.
    """
    depart_list = [Airport(code=o) for o in moderator.depart_list]
    destination_list = [Airport(code=o) for o in moderator.destination_list_easyjet]
    for depart in depart_list:
        t_progress_bar_destination = tqdm(destination_list, leave=True)
        for destination in t_progress_bar_destination:
            t_progress_bar_destination.set_description("EasyJet " + destination.name)
            t_progress_bar_destination.refresh()
            export_whole_months(depart=depart, destination=destination)
            time.sleep(0.6)


def export_whole_months(depart=None, destination=None):
    """
    Fetch data from Easyjet.com for destination's airport from departure's airport
    :param depart: The airport that the flight depart
    :type depart: Airport
    :param destination: The destination of the flight
    :type destination: Airport
    """
    whole_month_url = data_manager.Easyjet_whole_month_request
    currency_url = data_manager.currency_conversion.format(src='EUR', dest='ILS')
    request_currency = requests.get(url=currency_url)
    exchange_rate = request_currency.json()['EUR_ILS']
    date_str = datetime.today().strftime('%Y-%m-%d')
    request_whole_month_url = whole_month_url.format(depart=depart.code, destination=destination.code,
                                                     depart_date=date_str)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.149 Safari/537.36'}
    request = requests.get(url=request_whole_month_url, headers=headers)
    data_depart_hash = request.json()
    request_whole_month_url = whole_month_url.format(depart=destination.code, destination=depart.code,
                                                     depart_date=date_str)
    request = requests.get(url=request_whole_month_url, headers=headers)
    data_return_hash = request.json()
    data_depart = data_depart_hash["months"]
    data_return = data_return_hash["months"]
    try:
        year_month_day_date_return_str = str(
            data_return[len(data_return) - 1]["year"]) + '-' + moderator.month_string_to_number(
            data_return[len(data_return) - 1]["monthDisplayName"]) + '-' \
                                         + str(len(data_return[len(data_return) - 1]['days']))
    except Exception:
        return
    return_max_date_datetime = datetime.strptime(year_month_day_date_return_str, '%Y-%m-%d')
    flights = []
    for month in data_depart:
        year_month_date_depart = str(month["year"]) + '-' + moderator.month_string_to_number(month["monthDisplayName"])
        days = month['days']
        day_index = 0
        for day in days:
            if not day['lowestFare'] is None:
                price_depart = day['lowestFare']
                day_depart = ("0" if (day_index + 1) < 10 else "") + str(day_index + 1)
                selected_date_depart_str = year_month_date_depart + '-' + day_depart
                potential_days_return_list = []
                selected_date_depart_datetime = datetime.strptime(selected_date_depart_str, '%Y-%m-%d')
                for j in range(3, 7):
                    potential_days_return_list.append(selected_date_depart_datetime + relativedelta(days=j))
                for potential_day_return in potential_days_return_list:
                    day_return = int(potential_day_return.strftime("%d")) - 1

                    month_return_str = data_manager.data_manager.month_dict[potential_day_return.strftime("%m")]
                    month_return = 0
                    for return_temp in data_return:
                        if return_temp['monthDisplayName'] == month_return_str:
                            break
                        month_return = month_return + 1

                    selected_date_return_str = datetime.strftime(potential_day_return, '%Y-%m-%d')
                    if potential_day_return < return_max_date_datetime:
                        if not data_return[month_return]['days'][day_return]['lowestFare'] is None:
                            price_return = data_return[month_return]['days'][day_return]['lowestFare']
                            total_price = exchange_rate * (price_depart + price_return)
                            flight = Flight(departure=depart, destination=destination,
                                            depart_date=selected_date_depart_str,
                                            return_date=selected_date_return_str, price=total_price, source='Easyjet')
                            flights.append(flight)
            day_index = day_index + 1
        general.update_json_files(flights=flights, year_month_date_depart=year_month_date_depart,
                                  destination=destination)
        flights = []
