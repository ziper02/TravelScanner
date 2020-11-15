import json
import os


class DataManager:
    destination_list_skyscanner = ["LOND", "PRAG", "BERL", "MUC", "ZRH", "BCN", "MAD", "AMS", "MAN",
                                   "BUD", "GVA", "PARI", "BOJ", "VAR", "MILA", "SOF", "SKG", "DUB", "LIS", "BELI",
                                   "MLA"]
    destination_list_easyjet = ["AMS", "BSL", "SXF", "TXL", "BOD", "GVA", "LTN", "LYS", "MAN",
                                "MXP", "NTE", "NAP", "NCE", "CDG", "TLS", "VCE"]
    destination_list_wizzair = ["VAR", "SOF", "VIE", "BUD", "DEB", "RIX", "VNO", "KTW", "KRK", "WAW", "OTP", "CLJ",
                                "IAS",
                                "SBZ", "TSR", "LTN"]
    depart_list = ["TLV"]

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

    @classmethod
    def month_string_to_number(cls, month_name):
        """
        :param month_name: shortcut of month's name
        :type month_name: str
        :return: the number of month
        :rtype: str
        """
        m = {
            'jan': "01",
            'feb': "02",
            'mar': "03",
            'apr': "04",
            'may': "05",
            'jun': "06",
            'jul': "07",
            'aug': "08",
            'sep': "09",
            'oct': "10",
            'nov': "11",
            'dec': "12"
        }
        s = month_name.strip()[:3].lower()

        try:
            out = m[s]
            return out
        except Exception:
            raise ValueError('Not a month')

    @classmethod
    def transfer_airport_cod_names_to_all(cls, short_name):
        """
        :param short_name the code name airport
        :type short_name str
        :return: the code transferred to all code of possible for example LTN -> LOND
        :rtype: str
        """
        m = {
            'SXF': 'BERL',
            'TXL': 'BERL',
            'LTN': 'LOND',
            'CDG': 'PARI'
        }
        if short_name in m:
            return m[short_name]
        else:
            return short_name
