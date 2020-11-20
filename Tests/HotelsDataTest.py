from unittest import TestCase
import os,json






class HotelsTest(TestCase):

    def test_attributes_of_hotels_location_data(self):
        """
        check that all the the attributes of Hotel Location data is valid
        """
        location_data_path=os.path.dirname(__file__)+"\Data Updated\Hotels\Locations Data"
        hotels_names = os.listdir(location_data_path)
        att_set=set()
        suppose_att_set={'facilities', 'address', 'staff', 'popular facilities', 'cleanliness',
                         'score', 'comfort', 'value for money', 'location', 'free wifi', 'link', 'name'}
        for hotel_name in hotels_names:
            with open(f'{location_data_path}\\{hotel_name}','r',encoding='utf-8') as f:
                hotel_data:dict=json.load(f)
            for hotel_key,hotel_att in hotel_data.items():
                for att in hotel_att.keys():
                    att_set.update([att])
        self.assertEqual(att_set,suppose_att_set)

