import json
import os


class data_manager:
    with open(os.path.dirname(__file__)+'\data.json') as f:
        _data = json.load(f)
    Label_bot = _data["Label bot"]
    TravelScanner_bot = _data["TravelScanner bot"]
    SkyScanner_whole_month_request=_data["SkyScanner whole month request"]
    Easyjet_whole_month_request=_data["Easyjet whole month request"]
    currency_conversion=_data["Currency conversion"]
    Wizzair_headers=_data["Wizzair headers"]
    Wizzair_whole_month_request = _data["Wizzair whole month request"]
    Wizzair_data_structure = _data["Wizzair data structure"]

