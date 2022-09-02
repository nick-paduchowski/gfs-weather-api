# This is a sample Python script.
import math
import numpy
import xarray
import pandas
from datetime import datetime, timedelta, date
import time
import pytz


latitude = 43.151380
longitude = -79.3704 % 360

def find_nearest(array,value):
    idx = numpy.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return float(array[idx-1])
    else:
        return float(array[idx])

variables = ['dpt2m', 'tmpsfc', 'rhprs', 'gustsfc'] # dew point temperature 2 m above ground, surface temperature, relative humidity, surface wind speed
GFS_URL = 'https://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs20220825/gfs_0p25_06z' # GFS run for 2022-08-24
dataset = xarray.open_dataset(GFS_URL)[variables]

GFS_latitude = find_nearest(dataset.lat,latitude)
GFS_longitude = find_nearest(dataset.lon,longitude)

parsed_dataset = dataset.sel(lon=GFS_longitude,lat=GFS_latitude).to_dataframe()

local_tz = pytz.timezone('US/Eastern')
parsed_dataset.index = parsed_dataset.index.tz_localize('UTC')
parsed_dataset.index = parsed_dataset.index.tz_convert(local_tz)


print(parsed_dataset)