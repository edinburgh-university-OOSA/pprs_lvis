
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

def appendLVIS(filename,waves,lon,lat,nWaves,nBins,z,lfid,lShot,nRead=1000000,sInd=0):
  '''
  Append to an LVIS array
  '''

  # read new data
  nwaves,nlon,nlat,nnWaves,nnBins,nz,nlfid,nlShot=readLVIS(filename,nRead=nRead,sInd=sInd)

  # append to old arrays
  waves=np.append(waves,nwaves,axis=0)
  lon=np.append(lon,nlon)
  lat=np.append(lat,nlat)
  nWaves=np.append(nWaves,nnWaves)
  nBins=np.append(nBins,nnBins)
  z=np.append(z,nz,axis=0)
  lfid=np.append(lfid,nlfid)
  lShot=np.append(lShot,nlShot)

  return(waves,lon,lat,nWaves,nBins,z,lfid,lShot)


##############################################

def readLVIS(filename,nRead=1000000,sInd=0):
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
  for i in range(0,nWaves):
    res=(lZ0[i]-lZN[i])/nBins
    z[i]=np.arange(lZ0[i],lZN[i],-1.0*res)   # returns an array of floats

  # return arrays to initialiser
  return(waves,lon,lat,nWaves,nBins,z,lfid,lShot)


##############################################

def findStats(waves,z,statsLen=10):
  '''
  Finds standard deviation and mean of noise
  '''

  # set array sizes
  nWaves=waves.shape[0]
  nBins=waves.shape[1]

  # make empty arrays
  meanNoise=np.empty(nWaves)
  stdevNoise=np.empty(nWaves)

  # determine number of bins to calculate stats over
  res=(z[0,0]-z[0,-1])/nBins    # range resolution
  noiseBins=int(statsLen/res)   # number of bins within "statsLen"

  # loop over waveforms
  for i in range(0,nWaves):
    meanNoise[i]=np.mean(waves[i,0:noiseBins])
    stdevNoise[i]=np.std(waves[i,0:noiseBins])

  # return results
  return(meanNoise,stdevNoise)


##############################################

def denoise(waves,z,meanNoise,stdevNoise,noiseScale,sWidth,minWidth):
  '''
  Denoise waveform data
  '''

  # how many waveforms?
  nWaves=waves.shape[0]  # all numpy arrays have their size saved in .shape
  nBins=waves.shape[1]  # all numpy arrays have their size saved in .shape
  res=(z[0,0]-z[0,-1])/nBins    # range resolution

  # make array for output
  denoised=np.full(waves.shape,0)

  # loop over waves
  for i in range(0,nWaves):
    print("Denoising wave",i+1,"of",nWaves)

    # subtract mean background noise
    denoised[i]=waves[i]-meanNoise[i]

    # set threshold
    thresh=noiseScale*stdevNoise[i]

    # set all values less than threshold to zero
    denoised[i,denoised[i]<thresh]=0.0

    # minimum acceptable width
    binList=np.where(denoised[i]>0.0)[0]
    zeroList=[]
    for j in range(0,binList.shape[0]):       # loop over waveforms
      if((j>0)&(j<(binList.shape[0]-1))):    # are we in the middle of the array?
        if((binList[j]!=binList[j-1]+1)|(binList[j]!=binList[j+1]-1)):  # are the bins consecutive?
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
    plt.xlabel('DN')
    plt.ylabel('Elevation (m)')
    plt.plot(waves[i],z[i])
    plt.savefig(filename)
    plt.close()
    plt.clf()

    # write progress
    print("Written to",filename)

  return


##############################################

