from Flights.Utilities import Statistics as st


low_price_x,low_price_y,mid_price_x,mid_price_y,high_price_x,high_price_y=st.get_statistic_of_destination("London")
result_3=[]
result_4=[]
for i in range(len(low_price_y)):
    if low_price_y[i]==3:
        result_3.append(low_price_x[i])
    elif low_price_y[i]==4:
        result_4.append(low_price_x[i])
result_3.sort()
result_4.sort()
print(result_3)
print(result_4)