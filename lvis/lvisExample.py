
'''
Example of LVIS handler usage
'''

# tell python where to look for the handler
from sys import path
from os import getenv
homeDir=getenv("HOME")
path.extend(["%s/src/pprs_lvis/lvis"%homeDir])


# import functions
from lvisHandler import *

# set a filename
filename='/geos/netdata/avtrain/data/3d/pprs_waveform/lvis/LVIS_US_NH_2009_VECT_20100328.subset.84.h5'

# read data
waves,lon,lat,nWaves,nBins,z,lfid,lShot=readLVIS(filename)

# determine stats
meanNoise,stdevNoise=findStats(waves,z)

# set denoising threshold
noiseSale=5
thresh=setThreshold(meanNoise,stdevNoise,noiseSale)

# denoise
sWidth=1.0
minWidth=3
denoised=denoise(waves,z,thresh,sWidth,minWidth)

# find ground
ground=findGround(denoised,z)

# find height
height,cov=findHeight(denoised,ground,z)

# plot
plotGrWaves(denoised,z,ground,lfid,lShot)


'''
Geotiffs
'''

# import geotiff functions
from lvisTiff import *

# write height geotiff
res=20.0
writeTiff(height,lon,lat,res,epsg=3857,filename="lvis_height.tif")

