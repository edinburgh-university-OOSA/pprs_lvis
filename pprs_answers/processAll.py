

'''
Process all LVIS data
'''

# set up path to packages
from sys import path
from os import getenv
homeDir=getenv("HOME")
path.extend(["%s/src/pprs_lvis/lvis"%homeDir])

# import functions
from lvisHandler import *



# get a list of all LVIS data
import os

dir='/geos/netdata/avtrain/data/3d/pprs_waveform/lvis/'
fileList=os.listdir(dir)


# read first file to set up arrays
filename=dir+fileList[0]
waves,lon,lat,nWaves,nBins,z,lfid,lShot=readLVIS(filename)


for namen in fileList[1:]:
  filename=dir+namen
  waves,lon,lat,nWaves,nBins,z,lfid,lShot=appendLVIS(filename,waves,lon,lat,nWaves,nBins,z,lfid,lShot)


