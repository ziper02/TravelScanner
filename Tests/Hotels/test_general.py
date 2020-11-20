import json
import os
from unittest import TestCase, mock
from Hotel import Hotel
from Hotels import general as hotel_general


class GetLocationDataCityNameTest(TestCase):
    TestCase.maxDiff = None

    def setUp(self):
        with open(os.path.dirname(__file__) + "\\data.json", 'r', encoding='utf-8') as f:
            self.data_tests_folder = json.load(f)
        self.patcher = mock.patch("Hotels.general.os.path.dirname", return_value=os.path.dirname(__file__))
        self.patcher.start()

    def teadDown(self):
        self.patcher.stop()

    def test_get_location_data_by_city_name_get_all_data_no_json(self):
        """
            Test that return the full list of hotels in location without json
        """

        suppose_result = self.data_tests_folder["Budapest Hotels Data"]
        suppose_hotel_data = list()
        for item in suppose_result:
            suppose_hotel_data.append(Hotel(**suppose_result[item]))

        with open(os.path.dirname(__file__) + "\\..\\Data\\Hotels\\Locations Data\\Budapest.json", 'r',
                  encoding='utf-8') as f:
            budapest_hotel_file = json.load(f)
        suppose_hotel_data_from_file = list()
        for hotel_in_file in budapest_hotel_file:
            suppose_hotel_data_from_file.append(Hotel(**budapest_hotel_file[hotel_in_file]))

        given_hotel_data = hotel_general.get_location_data_by_city_name('Budapest')

        self.assertEqual(suppose_hotel_data_from_file, given_hotel_data)
        self.assertEqual(suppose_hotel_data, given_hotel_data)

    def test_get_location_data_by_city_name_get_all_data_with_json(self):
        """
            Test that return the full list of hotels in location with json
        """
        suppose_path_json = os.path.dirname(__file__) + self.data_tests_folder['Budapest Hotels Data Location Path']
        suppose_result = self.data_tests_folder["Budapest Hotels Data"]
        suppose_hotel_data = list()
        for item in suppose_result:
            suppose_hotel_data.append((Hotel(**suppose_result[item]), suppose_path_json))

        json_path = os.path.dirname(__file__) + "//..//Data//Hotels//Locations Data//Budapest.json"
        with open(json_path, 'r', encoding='utf-8') as f:
            budapest_hotel_file = json.load(f)
        suppose_hotel_data_from_file = list()
        for hotel_in_file in budapest_hotel_file:
            suppose_hotel_data_from_file.append((Hotel(**budapest_hotel_file[hotel_in_file]), json_path))

        given_hotel_data = hotel_general.get_location_data_by_city_name('Budapest', True)
        self.assertEqual(suppose_hotel_data, given_hotel_data)
        self.assertEqual(suppose_hotel_data_from_file, given_hotel_data)

    def test_get_location_data_by_city_name_wrong_city_name(self):
        """
        test that return empty list for city name that not exist in data
        """
        suppose_hotel_data = list()
        given_hotel_data_with_json = hotel_general.get_location_data_by_city_name("Jerusalem", True)
        given_hotel_data_without_json = hotel_general.get_location_data_by_city_name("Jerusalem", True)
        self.assertEqual(suppose_hotel_data, given_hotel_data_with_json)
        self.assertEqual(suppose_hotel_data, given_hotel_data_without_json)

    def test_get_location_data_by_city_name_wrong_types_of_parameters(self):
        """
        trying call with wrong types of parameters
        """
        self.assertRaises(ValueError, hotel_general.get_location_data_by_city_name, int(2))
        self.assertRaises(ValueError, hotel_general.get_location_data_by_city_name, 'Haifa', 'Jer')

    def test_get_all_location_data_with_json(self):
        """
        Test that return the full list of hotels from all destinations with json
        """
        hotels_location_path = os.path.dirname(__file__) + "//..//Data//Hotels//Locations Data"
        hotels_files = [f for f in os.listdir(hotels_location_path) if
                        os.path.isfile(os.path.join(hotels_location_path, f))]
        suppose_hotels_data_with_json = list()
        for hotel_file in hotels_files:
            json_path = hotels_location_path + "//" + hotel_file
            with open(json_path, 'r', encoding='utf-8') as f:
                hotel_json = json.load(f)
            for key in hotel_json:
                suppose_hotels_data_with_json.append((Hotel(**hotel_json[key]), json_path))

        given_hotels_data_with_json = hotel_general.get_all_location_data(True)

        given_hotels_data_with_json = [(str(hotel.link), json_path) for (hotel, json_path) in
                                       given_hotels_data_with_json]
        suppose_hotels_data_with_json = [(str(hotel.link), json_path) for (hotel, json_path)
                                         in suppose_hotels_data_with_json]

        self.assertCountEqual(suppose_hotels_data_with_json, given_hotels_data_with_json)

    def test_get_all_location_data_without_json(self):
        """
        Test that return the full list of hotels from all destinations without json
        """
        hotels_location_path = os.path.dirname(__file__) + "\\..\\Data\\Hotels\\Locations Data"
        hotels_files = [f for f in os.listdir(hotels_location_path) if
                        os.path.isfile(os.path.join(hotels_location_path, f))]
        suppose_hotels_data_without_json = list()
        for hotel_file in hotels_files:
            with open(hotels_location_path + "\\" + hotel_file, 'r', encoding='utf-8') as f:
                hotel_json = json.load(f)
            for key in hotel_json:
                suppose_hotels_data_without_json.append(Hotel(**hotel_json[key]))
        given_hotels_data_without_json = hotel_general.get_all_location_data(False)
        suppose_hotels_data_without_json = [str(hotel.link) for hotel in suppose_hotels_data_without_json]
        given_hotels_data_without_json = [str(hotel.link) for hotel in given_hotels_data_without_json]
        self.assertCountEqual(suppose_hotels_data_without_json, given_hotels_data_without_json)

    def test_get_all_location_data_wrong_type_parameter(self):
        """
        trying call with wrong types of parameters
        """
        self.assertRaises(ValueError, hotel_general.get_all_location_data, "bla")
        self.assertRaises(ValueError, hotel_general.get_all_location_data, 7.8)

    @mock.patch("Hotels.general.flight_general.get_list_of_all_destinations", return_value=[])
    def test_get_all_location_data_empty_destinations(self, empty_destinations_list):
        """
        test if get_list_of_all_destinations not working , suppose to return empty list
        Args:
            empty_destinations_list: mocking the flight_general.get_list_of_all_destinations
        """
        self.assertEqual(hotel_general.get_all_location_data(False), [])
        self.assertEqual(hotel_general.get_all_location_data(True), [])

