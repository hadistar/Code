'''
IoT·인공지능·빅데이터 개론 및 실습 (M2177.004900_001)
3/8 Basics of Python, Numpy, and Matplotlib
Adapted by Seonwoo Min from the IPython version of the CS231n Python tutorial (http://cs231n.github.io/python-numpy-tutorial/).

In this excercise, we will cover:

Basic Python: List, Dictionary, Function, Class
Numpy: Array, Array indexing, Array math
Matplotlib: Plotting, Subplot
'''
'''
1. Basic Python
List
A list is the Python equivalent of an array, but is resizeable and can contain elements of different types
'''

#############################################################
# General Usage
#############################################################
xs = [3, 1, 2]

# Print the last indice
# Negative indices count from the end of the list
print(xs[-1])

# Add a new element to the end of the list
xs.append('bar')
print(xs)

# Remove and return the last element of the list
x = xs.pop()
print(x, xs)

#############################################################
# Slicing//
#############################################################
# Create a list containing [0, 1, 2, 3, 4, 5]
# range is a built-in function that creates a list of integers
nums = list(range(5))
print(nums)

# Get a slice from index 2 to 4 (exclusive); prints "[2, 3]"
print(nums[2:4])

# Get a slice from index 2 to the end; prints "[2, 3, 4]"
print(nums[2:])

# Get a slice from the start to index 2 (exclusive); prints "[0, 1]"
print(nums[:2])

# Get a slice of the whole list; prints ["0, 1, 2, 3, 4]"
print(nums[:])

# Assign a new sublist to a slice; change nums into [0, 1, 8, 9, 4]
nums[2:4] = [8, 9]
print(nums)

#############################################################
# Loop & Enumerate
#############################################################
animals = ['cat', 'dog' 'monkey']

# Loop over and print the elements of the list:
for animal in animals:
    print(animal)


# Loop over and print the index and value of each elements of the list:
for idx, animal in enumerate(animals):
    print('#%d: %s' % (idx + 1, animal))


#############################################################
# List comprehensions
#############################################################
nums = [0, 1, 2, 3, 4]
squares = []
for x in nums:
    squares.append(x ** 2)
print(squares)


# Make this code simpler using a list comprehension
squares = [x ** 2 for x in nums]
print(squares)

# Make a list of squares of even numbers in the list
# List comprehensions can also contain conditions
even_squares = [x ** 2 for x in nums if x % 2 == 0]
print(even_squares)

'''
Dictionary
A dictionary stores (key, value) pairs
'''
#############################################################
# General Usage
#############################################################
# Create a dictionary containing the followings key:value pairs
# cat:cute  /  dog:furry
d = {'cat': 'cute', 'dog': 'furry'}

# print an entry 'cat' from a dictionary; prints 'cute'
print(d['cat'])

# Add another key:value pair
# fish:wet
d['fish'] = 'wet'

# Get an element with a default; prints "N/A" if not exists
# fish / monkey
print(d.get('fish', 'N/A'))
print(d.get('monkey', 'N/A'))

# Remove 'fish' from the dictionary
del d['fish']
print(d)

#############################################################
# Loop & Dictionary comprehensions
#############################################################
d = {'person': 2, 'cat': 4, 'spider': 8}

# Loop over keys of the dictionary
# Access the values with the keys
for animal in d:
    legs = d[animal]
    print('A %s has %d legs' % (animal, legs))

# Loop over keys and values of the dictionary
for animal, legs in d.items():
    print('A %s has %d legs' % (animal, legs))


# Make a dictionary of key:squares of even numbers in the list
# Dictionary comprehensions can also contain conditions
nums = [0, 1, 2, 3, 4]
even_num_to_square = {x: x ** 2 for x in nums if x % 2 == 0}
print(even_num_to_square)


'''
Function
Python functions are defined using the def keyword
'''

#############################################################
# General Usage
#############################################################
# Define a function called sign with argument <x>
# print 'positive' if x > 0
# print 'negative' if x < 0
# print 'zero' if x = 0
def sign(x):
    if x > 0:
        return 'positive'
    elif x < 0:
        return 'negative'
    else:
        return 'zero'

for x in [-1, 0, 1]:
    print(sign(x))


#############################################################
# Optional keyword argument
#############################################################
# Define a function called hello takes
# arguement <name>
# optional argument <loud> with default value False
# print "HELLO, [name in large letter]" if loud = True
# print "HELLO, [name in given form]" if loud = False
def hello(name, loud=False):
    if loud:
        print('HELLO, %s' % name.upper())
    else:
        print('Hello, %s!' % name)


hello('Bob')
hello('Fred', loud=True)


'''
Class
Python classes are defined using the class keyword
'''
#############################################################
# General Usage
#############################################################
# Define a function called Greeter
# initialize its variable <name> with default value "Alice"
# Define its function <greet> say hello as in the Function example
class Greeter:
    def __init__(self, name = 'Alice'):
        self.name = name

    def greet(self, loud=False):
        if loud:
            print('HELLO, %s!' % self.name.upper())
        else:
            print('Hello, %s' % self.name)

