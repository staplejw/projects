## @file circleADT.py
#  @title circleADT
#  @author Justin Staples
# staplejw 
# 001052815

from lineADT import *


## @brief This class represents a circle.
#  @details This class represents a circle
#  as an abstract data type. The circle is characterized
#  with a center point and radius.  
class CircleT:
	## @brief This is the constructor for CircleT
    #  @details The constructor takes in two parameters. 'cin'
    #  is the point that represents the center of the circle
    #  and 'rin' serve as the beginning and end of the line.
    #  @param cin The center point of the circle.
    #  @param rin The radius of the circle.
	def __init__(self, cin, rin):
		self.c = cin
		self.r = rin

	## @brief Getter method for the center point.
	#  @return Returns the center point of an instance of CircleT.
	def cen(self):
		return self.c

	## @brief Getter method for the radius.
	#  @return Returns the radius of an instance of CircleT.
	def rad(self):
		return self.r


	## @brief A method for calculating the area of a circle.
	#  @details Uses the formula for area of a circle.
	#  @return Returns the area of the circle.
	def area(self):
		return math.pi * self.r ** 2

	## @brief A method for determining if two circles intersect.
	#  @details Uses the distance between the circles and
	#  the radii of the circle to determine if two circles
	#  share any common points.
	#  @param ci This circle acts as the circle to compare to 
	#  test for intersection.
	#  @return Returns a boolean value. True if the circles 
	#  intersect and False otherwise.
	def intersect(self, ci):
		return self.cen().dist(ci.cen()) <= (self.rad() + ci.rad())

	## @brief A method for creating a connection line between
	#  the centers of two circles.
	#  @details Creates a line that where the beginning and end
	#  points are determined by the center points of each circle.
	#  @param ci This cirlce will be the circle that is connected to self.
	#  @return Returns an instance of LineT, where the beginning 
	#  and end points are given by the centers of the circle.
	def connection(self, ci):
		return LineT(self.cen(), ci.cen())

	## @brief This method creates a function that can be used
	#  to calculate the graviational force between two circles.
	#  @param f This function takes in a real as an argument and
	#  returns a real. This function is used to replace the 1/r**2
	#  term in universational law of gravitation, letting the user
	#  create custom functions for gravitational force.
	#  @return Returns the gravitational force between two instances 
	#  CircleT, using the area of the circles as masses and the input
	#  function f. 
	def force(self, f):
		return lambda x: self.area() * x.area() * f(self.connection(x).len())
