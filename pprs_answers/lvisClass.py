
'''
A class to hold LVIS data
with methods to read
'''

###################################
import numpy as np
import h5py


###################################

class lvisData(object):
  '''
  LVIS data handler
  '''

  def __init__(self,filename,nRead=-1,sInd=0,setElev=0,minX=-100000000,maxX=100000000,minY=-1000000000,maxY=100000000):
    '''
    Class initialiser. Calls a function
    to read "nRead" waveforms, starting 
    at "sInd" from the file, filename
    setElev=1 converts LVIS's stop and start
    elevations to arrays of elevation.
    '''
    # call the file reader and load in to the self
    self.waves,self.lon,self.lat,self.nWaves,self.nBins,self.lZN,self.lZ0,self.lfid,self.shotN=lvisData.readLVIS(filename,nRead,sInd,minX,maxX,minY,maxY)
    if(setElev==1):     # to save time, only read elev if wanted
      lvisData.setElevations(self)


  ###########################################

  def readLVIS(filename,nRead,sInd,minX,maxX,minY,maxY):
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
    lfid=temp[sInd:nRead+sInd]          # the LVIS flight ID, a label
    lShot=np.array(f['SHOTNUMBER'][sInd:nRead+sInd])   # the LVIS shot number, a label
    waves=np.array(f['RXWAVE'][sInd:nRead+sInd])       # the recieved waveforms. The data
    # store the array dimensions for ease of access
    nWaves=nRead
    nBins=waves.shape[1]
    # these variables will be converted to easier variables
    lZN=np.array(f['Z1023'][sInd:nRead+sInd])       # The elevation of the waveform bottom
    lZ0=np.array(f['Z0'][sInd:nRead+sInd])          # The elevation of the waveform top
    lon0=np.array(f['LON0'][sInd:nRead+sInd])       # longitude of waveform top
    lat0=np.array(f['LAT0'][sInd:nRead+sInd])       # lattitude of waveform top
    lon1023=np.array(f['LON1023'][sInd:nRead+sInd]) # longitude of waveform bottom
    lat1023=np.array(f['LAT1023'][sInd:nRead+sInd]) # lattitude of waveform bottom
    # close file
    f.close()

    # convert the above for ease
    lon=(lon0+lon1023)/2.0
    lat=(lat0+lat1023)/2.0

    # stop lon from wrappinh
    lon[lon>180]-=360

    # subset area of interest
    useInd=np.where((lon>=minX)&(lon<=maxX)&(lat>=minY)&(lat<=maxY))[0]
    waves=waves[useInd]
    lon=lon[useInd]
    lat=lat[useInd]
    lZN=lZN[useInd]
    lZ0=lZ0[useInd]
    lfid=lfid[useInd]
    lShot=lShot[useInd]

    nWaves=lon.shape[0]
    print("Now have",nWaves)

    # return arrays to initialiser
    return(waves,lon,lat,nWaves,nBins,lZN,lZ0,lfid,lShot)


  ###########################################

  def setElevations(self):
    '''
    Decodes LVIS's RAM efficient elevation
    format and produces an array of
    elevations per waveform bin
    '''
    self.z=np.empty((self.nWaves,self.nBins))
    for i in range(0,self.nWaves):    # loop over waves
      res=(self.lZ0[i]-self.lZN[i])/self.nBins
      self.z[i]=np.arange(self.lZ0[i],self.lZN[i],-1.0*res)   # returns an array of floats


  ###########################################

  def getOneWave(self,ind):
    '''
    Return a single waveform
    '''
    return(self.z[ind],self.waves[ind])


###########################################

