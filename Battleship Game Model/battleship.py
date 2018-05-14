# Justin Staples
# 001052815
# staplejw

from boardADT import *

class Battleship:

	p1 = None
	p2 = None

	@staticmethod
	def init(r, c):
		if not (r > 0 and c > 0):
			raise InvalidSizeException("dimensions must be greater than 0")
		Battleship.p1 = BoardT(r, c, True)
		Battleship.p2 = BoardT(r, c, False)

	@staticmethod
	def player1():
		return Battleship.p1

	@staticmethod
	def player2():
		return Battleship.p2
