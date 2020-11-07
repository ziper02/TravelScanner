# from datetime import datetime
#
#
# from Utilities import General as general
#
# data=general.get_updated_data_by_name("AMS")
# data_in_range=[flight for flight in data if ((datetime.strptime(flight.return_date, '%Y-%m-%d')-datetime.strptime(flight.depart_date, '%Y-%m-%d')).days==5 or
#                                              (datetime.strptime(flight.return_date, '%Y-%m-%d')-datetime.strptime(flight.depart_date, '%Y-%m-%d')).days==6) and  datetime.strptime(flight.return_date, '%Y-%m-%d')<datetime(2021,3,1)]\
#
# for i in range(0,4):
#     print(sorted(data_in_range)[i])

from Utilities import General as general

general.label_all_flights_by_price_range()