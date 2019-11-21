
'''
Script to split up LVIS files
'''

##################################################

from sys import path
from os import getenv
homeDir=getenv("HOME")
path.extend(["%s/src/pprs_answers"%homeDir])



from lvisClass import lvisData
import numpy as np
import argparse
import h5py


##################################################

def readCommands():
  p = argparse.ArgumentParser(description=("Split an LVIS file up"))
  p.add_argument("--input",dest="inName",type=str,default='/Users/dill/data/gedi/lvis/ILVIS1B_GA2016_0220_R1611_045137.h5',help=("Input filename"))
  p.add_argument("--outRoot",dest="outRoot",type=str,default='lvis.split',help=("Input filename"))
  p.add_argument("--nPer", dest ="nPer", type=int, default=1000, help=("Number of waveforms per file"))
  p.add_argument("--bounds",dest = "bounds", type=float, nargs=4, default=[-10000000,-19000000,100000000,1000000], help=("Bounds to extract between, minX minY maxX maxY"))
  cmdargs = p.parse_args()

  return cmdargs


##################################################

def splitLVIS(l,nPer,outRoot):
  nBlocks=int(l.nWaves/nPer+1)
  # loop over blocks
  for i in range(0,nBlocks):
    sInd=i*nPer
    eInd=sInd+nPer
    if(sInd>=l.nWaves):
      break
    if(eInd>l.nWaves):
      eInd=l.nWaves
    # open file
    outName=outRoot+"."+str(i)+".h5"
    f=h5py.File(outName,'w')
    # create datasets
    f.create_dataset('LON0',data=l.lon[sInd:eInd])
    f.create_dataset('LON1023',data=l.lon[sInd:eInd])
    f.create_dataset('LAT0',data=l.lat[sInd:eInd])
    f.create_dataset('LAT1023',data=l.lat[sInd:eInd])
    f.create_dataset('LFID',data=l.lfid[sInd:eInd])
    f.create_dataset('SHOTNUMBER',data=l.shotN[sInd:eInd])
    f.create_dataset('RXWAVE',data=l.waves[sInd:eInd])
    f.create_dataset('Z0',data=l.lZ0[sInd:eInd])
    f.create_dataset('Z1023',data=l.lZN[sInd:eInd])
    f.close()
    print("Written to",outName)
  return


##################################################

if __name__=="__main__":
  '''
  Main block
  '''
  cmdargs=readCommands()
  # read data
  l=lvisData(cmdargs.inName,setElev=0,minX=cmdargs.bounds[0],minY=cmdargs.bounds[1],maxX=cmdargs.bounds[2],maxY=cmdargs.bounds[3])
  # split it
  splitLVIS(l,cmdargs.nPer,cmdargs.outRoot)

