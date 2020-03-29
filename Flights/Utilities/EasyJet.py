import time
from datetime import datetime
from pathlib import Path

import requests
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

import Moderator
from DataManager import data_manager
from Entity.Airport import Airport
from Entity.Flight import Flight
from Moderator import month_string_to_number
from MyScanner import Scanner as sc
import os
import json

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from TelegramBot import bot
import sys

from Utilities import SkyScanner, General

locations = ('Amsterdam', 'London Stansted', 'Berlin Schoenefeld', 'Berlin Tegal', 'Geneva', 'London Gatwick',
             'London Luton', 'Lyon', 'Manchester', 'Milan Malpensa', 'Paris Charles de Gaulle (CDG)')

whole_month_url = data_manager.Easyjet_whole_month_request

currency_url = data_manager.currency_conversion.format(src='EUR',dest='ILS')
request_currency = requests.get(url=currency_url)
exchange_rate=request_currency.json()['EUR_ILS']

def export_whole_months_all_dest():
    depart_list=[Airport(code=o) for o in Moderator.depart_list]
    destination_list=[Airport(code=o) for o in Moderator.destination_list_easyjet]
    for depart in depart_list:
        t_progress_bar_destination = tqdm(destination_list, leave=True)
        for destination in t_progress_bar_destination:
            t_progress_bar_destination.set_description("EasyJet " + destination.name)
            t_progress_bar_destination.refresh()
            export_whole_months(depart=depart, destination=destination)
            time.sleep(0.6)


def export_whole_months(depart=None, destination=None):
    date_str = datetime.today().strftime('%Y-%m-%d')
    request_whole_month_url = whole_month_url.format(depart=depart.code, destination=destination.code,
                                                     depart_date=date_str)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    request = requests.get(url=request_whole_month_url, headers=headers)
    data_depart_hash = request.json()
    request_whole_month_url = whole_month_url.format(depart=destination.code, destination=depart.code,
                                                     depart_date=date_str)
    request = requests.get(url=request_whole_month_url, headers=headers)
    data_return_hash = request.json()
    data_depart = data_depart_hash["months"]
    data_return = data_return_hash["months"]
    year_month_day_date_return_str = str(data_return[len(data_return)-1]["year"]) + '-' + month_string_to_number(data_return[len(data_return)-1]["monthDisplayName"])+ '-' \
                                 + str(len(data_return[len(data_return)-1]['days']))
    return_max_date_datetime = datetime.strptime(year_month_day_date_return_str, '%Y-%m-%d')
    flights=[]
    for month in data_depart:
        year_month_date_depart = str(month["year"]) + '-' + month_string_to_number(month["monthDisplayName"])
        days = month['days']
        dayIndex = 0
        for day in days:
            if not day['lowestFare'] is None:
                price_depart=day['lowestFare']
                day_depart = ("0" if (dayIndex + 1) < 10 else "") + str(dayIndex + 1)
                selected_date_depart_str = year_month_date_depart + '-' + day_depart
                potential_days_return_list = []
                selected_date_depart_datetime = datetime.strptime(selected_date_depart_str, '%Y-%m-%d')
                for j in range(3, 7):
                    potential_days_return_list.append(selected_date_depart_datetime + relativedelta(days=j))
                for potential_day_return in potential_days_return_list:
                    day_return_str = str(int(potential_day_return.strftime("%d"))-1)
                    month_return_str = str(int(potential_day_return.strftime("%m"))- int(month_string_to_number(data_return[0]["monthDisplayName"])))
                    selected_date_return_str = datetime.strftime(potential_day_return, '%Y-%m-%d')
                    if potential_day_return<return_max_date_datetime:
                        if not data_return[int(month_return_str)]['days'][int(day_return_str)]['lowestFare'] is None:
                            price_return=data_return[int(month_return_str)]['days'][int(day_return_str)]['lowestFare']
                            total_price=exchange_rate*(price_depart+price_return)
                            flight=Flight(departure=depart,destination=destination,depart_date=selected_date_depart_str,
                                          return_date=selected_date_return_str,price=total_price,source='Easyjet')
                            flights.append(flight)
            dayIndex = dayIndex + 1
        General.update_json_files(flights=flights,year_month_date_depart=year_month_date_depart,destination=destination)
        flights = []



