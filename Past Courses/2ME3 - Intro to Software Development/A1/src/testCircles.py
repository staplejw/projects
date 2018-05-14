## @file testCircles.py
#  @title Tests
#  @author Justin Staples
#  @details This file contains a series of tests for all the methods
#  in CircleADT.py and Statistics.py modules. Each method has at least
#  one test case. For the most part, I decided to pick basic test cases 
#  which can outline that the core function of each method was implemented
#  properly. For certain methods, I picked a few extra cases which test 
#  'interesting' behaviour such as calculating the area of a circle with 
#  radius = 0, or ranking lists of circles... When this module is
#  interpreted, all of the tests run automatically, and each one is asserted
#  True or False, based on the expected values. In all cases, the desired
#  assertion is True (I realize that some outputs for boolean values are 
#  expected to be False, but this module checks that False == False, and 
#  will print True). All of the tests print to the terminal and show the 
#  input, expected output and result. For the tests that I have chosen, all
#  assert to True, which gives at least some indication that the other 
#  modules were implemented properly. I will give a more detailed explanation
#  all the tests in my report.

from CircleADT import *
from Statistics import *

print "----------------------------"
test = [CircleT(1, 2, 3), CircleT(-1.7, 2.3, 0)]
print "testing constructor/accessors:"
print "TEST: CircleT(1, 2, 3), EXPECTED: x = 1, y = 2, r = 3"
print test[0].xcoord() == 1, test[0].ycoord() == 2, test[0].radius() == 3
print "TEST: CircleT(-1.7, 2.3, 0), EXPECTED: x = -1.7, y = 2.3, r = 0"
print test[1].xcoord() == -1.7, test[1].ycoord() == 2.3, test[1].radius() == 0 
print "----------------------------"

test = [CircleT(3, 4, 0), CircleT(2, 8, 10)]
print "testing area:"
print "TEST: CircleT(3, 4, 0), EXPECTED: area = 0"
print test[0].area() == 0
print "TEST: CircleT(2, 8, 10), EXPECTED: area = (math.pi)*(10**2) = 314.159..."
print test[1].area() == (math.pi)*(10**2)
print "----------------------------"

test = CircleT(0, 0, 1)
print "testing insideBox:"
print "TEST: CircleT(0, 0, 1), box parameters given by [-5, 5, 1, 1] EXPECTED: False"
print test.insideBox(-5, 5, 1, 1) == False
print "TEST: CircleT(0, 0, 1), box paramaters given by [-2, 2, 4, 4] EXPECTED: True"
print test.insideBox(-2, 2, 4, 4) == True
print "TEST: CircleT(0, 0, 1), box paramaters given by [-1, 1, 2, 2] EXPECTED: True"
print test.insideBox(-1, 1, 2, 2) == True
print "----------------------------"

test = [CircleT(0, 0, 1), CircleT(-1, 0, 1), CircleT(2, 0, 1)]
print "testing intersect:"
print "TEST: CircleT(0, 0, 1) and CircleT(1, 0, 1), EXPECTED: True"
print test[0].intersect(test[1]) == True
print "TEST: CircleT(0, 0, 1) and CircleT(2, 0, 1), EXPECTED: True"
print test[0].intersect(test[2]) == True
print "TEST: CircleT(-1, 0, 1) and CircleT(2, 0, 1), EXPECTED: False"
print test[1].intersect(test[2]) == False
print "----------------------------"

test = CircleT(2, -1, 6)
test.scale(3)
print "testing scale:"
print "TEST: CircleT(2, -1, 6), k = 3, EXPECTED: r = 6*3 = 18"
print test.r == 18
print "----------------------------"

test = CircleT(1, 6, 11)
test.translate(3, -4)
print "testing translate:"
print "TEST: CircleT(1, 6, 11), dx = 3, dy = -4, EXPECTED: x = 4, y = 2"
print test.x == 4, test.y == 2
print "----------------------------"

test = [CircleT(-1, -1, 3), CircleT(4, 4, 4), CircleT(7, 6, 5)]
print "testing average:"
print "TEST: circles with radii of 3, 4, 5, EXPECTED: average = 4"
print average(test) == 4
print "----------------------------"

print "testing stdDev:"
print "TEST: circles with radii of 3, 4, 5, EXPECTED: stdDev = 0.8165..."
print stdDev(test) == math.sqrt((((3.0-4)**2 + (4-4)**2 + (5-4)**2)/3))
print "----------------------------"

test_1 = [CircleT(1, 2, 6), CircleT(1, 2, 5), CircleT(1, 2, 11), CircleT(1, 2, 9)]
test_2 = [CircleT(1, 2, 6), CircleT(1, 2, 5), CircleT(1, 2, 11), CircleT(1, 2, 11)]
test_3 = [CircleT(1, 2, 9), CircleT(1, 2, 5), CircleT(1, 2, 11), CircleT(1, 2, 9)]
print "testing rank:"
print "TEST: circles with radii of [6, 5, 11, 9], EXPECTED: [3, 4, 1, 2]"
print rank(test_1) == [3, 4, 1, 2]
print "TEST: circles with radii of [6, 5, 11, 11], EXPECTED: [3, 4, 1, 1]"
print rank(test_2) == [3, 4, 1, 1]
print "TEST: circles with radii of [9, 5, 11, 9], EXPECTED: [2, 4, 1, 2]"
print rank(test_3) == [2, 4, 1, 2]