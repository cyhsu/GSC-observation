#-
#-
#- Goal: Read in Binary dataset of CMORPH and output to NetCDF
#- Language: Python
#- Packages: numpy xarray matploblib scipy cartopy pandas os glob
#- Password Requirement: None
#-
#- CopyRight: C.Y. Hsu @TAMU, 2019-07-05.
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
df.attrs['host'] = 'your_host_name'
df.attrs['code'] = 'read_cmorph.py'
df.attrs['path'] = os.getcwd()
	
outnc = 'CMORPH_daily_1998_2018.nc'
df.to_netcdf(outnc,encoding={'time':{'units': 'days since 1990-01-01'}},
				 unlimited_dims={'time':True})
	

	
	
	
##-- test plot:
#fig, axes = plt.subplots(ncols=1,nrows=1,figsize=(10,8), subplot_kw=dict(projection=ccrs.PlateCarree()))             
#axes.set_extent([-100+360,-77+360,18,35])  
#axes.coastlines(resolution='50m',lw=1.0,color='white')  
#axes.add_feature(cf.OCEAN.with_scale('50m'),lw=1.0,edgecolor='white')  
#axes.add_feature(cf.LAND.with_scale('50m'),lw=1.0,edgecolor='white')    
#axes.pcolormesh(df.lon.data,df.lat.data,df.sel(time='2017-08-30').cmorph.data,vmin=0,vmax=300,cmap=plt.cm.jet)

##-- Error --: Need to check the error message... (2019-07-05)
##df.sel(time='2017-08-30').cmorph.plot.pcolormesh(ax=axes,vmin=0,vmax=350,cmap=plt.cm.jet) 
