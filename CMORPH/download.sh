#!/bin/bash
#-
#- Goal: Download the CMORPH_v1.0 Daily Rainfall Data
#- Period: From 1998 to 2019
#- Requirement: Bash Shell, Wget
#- Password Requirement: None
#-
#- CopyRight: C.Y. Hsu @TAMU, 2019-07-05.

web_head='ftp://ftp.cpc.ncep.noaa.gov/precip/CMORPH_V1.0/CRT/0.25deg-DLY_00Z'
for year in {1998..2019}
do
   for mo in {01..12}
   do
      #-- Create a directory, and subdirectory.
      dirc="${year}/${mo}"
      mkdir -p "${dirc}"

      #-- Construct a download Link, and download it.
      link="${web_head}/${year}/${year}${mo}/"
      wget -q -O index.html $link
      list=`grep ftp 'index.html' |sed 's/.*href="//'|sed 's/bz2.*/bz2/'|grep bz2`
      for fid in $list
      do
         echo $fid
         wget -q $fid
      done

      #-- Decompress the download files.
      bzip2 -d *bz2
      rm index.html

      #-- Move the decompress files into sub-directory.
      mv CMORPH* $dirc
   done
done
