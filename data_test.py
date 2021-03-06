# author : Adnane MARZOUK


import pandas as pd
from pandas.io.json import json_normalize
import json
import time
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from geopy.distance import vincenty
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
import matplotlib.cm as cm
from scipy.spatial.distance import cdist, pdist
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import copy
import json
import math
from collections import OrderedDict
import warnings
warnings.filterwarnings('ignore')


#import data
json_data=open("Brisbane_CityBike.json").read()
data = json.loads(json_data)
df=json_normalize(data) #DataFrame

#Kmean
X = df[['latitude', 'longitude']].values
Ks = range(1, 10)
kmean = [KMeans(n_clusters=i).fit(X) for i in Ks]

#plotting elbow to choose the K parameter of the Kmean
def plot_elbow(kmean, X):
    centroids = [k.cluster_centers_ for k in kmean]
    D_k = [cdist(X, center, 'euclidean') for center in centroids]
    dist = [np.min(D,axis=1) for D in D_k]

    # Total with-in sum of square
    wcss = [sum(d**2) for d in dist]
    tss = sum(pdist(X)**2)/X.shape[0]
    bss = tss-wcss

    plt.subplots(nrows=1, ncols=1, figsize=(8,8))
    ax = plt.subplot(1, 1, 1)
    ax.plot(Ks, bss/tss*100, 'b*-')
    plt.grid(True)
    plt.xlabel('Number of clusters')
    plt.ylabel('Percentage of variance explained (%)')
    plt.title('Elbow for KMeans clustering')
    plt.show()

plot_elbow(kmean, X)

#parameter
k = 5
model = kmean[k-1]
df['cluster_kmean'] = model.predict(X).tolist() # model predictions
coefficient = metrics.silhouette_score(X, model.labels_)
print('Silhouette coefficient: {:0.03f}'.format(metrics.silhouette_score(X, model.labels_))) #

ax = df.plot(kind='scatter', x='longitude', y='latitude',c='cluster_kmean', alpha=0.5, linewidth=0)
ax.set_title("Spatial Clustering with KMeans (k=5)")
plt.show()

#DBSCAN

#using the vicenty formula to compute distance between stations in meters
def greatCircleDistance(x, y):
    lat1, lon1 = x[0], x[1]
    lat2, lon2 = y[0], y[1]
    return vincenty((lat1, lon1), (lat2, lon2)).meters

#parameters
eps = 700       #(The maximum distance between two samples for them to be considered as in the same neighborhood)
min_sample=8   #(The number of samples in a neighborhood for a point to be considered as a core point.)
metric=greatCircleDistance      #(The metric to use when calculating distance between instances in a feature array.)

model2 = DBSCAN(eps=eps, min_samples=min_sample, metric=metric).fit(X)
df['cluster_dbscan'] = model2.labels_.tolist() # model predictions
print('Silhouette coefficient: {:0.03f}'.format(metrics.silhouette_score(X, model2.labels_)))

ax = df.plot(kind='scatter', x='longitude', y='latitude',c='cluster_dbscan', alpha=0.5, linewidth=0)
ax.set_title("DBSCAN ('greatCircle', eps={}, min_sample={})".format(eps, min_sample))
plt.show()


#saving predictions in a CSV file
df.to_csv('clustering_predictions.csv',sep=';')
