## @file CircleADT.py
#  @title CircleADT
#  @author Justin Staples

import math

## @brief This class represents a circle.
#  @details This class represents a circle as abstract data type. 
#  The circle is characterized with a center point with x and y 
#  coordinates (x, y), and a radius, r.
class CircleT:
    ## @brief This is the constructor for CircleT
    #  @details The constructor takes in three parameters. Two are  
    #  for the center of the circle (x and y) and a third which 
    #  gives the radius.
    #  @param x x-coordinate of the center of the circle.
    #  @param y y-coordinate of the center of the circle.
    #  @param r the radius of the circle.
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    ## @brief Getter method for x-coordinate.
    #  @return Returns the x-coordinate of an intance of CircleT.
    def xcoord(self):
        return self.x

    ## @brief Getter method for y-coordinate.
    #  @return Returns the y-coordinate of an intance of CircleT.    
    def ycoord(self):
        return self.y

    ## @brief Getter method for the radius.
    #  @return Returns the radius of an intance of CircleT.
    def radius(self):
        return self.r

    ## @brief Method for calculating the area of an instance of CircleT.
    #  return Returns the area of an instace of CircleT.
    def area(self):
        return math.pi * self.r ** 2

    ## @brief Checks to see if an instance of CircleT is in
    #  side of a rectangular box.
    #  @details This method will calculate a range of values that the 
    #  center of the circle is allowed to be in, given it's radius. Points 
    #  of the circle that lie on the edge of the box are OK.
    #  @param x0 X-coordinate of the left side of the box.
    #  @param y0 Y-coordinate of the top side of the box.
    #  @param w Width of the box.
    #  @param h Height of the box.
    #  @return The function returns a boolean value. True, if the center
    #  of the circle is within the correct range, and False otherwise.
    def insideBox(self, x0, y0, w, h):
        upper_x = x0 + w - self.r
        lower_x = x0 + self.r
        upper_y = y0 - self.r
        lower_y = y0 - h + self.r
        if (lower_x <= self.x <= upper_x) and (lower_y <= self.y <= upper_y):
            return True
        else:
            return False

    ## @brief Checks to see if two instances of CircleT intersect eachother.
    #  @details The function will do a check to see how far away the two 
    #  circles center's are away from eachother. This will get compared to the
    #  sum of the radii to see if the two circles share any points in common.
    #  @param c Another instance of CircleT to test with.
    #  @return The function returns a boolean value. True, if the circles share
    #  any common points (even just one), and False otherwise. That is to say,
    #  I have made the assumption that intersection is satisfied with just one 
    #  point, and the method uses the <= operator to allow this.
    def intersect(self, c):
        dist = math.sqrt((self.x - c.x) ** 2 + (self.y - c.y) ** 2)
        if (dist <= self.r + c.r):
            return True
        else: 
            return False

    ## @brief Scales the radius of an instance of CircleT by a factor, k.
    #  @param k The scale factor.
    def scale(self, k):
        self.r = k * self.r
    
    ## @brief Translates an instance of CircleT .
    #  @details The circle will be translated 'dx' units along the x-axis
    #  and 'dy' units along the y-axis.
    #  @param dx Determines how much the circle will be translated along the 
    #  x-axis.
    #  @param dy Determines how much the circle will be translated along the 
    #  y-axis.
    def translate(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy