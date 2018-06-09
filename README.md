# DataTest
A short industrilized program to compute a clustering algorithm on GeoData : 
Kmeans  
DBSCAN  

# Requirement
python 3  
numpy  
scipy  
geopy  
json  
json_normalize  
pandas  
scikit-learn  
matplotlib 

to install a package : pip install 'package_name'  
  
install/dowload Basemap for Windows or Linux  

# Launching the script
python3 data_test.py

# Data
Import a json file and create a DataFrame from it
```python
import json
json_data=open("data.json").read()
data = json.loads(json_data)
df=json_normalize(data) #df is now a dataframe
```
# Algorithm 1 : Kmeans
definition of plotting function :  
function plotting the '% of variance explained' function of the 'K' parameter of the Kmean
Thanks to that plot, we can choose K=5
Predictions are stored in df : feature cluster_kmean

# Algorithm 1 : DBSCAN
Before starting, we compute a new distance
using the vicenty formula to compute distance between stations in meters
```python
def greatCircleDistance(x, y):
    lat1, lon1 = x[0], x[1]
    lat2, lon2 = y[0], y[1]
    return vincenty((lat1, lon1), (lat2, lon2)).meters
```
Predictions are stored in df : feature cluster_dbscan

# OUTPUT
Predictions are stored in the DataFrame df and convert to csv

# PLOTS
for each model, we plot as output a scatter plot withe the different clusters predicted

