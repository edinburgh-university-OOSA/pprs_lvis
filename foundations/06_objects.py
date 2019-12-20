

'''
An example of an object
'''


# Often we want to store groups of data together to make it easier to pass it around our program
# We may also want to define functions which we will only ever apply to these grouped datasets
# To allow this, sets of data and functions can be "encapsulated" in to a group, known as an object (also called a class)
# This is particularly useful as programs become larger, and makes them easier to manage.


# Much of the code we use is made up of classes.
# We do not need to create our own classes in this course
# But every package we use is a class, so having some
# insight in to what a class is will help us understand
# how to make use of these packages.


# define a new class

class testClass():
  '''
  This is a class to illustrate
  how classes work
  '''
  # This function is called when the class is first applied
  # it initialises the class
  def __init__(self,somedata,moredata):  # we pass two items to store in the class
    '''The class initialiser'''
    self.x=somedata  # here "self" is the instance of the clasa.s The "." means there is something inside that class
    self.y=moredata  # in this case, we have saved two pieces of data, x and y. We have already used the "." when using numpy etc.
  # a function we would like to use. "Self" contains the data
  def multiplyContents(self):
    '''Function to multiply the contents together'''
    z=self.x*self.y   # note that z is not in self, so is not saved after this function
    print("The multiplitcation of",self.x,"and",self.y,"is",z)



# call an instance of that class
class1=testClass(3,4)   # this calls __init__ and passes 3 and 4 to be saved as x and y

# call the function
class1.multiplyContents()

# we can directly access the data too
print("Data within is",class1.x,class1.y)

# We can create a separate instance of the class, which will be independent from class1
class2=testClass(10,42)   # this calls __init__ and passes 3 and 4 to be saved as x and y


# to prove they are independent
class1.multiplyContents()
class2.multiplyContents()

# we will be using lots of packages that contain classes
# For example, there is a class to store and manipulate geotiff remote sensing files

