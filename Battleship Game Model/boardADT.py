# Justin Staples
# 001052815
# staplejw

from cellADT import *

class BoardT:

	MAX_SHIPS = 5

	def __init__(self, rows, columns, turn):
		if not (rows > 0 and columns > 0):
			raise InvalidSizeException("dimensions must be greater than 0")
		self.r = rows
		self.c = columns
		self.s = [[CellT() for i in range(rows)] for j in range(columns)]
		self.myTurn = turn
		self.myShots = []
		self.shipCounter = 0

	def getCells(self):
		return self.s

	def placeShip(self, i, j, k, l):
		if not (0 <= i < self.r and 0 <= k < self.r and 0 <= j < self.c and 0 <= l < self.c):
			raise OutOfBoundsException("you cannot place a ship outside of the board")
		if i > k or j > l:
			raise InvalidShipException("indices i and j must be smaller than k and l")
		if not (k - i == 0 or l - j == 0):
			raise InvalidShipException("you cannot place a ship on a diagonal")
		if self.shipCounter == BoardT.MAX_SHIPS:
			raise InvalidShipException("there are already 5 ships on the board")
		for a in range(i, k + 1):
			for b in range(j, l + 1):
				if self.s[a][b].getShipID() >= 0:
					raise InvalidShipException("there is already a ship in this range")
		for a in range(i, k + 1):
			for b in range(j, l + 1):
				self.s[a][b].setShipID(self.shipCounter)
		self.shipCounter += 1

	def isMyTurn(self):
		return self.myTurn

	def changeTurn(self):
		self.myTurn = not self.myTurn

	def fireShot(self, i, j, b):
		if not (0 <= i < self.r and 0 <= j < self.c):
			raise OutOfBoundsException("you cannot fire a shot outside of the board")
		if b.getCells()[i][j].getShot():
			raise InvalidShotException("this cell has already been shot at")
		if b.isMyTurn():
			raise WrongPlayerException("its the other players turn")
		if not self.myTurn:
			raise WrongPlayerException("its not your turn")
		self.myShots = self.myShots + [[i, j]]
		self.myTurn = False
		b.getCells()[i][j].setShot(True)
		b.changeTurn()

	def pastShot(self, k):
		if not (0 <= k < len(self.myShots)):
			raise OutOfBoundsException("index out of range in past shots list")
		return self.myShots[k]

	def didItHit(self, k, b):
		if not (0 <= k < len(self.myShots)):
			raise OutOfBoundsException("index out of range in past shots list")
		return b.getCells()[self.myShots[k][0]][self.myShots[k][1]].getShipID() >= 0

	def isLoser(self):
		for i in range(self.r):
			for j in range(self.c):
				if (self.s[i][j].getShipID() >= 0 and not(self.s[i][j].getShot())):
					return False
		return True

	def progress(self, b):
		hits = 0
		ships = 0
		for i in range(b.r):
			for j in range(b.c):
				if (b.s[i][j].getShipID() >= 0 and b.s[i][j].getShot()):
					hits += 1
		for i in range(b.r):
			for j in range(b.c):
				if (b.s[i][j].getShipID() >= 0):
					ships += 1		
		return 100 * hits / ships

class InvalidSizeException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)

class OutOfBoundsException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)

class InvalidShipException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)

class InvalidShotException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)

class WrongPlayerException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return str(self.value)  
