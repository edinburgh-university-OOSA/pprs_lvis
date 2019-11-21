

'''
Example solution for
batch processing LVIS
'''

# set up path to packages
from sys import path
from os import getenv
homeDir=getenv("HOME")
path.extend(["%s/src/pprs_lvis/lvis"%homeDir])

# import functions
from lvisHandler import *


# get a list of all LVIS data using the os package
import os

direc='/geos/netdata/avtrain/data/3d/pprs_waveform/lvis/'
fileList=os.listdir(direc)


# read first file to set up arrays
filename=direc+fileList[0]
waves,lon,lat,nWaves,nBins,z,lfid,lShot=readLVIS(filename)

# loop over all files and use the appendLVIS function.
for namen in fileList[1:]:
  filename=direc+namen
  waves,lon,lat,nWaves,nBins,z,lfid,lShot=appendLVIS(filename,waves,lon,lat,nWaves,nBins,z,lfid,lShot)


# the waves array now contains all the data from all files
# process data, as before

# determine stats
meanNoise,stdevNoise=findStats(waves,z)

# denoise
noiseScale=3.5
sWidth=1.0
minWidth=3
denoised=denoise(waves,z,meanNoise,stdevNoise,noiseScale,sWidth,minWidth)

# determine top and bottom of waveform (RH99.5 and RH0.5)
top,bot=findWaveEnds(denoised,z)

# find ground
ground=findGround(denoised,z,top,bot)

# find height and cover
height,cov=findHeight(denoised,ground,z,top,bot)

# make geotiffs of all properties
from lvisTiff import *
res=30.0
writeTiff(height,lon,lat,res,epsg=3857,filename="lvis_height.tif")
writeTiff(ground,lon,lat,res,epsg=3857,filename="lvis_dtm.tif")
writeTiff(top,lon,lat,res,epsg=3857,filename="lvis_dsm.tif")
writeTiff(cov,lon,lat,res,epsg=3857,filename="lvis_cover.tif")