def create_dict_for_location(st='all'):
    '''
    :param st:if need to get all the locations
    :return: dict that the key is location-month-year
    '''
    months = (
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
    'December')
    years = (2019, 2020, 2021, 2022, 2023, 2024)
    dict = {}
    if st == 'all':
        for location in locations:
            for year in years:
                for month in months:
                    dict[''.join((location, ' ', month, ' ', str(year)))] = 0
    else:
        for year in years:
            for month in months:
                dict[''.join((st, ' ', month, ' ', str(year)))] = 0
    return dict


def update_locations_new_notfication_file():
    '''
    :return:
        update the notifications flights according to available flights in easyjet
        if the file is not exist, the function create one
    '''
    if not os.path.isfile('Flights/EasyJet/notifications.json'):
        mydict = create_dict_for_location('all')
        mydict = json.dumps(mydict, indent=4)
        with open(os.path.dirname(__file__) + '/../../Data/Flights/EasyJet/notifications.json', 'w') as f:
            f.write(mydict)
            new_location_month_year_list = update_file()
    else:
        new_location_month_year_list = update_file()
    if len(new_location_month_year_list) != 0:
        message = "באתר איזי ג'ט:" + "\n"
        for location_month_year in new_location_month_year_list:
            location_month_year_split = location_month_year.split()
            message = message + "הוסיפו טיסה חדשה ל" + bot.hebrew_dict[' '.join(location_month_year_split[:-2])]
            message = message + " בתאריך " + bot.hebrew_dict[''.join(location_month_year_split[-2:-1])]
            message = message + " " + ''.join(location_month_year_split[-1:]) + "\n"
        bot.bot_send_message(message)
    else:
        bot.bot_send_message("בוצעה סריקה ולא נמצאו טיסות", bot.log_group)


def update_file():
    '''
    :return:
            update the notifications flights according to available flights in easyjet
            and return the new location month year that added to the file
    '''
    driver = sc.prepare_driver('https://www.easyjet.com/en/')
    search_field = driver.find_element_by_name('destination')
    origin_field = driver.find_element_by_name('origin')
    origin_field.clear()
    origin_field.send_keys('TLV')
    origin_field.send_keys(Keys.RETURN)
    new_updates = []
    for location in locations:
        search_field.clear()
        search_field.send_keys(location)
        search_field.send_keys(Keys.RETURN)

        temp = driver.find_element_by_class_name('date-picker-button')
        driver.execute_script("arguments[0].click();", temp)

        try:
            WebDriverWait(driver, timeout=4).until(EC.presence_of_all_elements_located(
                (By.CLASS_NAME, 'route-date-picker-month')))
        except Exception as e:
            bot.bot_send_message(location + "קיימת בעיה במהלך השאיבה של ")
            sys.exit()

        try:
            all_months_of_selenium.clear()
            all_months_strings.clear()
        except:
            pass
        all_months_of_selenium = driver.find_elements_by_class_name('route-date-picker-month')
        all_months_strings = [location + ' ' + month.text.splitlines()[0] for month in all_months_of_selenium if
                              len(month.text) != 0]
        with open(os.path.dirname(__file__) + '/../../Data/Flights/EasyJet/notifications.json', 'r') as JSON:
            current_dict = json.load(JSON)
        for location_month_year_string in all_months_strings:
            if location_month_year_string not in current_dict:
                current_dict[location_month_year_string] = 1
                new_updates.insert(location_month_year_string)
            else:
                if current_dict[location_month_year_string] == 0:
                    current_dict[location_month_year_string] = 1
                    new_updates.append(location_month_year_string)
        mydict = json.dumps(current_dict, indent=4)
        with open(os.path.dirname(__file__) + '/../../Data/Flights/EasyJet/notifications.json', 'w') as f:
            f.write(mydict)
        temp = driver.find_element_by_id('close-drawer-link')
        driver.execute_script("arguments[0].click();", temp)
        time.sleep(1)
    driver.close()
    return new_updates