g1 = Greeter('Fred')
g1.greet()
g1.greet(loud=True)

g2 = Greeter()
g2.greet()
g2.greet(loud=True)

'''
2. Numpy
'''

'''
Array
A numpy array is a grid of values, all of the same type, and is indexed by a tuple of nonnegative integers.
'''
# Create an 2-by-2 array of all zeros
a = np.zeros((2,2))
print(a)

# Create an 2-by-2 array of all ones
a = np.ones((2,2))
print(a)

# Create an 2-by-2 array with random numbers
a = np.random.random((2,2))
print(a)

# Create an 1-by-6 array with elements 1 to 6
a = np.array([1, 2,3 , 4, 5, 6])
print(a)

#Create a rank 2 array with elements 1 to 6
b = np.array([[1,2,3],[4,5,6]])
print(b)

# print shape of the array
print(b.shape)

# print the element in the 1 in 1st index and 0 in 2nd index
print(b[1][0])

'''
Array indexing
Since arrays may be multidimensional, you must specify a slice for each dimension of the array
'''
# Create an 3-by-4 array with elements 1 to 12
# Use reshape
a = np.arange(1,13).reshape(3,4)
print(a)

# Use slicing to pull out the subarray consisting of the first 2 rows and columns 1 and 2;
# and modify [0, 0] element of the array b into 0
b = a[:2, 1:3]
print(b)
b[0,0] = 0
print(b[0,0], a[0, 1])
b[0,0] = 2 # reset

# Instead create an array with the subarray consisting of the first 2 rows and columns 1 and 2;
# and modify [0, 0] element of the array b into 0
b = np.array(a[:2, 1:3]) //
print(b)
b[0,0] = 0
print(b[0,0], a[0, 1])

# Get the [0, 2, 0, 1] indices from each row of a matrix: [0,0], [1,2], [2,1]
indices = np.array([0, 2, 1])
print(a[np.arange(3), indices])

# Add 10 to the [0, 2, 0, 1] indices from each row of a matrix
a[np.arange(3), indices] += 10
print(a)

'''
Array math
Basic mathematical functions operate elementwise on arrays, and are available both as operator overloads and as functions in the numpy module
'''

#############################################################
# General Usage
#############################################################
x = np.array([[1,2],[3,4]], dtype=np.float64)
y = np.array([[5,6],[7,8]], dtype=np.float64)

# Elementwise product of x and y
z = x * y
print(z)

#############################################################
# General Usage
#############################################################
x = np.array([[1,2],[3,4]], dtype=np.float64)
y = np.array([[5,6],[7,8]], dtype=np.float64)

# Elementwise product of x and y
z = x * y
print(z)

# Compute sum of all elements in x
z = np.sum(x)
print(z)

# Compute sum of each column in x;
z = np.sum(x, axis=0)
print(z)

# Compute sum of each row in x
z = np.sum(x, axis=1)
print(z)

#############################################################
# Broadcasting
#############################################################
x = np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]])
v = np.array([1, 0, 1])
y = np.empty_like(x)

# Add the vector v to each row of the matrix x with an explicit loop
for i in range(4):
    y[i, :] = x[i, :] + v
print(y)

# Add the vector v to each row of the matrix x with stacking v multiple times
vv = np.tile(v, (4, 1))
y = x + vv
print(y)

# Add the vector v to each row of the matrix x with broadcasting
y = x + v
print(y)

# Multiply matrix x by a constant 2:
z = x * 2
print(z)

'''
3. Matplotlib
Matplotlib is a plotting library. In this section give a brief introduction to the matplotlib.pyplot module.
'''

import matplotlib.pyplot as plt

'''
Plotting
The most important function in matplotlib is plot, which allows you to plot 2D data. Here is a simple example:
'''
# Compute the x and y coordinates for points on a sine curve
x = np.arange(0, 3 * np.pi, 0.3) // np.pi는 파이이다
y = np.sin(x)

# Plot the points using matplotlib
plt.plot(x, y, 'o-', c='b'    )

# Plot the points using matplotlib
plt.plot(x, y, 'o')

# Plot the points using matplotlib
plt.plot(x, y, '-o')

y_sin = np.sin(x)
y_cos = np.cos(x)

# Plot the points using matplotlib
plt.plot(x, y_sin)
plt.plot(x, y_cos)
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.title('Sine and Cosine')
plt.legend(['Sine', 'Cosine'])

'''
Subplots
You can plot different things in the same figure using the subplot function. Here is an example:
'''

# Compute the x and y coordinates for points on sine and cosine curves
x = np.arange(0, 3 * np.pi, 0.1)
y_sin = np.sin(x)
y_cos = np.cos(x)

# Set up a subplot grid that has height 2 and width 1,
# and set the first such subplot as active, and make the first plot.
plt.subplot(2, 1, 1)
plt.plot(x, y_sin)
plt.title('Sine')

# Set the second subplot as active, and make the second plot.
plt.subplot(2, 1, 2)
plt.plot(x, y_cos)
plt.title('Cosine')

# Show the figure.
plt.show()