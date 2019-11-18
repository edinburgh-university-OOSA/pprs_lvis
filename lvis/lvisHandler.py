
'''
Functions to hold and
analyse LVIS data
'''

###################################
import numpy as np
import matplotlib.pyplot as plt
import h5py                                          # package to read HDF5 data
from scipy.ndimage.filters import gaussian_filter1d  # smoothing function


##############################################

def readLVIS(filename,nRead=10000,sInd=0):
  '''
  Read LVIS data from file
  '''

  # open file for reading
  f=h5py.File(filename,'r')

  # determine number of waveforms so we can decide how many to read
  temp=np.array(f['LFID'])
  if((nRead<0)|(temp.shape[0]<(nRead+sInd))):
    nRead=temp.shape[0]-sInd
  print("Reading",nRead,"waveforms from",filename)

  # load sliced arrays, to save RAM
  lfid=temp[sInd:nRead+sInd]                         # the LVIS flight ID, a label
  lShot=np.array(f['SHOTNUMBER'][sInd:nRead+sInd])   # the LVIS shot number, a label
  waves=np.array(f['RXWAVE'][sInd:nRead+sInd])       # the recieved waveforms. The data, in a 2D array

  # store the array dimensions for ease of access
  nWaves=nRead
  nBins=waves.shape[1]

  # these variables will be converted to easier variables. Read in to temporary arrays for now
  lZN=np.array(f['Z1023'][sInd:nRead+sInd])       # The elevation of the waveform bottom
  lZ0=np.array(f['Z0'][sInd:nRead+sInd])          # The elevation of the waveform top
  lon0=np.array(f['LON0'][sInd:nRead+sInd])       # longitude of waveform top
  lat0=np.array(f['LAT0'][sInd:nRead+sInd])       # lattitude of waveform top
  lon1023=np.array(f['LON1023'][sInd:nRead+sInd]) # longitude of waveform bottom
  lat1023=np.array(f['LAT1023'][sInd:nRead+sInd]) # lattitude of waveform bottom

  # close file
  f.close()

  # get coordinate of each waveform
  lon=(lon0+lon1023)/2.0
  lat=(lat0+lat1023)/2.0

  # make z arrays
  z=np.empty((nRead,nBins))
  for i in range(0,nBins):
    res=(lZ0[i]-lZN[i])/nBins
    z[i]=np.arange(lZ0[i],lZN[i],-1.0*res)   # returns an array of floats

  # return arrays to initialiser
  return(waves,lon,lat,nWaves,nBins,z,lfid,lShot)


##############################################

def findStats(waves,z,nWaves,nBins,statsLen=10):
  '''
  Finds standard deviation and mean of noise
  '''

  # make empty arrays
  meanNoise=np.empty(nWaves)
  stdevNoise=np.empty(nWaves)

  # determine number of bins to calculate stats over
  res=(z[0,-1]-z[0,0])/nBins    # range resolution
  noiseBins=int(statsLen/res)   # number of bins within "statsLen"

  # loop over waveforms
  for i in range(0,nWaves):
    meanNoise[i]=np.mean(waves[0:noiseBins])
    stdevNoise[i]=np.std(waves[0:noiseBins])

  # return results
  return(meanNoise,stdevNoise)


##############################################

def setThreshold(meanNoise,stdevNoise,scale):
  '''
  Sets denoising threshold
  '''
  thresh=meanNoise+scale*stdevNoise
  return(thresh)


##############################################

def denoise(waves,thresh,sWidth,minWidth):
  '''
  Denoise waveform data
  '''

  # how many waveforms?
  nWaves=waves.shape[0]  # all numpy arrays have their size saved in .shape

  # make array for output
  denoised=np.full(waves.shape,0)

  # loop over waves
  for i in range(0,nWaves):
    # subtract background noise
    denoised[i]=waves[i]-thresh[i]

    # set all negative values to zero
    denoised[i,denoised[i]<0]=0.0

    # minimum acceptable width
    binList=np.where(denoised[i]>0.0)[0]
    zeroList=[]
    for j in range(0,binList.shape[0]):       # loop over waveforms
      if((j>0)&(j<(binList.shape[0]-1))):    # are we in the middle of the array?
        if((binList[j]!=binList[j-1]-1)|(binList[j]!=binList[j+1]+1)):  # are the bins consecutive?
          denoised[i,binList[j]]=0   # if not, set to zero

    # smooth
    denoised[i]=gaussian_filter1d(denoised[i],sWidth/res)

  return(denoised)


##############################################

def plotWaves(waves,z,lfid,lShot,outRoot="waveforms"):
  '''
  Plot waveforms
  '''

  # determine array size
  nWaves=waves.shape[0]
  nBins=waves.shape[1]

  # loop over waveforms
  for i in range(0,nWaves):
    # set a filename based on the LVIS shot IDs
    filename=outRoot+"."+str(lfid[i])+"."+str(lShot[i])+".png"

    # plot data to file
    plt.ylabel('DN')
    plt.xlabel('Elevation (m)')
    plt.plot(waves[i],z[i])
    plt.savefig(filename)
    plt.close()
    plt.clf()

    # write progress
    print("Written to",filename)

  return

##############################################

