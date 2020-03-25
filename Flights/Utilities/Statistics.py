import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from Entity.Flight import Flight


def get_statistic_of_destination(name):
    with open(os.path.dirname(__file__) + '/../../Data/Flights/json_files_dict.json', 'r') as f:
        dict = json.load(f)
    list=dict[name]
    flights_data = []
    for json_file in list:
        with open(os.path.dirname(__file__)+"/../../" + json_file) as f:
            data = json.load(f)
        for temp in data:
            flights_data.append(Flight(**temp))
    flights_data_filtered=[flight for flight in flights_data if flight.label!=-1]
    flights_days=[(datetime.strptime(flight.return_date, '%Y-%m-%d')-datetime.strptime(flight.depart_date, '%Y-%m-%d')).days
                  for flight in flights_data_filtered]
    flights_price=[flight.price for flight in flights_data_filtered]
    flights_label=[flight.label for flight in flights_data_filtered]
    low_price_x=[]
    low_price_y = []
    mid_price_x=[]
    mid_price_y = []
    high_price_x=[]
    high_price_y = []
    for i in range(len(flights_days)):
        if flights_label[i]==1:
            high_price_y.append(flights_days[i])
            high_price_x.append(flights_price[i])
        elif flights_label[i]==2:
            mid_price_y.append(flights_days[i])
            mid_price_x.append(flights_price[i])
        else:
            low_price_y.append(flights_days[i])
            low_price_x.append(flights_price[i])
    cm = plt.cm.get_cmap('RdYlBu')
    plt.scatter(x=high_price_x,y=high_price_y,label="High",c='Red',s=30)
    plt.scatter(x=mid_price_x, y=mid_price_y, label="Mid",c='Yellow',s=30)
    plt.scatter(x=low_price_x, y=low_price_y, label="Low",c='Green',s=30)
    plt.xlabel('days')
    plt.ylabel('price')
    axes = plt.gca()
    axes.set_ylim([2.5, 7.5])
    axes.set_xlim([110, 1050])
    plt.legend(loc='upper right',fontsize=10,bbox_to_anchor=(1.1, 1.05),fancybox=True)
    plt.show()
    return low_price_x,low_price_y,mid_price_x,mid_price_y,high_price_x,high_price_y
