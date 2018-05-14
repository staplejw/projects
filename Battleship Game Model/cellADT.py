# Justin Staples
# 001052815
# staplejw

# This class represents an abstract data type for a single cell 
# of the game board
class CellT:

	def __init__(self):
		self.shipID = -1
		self.shot = False

	def getShipID(self):
		return self.shipID

	def getShot(self):
		return self.shot

	def setShipID(self, i):
		if not (0 <= i <= 4):
			raise InvalidShipIdException("invalid ship id")
		self.shipID = i

	def setShot(self, b):
		self.shot = b

class InvalidShipIdException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)
