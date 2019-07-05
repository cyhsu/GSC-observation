import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import scipy.io as sio
import cartopy.crs as ccrs
import cartopy.feature as cf
import pandas as pd
import os
from glob import glob

def read_cmorph(fid):
	with open(fid,'rb') as f:
		a = np.fromfile(f,np.float32)
	return np.ma.masked_where(a==-999,a).reshape(480,1440) 

def cmorph_to_netcdf(fid):
	tim = pd.to_datetime(fid.split('_')[-1],format='%Y%m%d')
	a = read_cmorph(fid)
	lon, lat = np.arange(0.125,360,0.25), np.arange(-59.875,60,0.25)
	lon[lon > 180.] = lon[lon>180.] - 360.
	df = xr.DataArray(read_cmorph(fid), coords=[lat,lon],
		dims=['lat','lon'], name='cmorph').assign_coords(time=tim)
	df['lat'].attrs['units'] = 'Degrees-North'
	df['lon'].attrs['units'] = 'Degrees-East'    
	df.attrs['title'] = 'CMORPH Version 1.0BETA Version, daily precip from 00Z-24Z'
	df.attrs['units'] = 'CMORPH Version 1.0 daily precipitation (mm)'
	return df
	
	
fids = glob('./*/*/*'); fids.sort()

df = []
for fid in fids:
	df.append(cmorph_to_netcdf(fid))
df = xr.concat(df,dim='time').to_dataset()
df.attrs['host'] = 'ada.tamu.edu'
df.attrs['code'] = 'read_cmorph.py'
df.attrs['path'] = os.getcwd()
	
outnc = 'CMORPH_daily_1998_2018.nc'
df.to_netcdf(outnc,encoding={'time':{'units': 'days since 1990-01-01'}},
				 unlimited_dims={'time':True})
	

