## @file Statistics.py
#  @title Statistics
#  @author Justin Staples
#  @details This file contains three functions for analyzing
#  the radii of a list of circles. It is implemented as a library.

import numpy as np

## @brief This method calculates the average radius, given a list of 
#  circles.
#  @param list This is the input list of instances of CircleT.
#  @return The value that is returned is average radius of all the
#  circles in the list.
def average(list):
	x = np.zeros(len(list))
	for i in range(0, len(list)):
		x[i] = list[i].r
	return np.average(x)

## @brief This method calculates the standard deviation of the radii,
#  given a list of circles.
#  @param list This is input list of instances of CircleT.
#  @return The value that is returned is the standard deviation of 
#  the radii of all circles in the list.
def stdDev(list):
	x = np.zeros(len(list))
	for i in range(0, len(list)):
		x[i] = list[i].r
	return np.std(x)

## @brief This method ranks a list of circles according to their radius.
#  @details This method first uses the input list to create a new list 
#  with just the radii. Then, it iterates through this new list, and for
#  each element, checks how many elements in the list are larger than it.
#  The counter variable is initialized to 1. This is because I have assumed
#  that the lowest possible rank value is 1. I have also assumed that circles
#  with the same radii will receive the exact same rank, one below the next largest radius. After ranking 
#  elements that are part of a tie, the rank value will go back to normal (will 
#  jump values by at least 2 depending on how many elements are involved in the tie).
#  This is evident in my test cases for this method. 
#  @param list This is the input list of instances of CircleT.
#  @return The method return a list of integers with the same length as
#  the input list. Each element of the list gives a rank which corresponds
#  to the instance of CircleT with the same index.
def rank(list):
	x = []
	a = []
	for i in range(0, len(list)):
		x.append(list[i].r)
	for i in range(0, len(list)):
		rank = 1
		for j in range(0, len(list)):
			if (x[j] > x[i]):
				rank += 1
		a.append(rank)
	return a