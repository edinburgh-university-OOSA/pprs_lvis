
'''
Example of LVIS handler usage
'''

# tell python where to look for the handler
import sys
sys.path.extend(["/home/shancock/wordybits/auldreekie/teaching/pprs/2019/02_intro_programming/src/pprs_lvis/lvis"])

# import functions
from lvisHandler import *

# set a filename
filename="/home/shancock/data/teaching/oosa/week5_lvis/lvis.200Mbytes/ILVIS1B_GA2016_0220_R1611_045137.3.h5"

# read data
waves,lon,lat,nWaves,nBins,z,lfid,lShot=readLVIS(filename)

# determine stats
meanNoise,stdevNoise=findStats(waves,z)

# set denoising threshold
noiseSale=3.5
thresh=setThreshold(meanNoise,stdevNoise,noiseSale)

# denoise
sWidth=0.9
minWidth=3
denoised=denoise(waves,z,thresh,sWidth,minWidth)

# find ground
ground=findGround(denoised,z)


