 # Travel Scanner

## Software description  
This Software developed as personal project. 
The purpose of this project is let the user tools for getting information for start plan his travel, The project is still in progress but already offer few tools.

## Project Components
* The data is fetched by [Selenium automation](https://www.selenium.dev/).  
* The Telegram bot running by using [Python-Telegram-Bot](https://github.com/python-telegram-bot/python-telegram-bot).
  
## Requirements
For this project need Chrome version 76, The version of ChromeDriver only supports this one.
if you using other version of chrome , you can find out [Here](https://chromedriver.chromium.org/downloads) Chromedriver.exe for your chrome version
## Services  
* For getting EasyJet new fights notifications change in bot.py ,TOKEN TO ACCESS THE HTTP API to your token, after this, have an example for how to run the bot.
* For getting all information on hotels in specific location use update_data_per_location_hotels_without_dates("Location Name") in ScannerHotel.py,and it will create JSON file in "Location_Data" folder with all the data.  
  For example:  
  ScannerHotel.update_data_per_location_hotels_without_dates("Berlin") will create Berlin_data.json in Location data folder.
* For getting all information on hotels in specific location and specific dates use get_data_of_location_hotel_in_dates(MySearch) in ScannerHotel.py,and it will create JSON file in "Order_Data" folder with all the data.  
    For example:  
    MySearch=hotel.hotel('London','12-12-20','12-15-20')
    ScannerHotel.get_data_of_location_hotel_in_dates(MySearch)

