

'''
Examples of plotting
'''


# Often we need to visualise data
# python has a very useful plotting package

import matplotlib.pyplot as plt


# let us read some data in.

import numpy as np
filename='practice_data.csv'
x,y=np.loadtxt(filename,delimiter=',',unpack=True,dtype=float,comments="#")


# set the labels
plt.xlabel('x')
plt.ylabel('y')

# tell it which data to plot, and what format. '.' means point
plt.plot(x,y,'.')

# print to screen
plt.show()

# plot with a line
plt.plot(x,y)
plt.show()


# clear everything so we can start a new plot
plt.clf()


# plot to a file, so we can include iun report etc.
filename="a_plot.png"   # pick a filename

plt.xlabel('x')
plt.ylabel('y')
plt.plot(x,y,'.')
plt.savefig(filename) # write the graph to a file
plt.close()           # close the file
plt.clf()             # clear everything so we can start a new plot


# there are many many more options for plotting.
# See online documentation for full details

# eg. a histrogram

# make a histogram of the data
hist=np.histogram(y,bins=20)

# this makes a 2D array of the data.
# hist[0] contains the frequency of occurance
# hist[1] contains the divisions between each bin, so is 1 longer than hist[0]

# we want the mean of each bin, so move to a numpy array to allow this
pY=np.array(hist[0])
histX=np.array(hist[1])
pX=(histX[0:-1]+histX[1:])/2  # note we are using slices to get the arrays to the same length

filename="a_histogram.png"
plt.xlabel('y')
plt.ylabel('Frequency')
plt.plot(pX,pY)
plt.savefig(filename)
plt.close()
plt.clf()

# now on to functions and loops...

