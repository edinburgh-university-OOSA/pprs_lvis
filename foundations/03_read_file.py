

'''
Intro to reading a file
'''

# Python can read just about any data format

# eg. numbers from a csv file
import numpy as np

filename='practice_data.csv'
x,y=np.loadtxt(filename,delimiter=',',unpack=True,dtype=float,comments="#")


# we can do rapid statistics on this using built in tools of numpy
meanY=np.mean(y)
minY=np.min(y)
maxY=np.max(y)
stdevY=np.std(y)
print("Statistics for y are")
print("Mean",meanY)
print("Min",minY)
print("Max",maxY)
print("Standard deviation",stdevY)


# as well as the maths from the last lesson


# Our data today will be in either HDF5 or geotiff format. More on this later


