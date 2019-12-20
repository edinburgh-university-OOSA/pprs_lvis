

'''
Intro to loops, funcitons and ifs
'''



# So far we have written "monolithic" code. We can create reusable chunks of code called "functions".
# We have already been using these from some packages (eg plt.plot()), but can create our own.

# to create a function, define it, the populate it with commands with a set number of indentations

def myFunc(x):   # function name and input variables
  '''Describe the function here'''
  y=x*x       # do some analysis
  return(y)   # pass the results back

# here we have defined the function. It has not run# To run, we must call it

x=2
res=myFunc(x)
print("The result of",x,"is",res)

# It is good practice to group all commands in to functions. These can even be embedded in "objects" along with their data
# more on that in OOSA.




'''
Loops
'''

# The real power of a computer comes from its ability to perform repetative tasks quickly
# we can "loop" over a set of tasks, repeating them one by one

# simple loop

for i in range(0,10):
  print(i)



# let us read in some data

import numpy as np

def readData(filename):
  '''A function to read some data'''
  x,y=np.loadtxt(filename,delimiter=',',unpack=True,dtype=float,comments="#")
  return(x,y)

x,y=readData('practice_data.csv')



# write out our elements, one by one

for i in range(0,len(x)):
  print(x[i],y[i])


# here, i is an index, varying from 0 to the end of the element
# range() is a command to produce a list of numbers between 0 and len(x)
# len(x) is a command to return the length of array x


# we can also get the computer to decide what to do based on the value of a variable with an "if"

z=0.34
if(z>0.5):
  print("z is bigger than 0.5",z)
else:
  print("z is smaller than 0.5",z)



# eg, only print values more than 2 stdandard deviations from the mean
meanY=np.mean(y)
stdevY=np.std(y)
# set thresholds
minThresh=meanY-2*stdevY
maxThresh=meanY+2*stdevY

# only write those values
for i in range(0,len(x)):
  if( (y[i]<minThresh) | (y[i]>maxThresh)):
    print(x[i],y[i])



# Ifs

# An if statement lets us control the flow of a program, allowing it to do different things in different conditions.
# This allows our program to make "decisions", making it more flexible


# example of an if statement

x=0.4           # a value we will use to test
threshold=0.5   # a threshold against which we will test

if(x<threshold):   # the test
  print(x,"is less than",threshold)   # if the test is passed, do this
else:              # if the test fails
  print(x,"is greater than or equal to",threshold) # otherwise do this

# python has a datatype called "booleab" for doing this

testPar=True

if(testPar):
  print("It is true")
else:
  print("It is false")


# we can stack if statements using "else if" statement, "elif"


x=0.4
thresh1=0.25   # a threshold against which we will test
thresh2=0.5   # a threshold against which we will test
thresh3=0.75   # a threshold against which we will test

if(x<thresh1):   # the test
  print(x,"is less than",thresh1)   # if the test is passed, do this
elif(x<thresh2):   # otherwise this test
  print(x,"is less than",thresh2)   # if the test is passed, do this
elif(x<thresh3):   # otherwise this test
  print(x,"is less than",thresh3)   # if the test is passed, do this
else:              # if the test fails
  print(x,"is greater than or equal to",thresh3) # otherwise do this


# We have covered the basic aspects of python. We can now try applying them to some remote sensing data.

