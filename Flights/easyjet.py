import time
from datetime import datetime
from Data import DataManager
import requests
from dateutil.relativedelta import relativedelta
from tqdm import tqdm
import moderator
from DataManager import DataManager
from Entity.Airport import Airport
from Entity.Flight import Flight
from Flights import general

my_blacounter=0
def export_whole_months_all_dest():
    """
    Fetch data from Easyjet.com for all the detentions from TLV,
    and save the data as json in Data\\Flights folder.
    """
    depart_list = [Airport(code=o) for o in moderator.depart_list]
    destination_list = [Airport(code=o) for o in moderator.destination_list_easyjet]
    flights_data = []
    for depart in depart_list:
        t_progress_bar_destination = tqdm(destination_list, leave=True)
        for destination in t_progress_bar_destination:
            t_progress_bar_destination.set_description("EasyJet " + destination.name)
            t_progress_bar_destination.refresh()
            flights_to_dest = export_whole_months(depart=depart, destination=destination)
            if len(flights_to_dest) != 0:
                flights_data.extend(flights_to_dest)
            time.sleep(0.6)
    print(my_blacounter)
    general.update_most_updated_flights(flights_data)


def export_whole_months(depart=None, destination=None):
    """
    Fetch data from Easyjet.com for destination's airport from departure's airport
    :param depart: The airport that the flight depart
    :type depart: Airport
    :param destination: The destination of the flight
    :type destination: Airport
    :return return list of flights from departure airport to destination airport
    :rtype list[Flight]
    """
    global my_blacounter
    whole_month_url = DataManager.Easyjet_whole_month_request
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
        #print(f'EasyJet missing flight to -{destination}')
        return list()
    return_max_date_datetime = datetime.strptime(year_month_day_date_return_str, '%Y-%m-%d')
    flights = []
    flights_data = []
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

                    month_return_str = DataManager.month_dict[potential_day_return.strftime("%m")]
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
                            flight = Flight(flying_out=depart, flying_back=destination,
                                            flying_out_date=selected_date_depart_str,
                                            flying_back_date=selected_date_return_str, price_per_adult=total_price,
                                            source_site='Easyjet')
                            flights.append(flight)
                            my_blacounter = my_blacounter +1
            day_index = day_index + 1
        if len(flights) != 0:
            general.update_json_files(flights=flights, year_month_date_depart=year_month_date_depart,
                                      destination=destination)
            flights_data.extend(flights)
        flights = []
    return flights_data

currency_url = DataManager.currency_conversion.format(src='EUR', dest='ILS')
request_currency = requests.get(url=currency_url)
exchange_rate = request_currency.json()['EUR_ILS']