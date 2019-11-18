

'''
Basics of lists and 
arrays in python3
'''


# We can also store lists of things in a single variable
x=[1,2,3,4,5]

# This can be used to pass around large amounts of data without needing thousands of variables
print(x)

# it can be accessed by telling pythong with "element" you want
print(x[0])


# we can also count from the back
print(x[-1])
print(x[-2])


# Note that the elements start from "0" and go, in this case, to 4.
print(x[0],x[4])


# we can reassign elements one by one
x[2]=4.243546
print(x)


# or overwrite the whole thing
x=[4,3,2,1]


# lists can be of any type
x=["This","is","now","a","string"]


# or even a mix
x=[1,2,"sausage",4,5]
print(x)


# there are many other ways to hold large amounts of data in pythom., eg. dictionaries and tuples
# but lists are perhaps the most common

# in GIS and EO, we often want to hold large arrays of numbers
# this can be efficiently done using a "numpy" array, which have
# been specifically designed for this. Import numpy

import numpy as np


# set some data (most often we will read from file)
x=np.array([4,3,2,1])


# It can be accessed in a similar way to lists
print(x[0],x[2])


# but now we can perform maths on the whole array
y=x/2
print("original",x,"modified",y)



# SLICES: We can access sections of an array using the slice feature
x=np.arange((100))  # make an array of 1 to 99

# write of the 4th to 20th elements
print(x[4:21])

# write out the first ten elements
print(x[:10])

# write out the last ten elements
print(x[-10:])

# write out a chosen set of elements
chosen=[12,15,35,2,80,-4]
print(x[chosen])


# arrays can also be multi-dimensional. Let us make one full of "-1"
x=np.full((100,100),-1)

# the "np.full()" command tells it to make an array full of a given value
# the "(100,100)" tells it to make it 100*100 elements
# the "-1" tells it what value to fill the array with


# Now we can store large amounts of data in a single variable. Let us see how we can analyse that

