
'''
Example of LVIS handler usage
'''

# tell python where to look for the handler
import sys
sys.path.extend(["/home/shancock/wordybits/auldreekie/teaching/pprs/2019/02_intro_programming/src/pprs_lvis/lvis"])


# import functions
from lvisHandler import *

# set a filename
filename='/geos/d71/data/teaching/pprs/data/ILVIS1B_GA2016_0220_R1611_044415.27.h5'
filename='/home/shancock/data/teaching/pprs/lvis/lgw/LVIS_US_NH_2009_VECT_20100328.subset.h5'

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
#plotGrWaves(denoised,z,ground,lfid,lShot)


# import geotiff functions

from lvisTiff import *

# write height geotiff
res=20.0
writeTiff(height,lon,lat,res,epsg=3857,filename="lvis_height.tif")

