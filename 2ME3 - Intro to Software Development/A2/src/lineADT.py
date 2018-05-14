## @file lineADT.py
#  @title lineADT
#  @author Justin Staples
# staplejw 
# 001052815

from pointADT import *

## @brief This class represents a line.
#  @details This class represents a two-dimensional line
#  as an abstract data type. The line is characterized 
#  with two points, a beginning and and end. 
class LineT:
	## @brief This is the constructor for LineT
    #  @details The constructor takes in two parameters. 'p1'
    #  and 'p2' serve as the beginning and end of the line.
    #  @param p1 The beginning point of the line.
    #  @param p2 The end point of the line.
	def __init__(self, p1, p2):
		self.b = p1
		self.e = p2

	## @brief Getter method for the beginning point.
	#  @return Returns the beginning point of an instance of LineT.
	def beg(self):
		return self.b

	## @brief Getter method for the end point.
	#  @return Returns the end point of an instance of LineT.
	def end(self):
		return self.e

	## @brief A method for calculating the length of a line.
	#  @details Uses the 'dist' method defined in pointADT.
	#  @return The length of the line.
	def len(self):
		return self.beg().dist(self.end())

	## @brief A method for finding the midpoint of a line.
	#  @details Uses the 'dist' method defined in pointADT.
	#  @return The length of the line.
	def mdpt(self):
		xmid = (self.beg().xcrd() + self.end().xcrd())/2.0
		ymid = (self.beg().ycrd() + self.end().ycrd())/2.0
		return PointT(xmid, ymid)

	## @brief This method will rotate a line some angle around the origin.
	#  @details This method rotates the beginning and end points of the line,
	#  effectively rotating the whole line.
	#  @param phi The angle of rotation, given in radians.
	def rot(self, phi):
		self.beg().rot(phi)
		self.end().rot(phi)
		