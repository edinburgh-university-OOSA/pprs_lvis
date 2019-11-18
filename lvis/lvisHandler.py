
'''
Functions to hold and
analyse LVIS data
'''

###################################
import numpy as np
import h5py   # package to read HDF5 data


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



##############################################

