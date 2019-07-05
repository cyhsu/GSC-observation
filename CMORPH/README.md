NOAA CPC Morphing Technique ("CMORPH"), PYTHON SCRIPTS
Using Numpy and Xarray to reconstruct the CMORPH dataset.

  Information
===============


          1. information site:
          https://www.cpc.ncep.noaa.gov/products/janowiak/cmorph_description.html
          
          2. download site:
          ftp://ftp.cpc.ncep.noaa.gov/precip/CMORPH_V1.0/
          
          3. Xarray site: 
          http://xarray.pydata.org/en/stable/
          
          
  Notification
================

          The code (read_cmorphy.py) here is focused on the daily mean dataset. 
          In order to modify it, please check the GrADs CTL files that are listed on the download site (CTL directory).

          You should change the domain size (lat,lon) from (480,1440) to whatever domain you are reading. 
