
'''
An example script to 
create some data
'''

import numpy as np

# set the output name
filename='practice_data.csv'


# set array length
numb=1000


# make Gaussian random numbers
y=np.random.normal(loc=42.0,scale=10.0,size=numb)

# make indices
x=np.arange(numb)


# combine datasets
z=np.empty((numb,2))
z[:,0]=x
z[:,1]=y


# write
np.savetxt(filename,z,fmt="%.5f",delimiter=",",newline='\n')

