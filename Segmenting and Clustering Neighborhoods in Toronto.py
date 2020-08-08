#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 


from IPython.display import display_html
import pandas as pd
import numpy as np
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

import folium # plotting library
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans
import matplotlib.cm as cm
import matplotlib.colors as colors


# In[8]:


# Scraping the Wikipedia page for the table of postal codes of Canada

source = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text
soup=BeautifulSoup(source,'lxml')
print(soup.title)
from IPython.display import display_html
tab = str(soup.table)
display_html(tab,raw=True)


# In[9]:


# The html table is converted to Pandas DataFrame for cleaning and preprocessing

dfs = pd.read_html(tab)
df=dfs[0]
df.head()


# In[10]:


#Data preprocessing and cleaning


# In[15]:


# Dropping the rows where Borough is 'Not assigned'

df1 = df[df.Borough != 'Not assigned']


# In[17]:


# Combining the neighbourhoods with same Postalcode
df2 = df1.groupby(['Postal Code','Borough'],sort=False).agg(', '.join)
df2.reset_index(inplace=True)


# In[18]:


# Replacing the name of the neighbourhoods which are 'Not assigned' with names of Borough
df2['Neighbourhood'] = np.where(df2['Neighbourhood'] == 'Not assigned',df2['Borough'], df2['Neighbourhood'])

df2


# In[20]:


#Importing the csv file conatining the latitudes and longitudes for various neighbourhoods in Canada


# In[21]:


lat_lon = pd.read_csv('https://cocl.us/Geospatial_data')
lat_lon.head()


# In[22]:


# Merging the two tables for getting the Latitudes and Longitudes for various neighbourhoods in Canada


# In[32]:


lat_lon.rename(columns={'Postcode':'Postal Code'},inplace=True)


# In[34]:


df3 = pd.merge(df2,lat_lon,on='Postal Code')
df3.head()


# In[35]:


df3.rename(columns={'Postal Code':'Postcode'},inplace=True)


# In[36]:


df3.head()


# In[ ]:





# In[37]:


#Getting all the rows from the data frame which contains Toronto in their Borough.


# In[38]:


df4 = df3[df3['Borough'].str.contains('Toronto',regex=False)]
df4


# In[ ]:





# In[39]:


# Visualizing all the Neighbourhoods of the above data frame using Folium


# In[41]:


map_toronto = folium.Map(location=[43.651070,-79.347015],zoom_start=10)

for lat,lng,borough,neighbourhood in zip(df4['Latitude'],df4['Longitude'],df4['Borough'],df4['Neighbourhood']):
    label = '{}, {}'.format(neighbourhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
    [lat,lng],
    radius=5,
    popup=label,
    color='blue',
    fill=True,
    fill_color='#3186cc',
    fill_opacity=0.7,
    parse_html=False).add_to(map_toronto)
map_toronto


# In[42]:


# Using KMeans clustering for the clsutering of the neighbourhoods


# In[43]:


k=5
toronto_clustering = df4.drop(['Postcode','Borough','Neighbourhood'],1)
kmeans = KMeans(n_clusters = k,random_state=0).fit(toronto_clustering)
kmeans.labels_
df4.insert(0, 'Cluster Labels', kmeans.labels_)


# In[44]:


df4


# In[45]:


# create map
map_clusters = folium.Map(location=[43.651070,-79.347015],zoom_start=10)

# set color scheme for the clusters
x = np.arange(k)
ys = [i + x + (i*x)**2 for i in range(k)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, neighbourhood, cluster in zip(df4['Latitude'], df4['Longitude'], df4['Neighbourhood'], df4['Cluster Labels']):
    label = folium.Popup(' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.7).add_to(map_clusters)
       
map_clusters


# In[ ]:





# In[ ]:




