import math
import numpy as np
import xarray as xr
import requests
import pandas as pd
from datetime import datetime, timedelta, date
import time
import pytz

latitude = 43.17 # latitude of point
longitude = -79.24 % 360 # longitude of point when converting to 0-360 scale used by NOAA GFS.

# Function for finding the NOAA coordinates nearest to the site's coordinates
def find_nearest(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return float(array[idx-1])
    else:
        return float(array[idx])

variables = ['pressfc', 'gustsfc', 'tmpsfc']

#Pressfc is surface pressure measured in PA
#Gustsfc is suface windspeed measured in M/S
#Tmpsfc is surface temperature measured in kelvin
#Rhprs is relative humidity as a %

date_string = datetime.today().strftime('%Y%m%d')

GFS_URL = f'http://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs{date_string}/gfs_0p25_00z' # GFS run for current date
dataset = xr.open_dataset(GFS_URL)[variables]

# Finding the nearest lat long coordinates for this point
print('getting coordiante data')
GFS_latitude = find_nearest(dataset.lat,latitude)
GFS_longitude = find_nearest(dataset.lon,longitude)

# Parsing dataset for specific lat long coordinates and converting to pandas dataframe
#print('parsing')
#parsed_dataset = dataset.sel(lon=GFS_longitude,lat=GFS_latitude).to_dataframe()


# localizing timezone since timestamps from NOAA are in UTC
#local_tz = pytz.timezone('US/Eastern')
#parsed_dataset.index = parsed_dataset.index.tz_localize('UTC')
#parsed_dataset.index = parsed_dataset.index.tz_convert(local_tz)

ds = dataset.sel(lon=GFS_longitude,lat=GFS_latitude)
#This gives you something like this
'''
<xarray.Dataset>
Dimensions:  (time: 129)
Coordinates:
  * time     (time) datetime64[ns] 2024-02-01 2024-02-01T03:00:00 ... 2024-02-17
    lat      float64 43.25
    lon      float64 280.8
Data variables:
    pressfc  (time) float32 ...
    gustsfc  (time) float32 ...
    tmpsfc   (time) float32 ...
Attributes:
    title:        GFS 0.25 deg starting from 00Z01feb2024, downloaded Feb 01 ...
    Conventions:  COARDS\nGrADS
    dataType:     Grid
    history:      Thu Feb 01 09:10:25 UTC 2024 : imported by GrADS Data Serve...
'''

times = ds['time'].values.tolist()
temp_data = ds['tmpsfc'].values.tolist()
wind_data = ds['gustsfc'].values.tolist()
pressure_data= ds['pressfc'].values.tolist()

weather_forecast = []



for x in range(0, len(times)):
    weather_forecast.append({
        int(times[x] / 1000000000): {
            "temp": temp_data[x],
            "wind_speed": wind_data[x],
            "pressure": pressure_data[x]
        }
    })

print(weather_forecast)

#print(ds['gustsfc'].values)



#print(ds['gustsfc'].values.tolist())



'''
for x in ds['time']:
    times.append(x.values)

for i in ds['tmpsfc']:
    temp_data.append(i.values)

print(times)
print(temp_data)
'''