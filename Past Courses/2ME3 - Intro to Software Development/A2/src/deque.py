from circleADT import *

G = 6.672e-11

## @brief This class represents a double ended queue for cirlces.
#  @details This class represents a double ended queue for circles,
#  as an abstract object. The maximum size for the queue is 20 circles.
class Deq:

	# the maximum size of the queue is 20 circles.
	MAX_SIZE = 20

	# the state variable that is used to represent the queue is a list 
	s = []

	## @brief This is the initializer method the deque. 
	#  It initializes the queue to an empty queue.
	@staticmethod
	def init():
		Deq.s = []

	## @brief This method will push an instance of CircleT to the 
	#  the back of the queue.
	#  @param c This instance of CircleT will be pushed to the back of the queue.
	@staticmethod
	def pushBack(c):
		if (len(Deq.s) == Deq.MAX_SIZE):
			raise FULL("The queue is full, maximum size cannot be exceeded")
		back = [c]
		Deq.s = Deq.s + back

	## @brief This method will push an instance of CircleT to the 
	#  the front of the queue.
	#  @param c This instance of CircleT will be pushed to the front of the queue.
	@staticmethod
	def pushFront(c):
		if (len(Deq.s) == Deq.MAX_SIZE):
			raise FULL("The queue is full, maximum size cannot be exceeded")
		front = [c]
		Deq.s = front + Deq.s

	## @brief This method will remove the instance of CircleT
	#  at the very back of the queue.
	@staticmethod
	def popBack():
		if (len(Deq.s) == 0):
			raise EMPTY("The queue is empty")
		Deq.s = Deq.s[0:len(Deq.s) - 1]

	## @brief This method will remove the instance of CircleT
	#  at the very front of the queue.
	@staticmethod
	def popFront():
		if (len(Deq.s) == 0):
			raise EMPTY("The queue is empty")
		Deq.s = Deq.s[1:len(Deq.s)]

	## @brief This method can be used to access the back 
	#  element in the queue.
	#  @return Returns the backmost element in the queue.
	@staticmethod
	def back():
		if (len(Deq.s) == 0):
			raise EMPTY("The queue is empty")
		return Deq.s[len(Deq.s) - 1]

	## @brief This method can be used to access the front 
	#  element in the queue.
	#  @return Returns the frontmost element in the queue.
	@staticmethod
	def front():
		if (len(Deq.s) == 0):
			raise EMPTY("The queue is empty")
		return Deq.s[0]

	## @brief This method gives the current size of the 
	#  queue, by returning the number of elements in the queue.
	#  @return Returns the number of elements in the queue.
	@staticmethod
	def size():
		return len(Deq.s)

	## @brief This method determines if all the circle 
	#  currently in the queue are disjoint from eachother.
	#  @details Considers all possible pairs of circles from the
	#  queue and if none of the pairs intersect, then the whole set
	#  is considered disjoint. 
	#  @return Returns a boolean value. True if all the circles are
	#  disjoint and False otherwise.
	@staticmethod
	def disjoint():
		if (len(Deq.s) == 0):
			raise EMPTY("The queue is empty")		
		for i in range(0, len(Deq.s)):
			for j in range(0, len(Deq.s)):
				if i != j:
					if Deq.s[i].intersect(Deq.s[j]):
						return False
		return True 

	## @brief This method sums up all the x components
	#  of all the gravitational forces contributed by the 
	#  circles in the queue on the front circle (other than the
	#  front circle).
	#  @param f This is a function that takes in a real and returns
	#  a real. It passes this function to the force() method from 
	#  circleADT.py and uses the output of this function to find 
	#  the forces and the xcomponents from that. 
	#  @return Returns a single real, which is a sum of all the 
	#  xcomponents of all forces acting on the front circle.
	@staticmethod
	def sumFx(f):
		if (len(Deq.s) == 0):
			raise EMPTY("The queue is empty")
		xdelta = lambda ci: ci.c.xc - Deq.s[0].c.xc
		distance = lambda ci: ci.connection(Deq.s[0]).len()
		xcomp = lambda ci: ci.force(f)(Deq.s[0])*xdelta(ci)/distance(ci)
		return reduce(lambda x, y: x + y, map(xcomp, Deq.s[1:len(Deq.s)]), 0)

## @brief This in an exception class called FULL. 
#  It is thrown when the queue has reached its max size
#  and certain methods are called that would attempt to 
#  violate the state invariant. 
class FULL(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)

## @brief This in an exception class called EMPTY. 
#  It is thrown when the queue has a size of 0 and certain
#  methods are called. Many methods cannot return a value 
#  when the queue does not have any elements in it.
class EMPTY(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)

