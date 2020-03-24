import time

from MyScanner import Scanner as sc
import os
import json

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from TelegramBot import bot
import sys



locations = ('Amsterdam', 'London Stansted', 'Berlin Schoenefeld', 'Berlin Tegal', 'Geneva', 'London Gatwick',
    'London Luton', 'Lyon', 'Manchester', 'Milan Malpensa', 'Paris Charles de Gaulle (CDG)')

def create_dict_for_location(st='all'):
    '''
    :param st:if need to get all the locations
    :return: dict that the key is location-month-year
    '''
    months=('January','February','March','April','May','June','July','August','September','October','November','December')
    years=(2019,2020,2021,2022,2023,2024)
    dict = {}
    if st=='all':
        for location in locations:
            for year in years:
                for month in months:
                    dict[''.join((location,' ',month,' ',str(year)))]=0
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
        mydict=create_dict_for_location('all')
        mydict = json.dumps(mydict, indent=4)
        with open(os.path.dirname(__file__) +'/../../Data/Flights/EasyJet/notifications.json', 'w') as f:
            f.write(mydict)
            new_location_month_year_list=update_file()
    else:
        new_location_month_year_list=update_file()
    if len(new_location_month_year_list)!=0:
        message = "באתר איזי ג'ט:"+"\n"
        for location_month_year in new_location_month_year_list:
            location_month_year_split=location_month_year.split()
            message = message + "הוסיפו טיסה חדשה ל" + bot.hebrew_dict[' '.join(location_month_year_split[:-2])]
            message = message + " בתאריך " + bot.hebrew_dict[''.join(location_month_year_split[-2:-1])]
            message = message + " " +''.join(location_month_year_split[-1:])+"\n"
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
    new_updates=[]
    for location in locations:
        search_field.clear()
        search_field.send_keys(location)
        search_field.send_keys(Keys.RETURN)


        temp=driver.find_element_by_class_name('date-picker-button')
        driver.execute_script("arguments[0].click();", temp)

        try:
            WebDriverWait(driver, timeout=4).until(EC.presence_of_all_elements_located(
               (By.CLASS_NAME, 'route-date-picker-month')))
        except Exception as e :
            bot.bot_send_message(location+"קיימת בעיה במהלך השאיבה של ")
            sys.exit()

        try:
            all_months_of_selenium.clear()
            all_months_strings.clear()
        except:
            pass
        all_months_of_selenium=driver.find_elements_by_class_name('route-date-picker-month')
        all_months_strings=[location+' '+month.text.splitlines()[0] for month in all_months_of_selenium if len(month.text)!=0]
        with open(os.path.dirname(__file__) +'/../../Data/Flights/EasyJet/notifications.json', 'r') as JSON:
            current_dict = json.load(JSON)
        for location_month_year_string in all_months_strings:
                if location_month_year_string not in current_dict:
                    current_dict[location_month_year_string] = 1
                    new_updates.insert(location_month_year_string)
                else:
                    if current_dict[location_month_year_string]==0:
                        current_dict[location_month_year_string]=1
                        new_updates.append(location_month_year_string)
        mydict = json.dumps(current_dict, indent=4)
        with open(os.path.dirname(__file__) +'/../../Data/Flights/EasyJet/notifications.json', 'w') as f:
            f.write(mydict)
        temp=driver.find_element_by_id('close-drawer-link')
        driver.execute_script("arguments[0].click();", temp)
        time.sleep(1)
    driver.close()
    return new_updates


