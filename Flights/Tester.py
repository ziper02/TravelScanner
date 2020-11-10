from datetime import datetime


from Utilities import general as general

data=general.get_all_updated_data()
data_in_range=[flight for flight in data if (flight.days==5 or flight.days==6) and flight.destination_value<=25 and  (flight.label==4 or flight.label==3) and  datetime.strptime(flight.depart_date, '%Y-%m-%d')>datetime(2020,11,8) and datetime.strptime(flight.return_date, '%Y-%m-%d')<datetime(2021,3,1)]
dict={}
count=0
for i in range(0,len(data_in_range)):
    flight=sorted(data_in_range)[i]
    if flight.destination.code not in dict.keys():
        print(flight.pretty_print())
        print()
        dict[flight.destination.code]='1'
        count=count+1
        if count==15:
            break

