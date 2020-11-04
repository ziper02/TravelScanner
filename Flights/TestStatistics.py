import numpy as np
from sklearn.cluster import KMeans
from Utilities import Statistics as stat
import matplotlib.pyplot as plt


#stat.get_statistic_of_destination("LOND")
#stat.get_statistic_of_dest_per_days("London",5)
#stat.get_statistic_of_dest_per_days("London",6)
x_lst,y_lst=stat.get_statistic_of_destination_temp('LOND')
x=np.array(x_lst) ## normal price
y=np.array(y_lst) ## calculated price
X = np.concatenate([x[:,None],y[:,None]], axis=1)
kmeans = KMeans(n_clusters=9)
kmeans.fit(X)
y_kmeans = kmeans.predict(X) ## label
min=1000
index_min=-1
for i in range(0,9):
    count=0
    for clust in y_kmeans:
        if clust==i:
            if min>x[count]:
                min=x[count]
                index_min=count
            break
        count=count+1
max=0
count=0
max_index=-1
print(min)
for temp in y_kmeans:
    if temp==y_kmeans[index_min] and max<x[count]:
        max = x[count]
        index_max = count
    count=count+1
print(max)
plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')
plt.show()
