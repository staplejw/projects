## @file pointADT.py
#  @title pointADT
#  @author Justin Staples
# staplejw 
# 001052815

import math

## @brief This class represents a 2D point.
#  @details This class represents a two-dimensional point
#  as an abstract data type. The point is characterized 
#  with an 'x' and 'y' coordinate. 
class PointT:
    ## @brief This is the constructor for PointT
    #  @details The constructor takes in two parameters. 'x'
    #  and 'y' serve as the coordinates for the point.
    #  @param x x-coordinate of the point.
    #  @param y y-coordinate of the point.
	def __init__(self, x, y):
		self.xc = x
		self.yc = y

	## @brief Getter method for the x-coordinate.
	#  @return Returns the x-coordinate of an intance of PointT.
	def xcrd(self):
		return self.xc

	## @brief Getter method for the y-coordinate.
	#  @return Returns the y-coordinate of an intance of PointT.
	def ycrd(self):
		return self.yc

	## @brief A method for calculating the distance between two instances 
	#  of PointT.
	#  @details Uses the x-coordinates and y-coordinates of both points, 
	#  along with the pythagorean theorem, to find the distance between 
	#  points.
	#  @param p Distance requires two instance of PointT to calculate the
	#  distance, and p serves as the second point.
	#  @return The distance bewteen the two points.
	def dist(self, p):
		return math.sqrt((self.xc - p.xcrd())**2 + (self.yc - p.ycrd())**2)

	## @brief Rotates the point around the origin (0, 0)
	#  @details Uses the transition matrix for rotation to rotate the 
	#  @param phi The angle of rotation, given in radians.
	def rot(self, phi):
		temp1 = self.xc
		temp2 = self.yc
		self.xc = math.cos(phi)*temp1 - math.sin(phi)*temp2
		self.yc = math.sin(phi)*temp1 + math.cos(phi)*temp2
		