def plotGrWaves(waves,z,ground,lfid,lShot,outRoot="waveforms"):
  '''
  Plot waveforms with ground marked
  '''

  # determine array size
  nWaves=waves.shape[0]
  nBins=waves.shape[1]

  # loop over waveforms
  for i in range(0,nWaves):
    # set a filename based on the LVIS shot IDs
    filename=outRoot+"."+str(lfid[i])+"."+str(lShot[i])+".png"

    # plot data to file
    plt.xlabel('DN')
    plt.ylabel('Elevation (m)')
    plt.plot(waves[i],z[i])
    plt.plot([0,np.max(waves[i])], [ground[i],ground[i]], color='r', linestyle='-', linewidth=2)  # ground estimate
    plt.savefig(filename)
    plt.close()
    plt.clf()

    # write progress
    print("Written to",filename)

  return


##############################################

def findWaveEnds(waves,z):
  '''
  Find top and bottom of waveform ends
  '''

  # set arrays. Initially to be bounds
  top=np.array(z[:,0])
  bot=np.array(z[:,-1])

  nWaves=waves.shape[0]

  # loop over bounds
  for i in range(0,nWaves):
    # get cumuative distribution for RH metrics
    cumul=np.cumsum(waves[i])/np.sum(waves[i])

    # find the closest value to 0.5% and 99.5%
    topInd=np.abs(cumul-0.005).argmin()   # make use of the "numpy.argmin()" method
    botInd=np.abs(cumul-0.995).argmin()

    # read elevations from z array
    top[i]=z[i,topInd]
    bot[i]=z[i,botInd]

  return(top,bot)


##############################################

def findGround(waves,z,top,bot):
  '''
  Find ground by inflection points
  '''

  print("Finding ground")

  # determine array size
  nWaves=waves.shape[0]
  nBins=waves.shape[1]

  # make array for answers, holding missing data value for now
  ground=np.full(nWaves,-999,dtype=float)

  # loop over waveforms
  for i in range(0,nWaves):
    print("Finding ground, wave",i+1,"of",nWaves)
    # get second derivative
    dydx=np.gradient(waves[i])
    d2ydx2=np.gradient(dydx)

    # set values beyond top and bottom to zero to avoid the messy stuff on the edge of gaussians
    topInd=np.abs(z[i]-top[i]).argmin()
    botInd=np.abs(z[i]-bot[i]).argmin()
    d2ydx2[0:topInd]=0.0
    d2ydx2[botInd+1:]=0.0

    # determine minimum inflection at bottom of waveform
    inFeat=False   # a tracker of if this is the first feature or not
    CofG=contN=0.0
    for j in range(nBins-2,1,-1):  # loop from the bottom
      # look for crossing points of 2nd derivative
      if((d2ydx2[j]<=d2ydx2[j-1])&(d2ydx2[j]<d2ydx2[j+1])):
        if(inFeat):
          break
        else:
          inFeat=True

      # keep track of centre of gravity to use as ground estimate
      if(inFeat):
        CofG=CofG+waves[i,j]*z[i,j]  # add up centre of gravity
        contN=contN+waves[i,j]       # keep track of integral

    # ground is centre of gravity
    if(contN>0.0):
      ground[i]=CofG/contN

  print("Ground found")
  return(ground)


##############################################

def findHeight(waves,ground,z,top,bot):
  '''
  Calculate height and canopy cover
  '''

  # array sizes
  nWaves=waves.shape[0]
  nBins=waves.shape[1]
  res=(z[0,0]-z[0,-1])/nBins

  # create arrays
  height=np.full(nWaves,-999.0)
  cov=np.full(nWaves,-999.0)

  # loop over waveforms
  for i in range(0,nWaves):
    # find the top and bottom
    topInd=np.abs(z[i]-top[i]).argmin()
    botInd=np.abs(z[i]-bot[i]).argmin()

    # height of this above ground
    height[i]=z[i,topInd]-ground[i]

    # total energy
    totE=np.sum(waves[i])

    # energy under ground
    gBin=int((z[i,0]-ground[i])/res)
    grE=np.sum(waves[i,gBin:botInd])*2.0  # times two as this is half the energy
    cov[i]=(totE-grE)/totE

  return(height,cov)


##############################################


