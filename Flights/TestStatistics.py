import numpy as np
from sklearn.cluster import KMeans
from Utilities import Statistics as stat
import matplotlib.pyplot as plt


#stat.get_statistic_of_destination("LOND")
#stat.get_statistic_of_dest_per_days("London",5)
#stat.get_statistic_of_dest_per_days("London",6)
x_lst,y_lst=stat.get_statistic_of_destination_temp('LOND')
x=np.array(x_lst)
y=np.array(y_lst)
X = np.concatenate([x[:,None],y[:,None]], axis=1)
kmeans = KMeans(n_clusters=4)
kmeans.fit(X)
y_kmeans = kmeans.predict(X)
plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')
plt.show()
