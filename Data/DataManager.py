import json
import os


class DataManager:
    with open(os.path.dirname(__file__) + '\\data.json') as f:
        __data = json.load(f)
    Label_bot = __data["Label bot"]
    TravelScanner_bot = __data["TravelScanner bot"]
    SkyScanner_whole_month_request = __data["SkyScanner whole month request"]
    Easyjet_whole_month_request = __data["Easyjet whole month request"]
    currency_conversion = __data["Currency conversion"]
    Wizzair_headers = __data["Wizzair headers"]
    Wizzair_whole_month_request = __data["Wizzair whole month request"]
    Wizzair_data_structure = __data["Wizzair data structure"]
    url_request_wizzair_api_version = __data["Url request wizzair api version"]
    booking_order_address = __data["Booking order address"]
    booking_headers = __data["Booking headers"]
    with open(os.path.dirname(__file__) + '\\monthDict.json') as f:
        month_dict = json.load(f)


