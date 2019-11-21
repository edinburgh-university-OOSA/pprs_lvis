
'''
Examples of the basic aspects of python3
'''

# Comments can be behind "#"
'''Or behind three quotation marks'''
# use # for comments in text, and ''' for descriptions of functions


# print something to the screen
print("Welcome to python3")


# set a variable. The variable will hold this value until you over-write it.
x=2.718281828459045


# write variable to screen
print(x)


# set a "string", ie a word. Note we have overwritten "x" set earlier and changed it from a number to a word
x="This is a word"


# print a string variable to the screen
print(x)


# Multiple variables can be printed out
x=2.718281828459045
y=6.52
z="a note"
print(z,x,y)


# basic maths can be done in python
x=2.718281828459045
y=3.2
z=x*y
print(x,"times",y,"equals",z)


'''
Packages
'''

# There are different packages in python for problem solving
# to bring in a package, import it
import math


# the "math" tools will be available by calling math.tool(), eg:
x=3.1415/2.0
y=math.sin(x)
print(y)


# if we only want certain parts of a package, or we don't want to write "math." each time, we can import parts of it
from math import sin,cos,exp
x=3.1415/2.0
y=sin(x)


# we can also rename packages as we import them, eg to save typing
import numpy as np


# Play with these features until you have the basics.
# Then move on to lesson 2, lists and arrays


