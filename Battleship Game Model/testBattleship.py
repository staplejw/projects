# Justin Staples
# 001052815
# staplejw

from battleship import *
import unittest

class cellTests(unittest.TestCase):

	def setUp(self):
		self.c1 = CellT()

	def tearDown(self):
		self.c1 = None

	def test_getShipID(self):
		self.assertTrue(self.c1.getShipID() == -1)

	def test_getShot(self):
		self.assertTrue(self.c1.getShot() == False)

	def test_setShipID(self):
		self.c1.setShipID(2)
		self.assertTrue(self.c1.getShipID() == 2)
		self.assertRaises(InvalidShipIdException, self.c1.setShipID, 10)


	def test_setShot(self):
		self.c1.setShot(True)
		self.assertTrue(self.c1.getShot() == True)

class boardTest(unittest.TestCase):

	def setUp(self):
		self.b1 = BoardT(10, 10, True)
		self.b2 = BoardT(10, 10, False)


	def tearDown(self):
		self.b1 = None
		self.b2 = None

	def test_BoardT(self):
		self.assertRaises(InvalidSizeException, BoardT, -1, 3, True)

	def test_getCells(self):
		self.assertTrue(self.b1.getCells()[3][4].getShipID() == -1 and self.b1.getCells()[3][4].getShot() == False)

	def test_placeShip(self):
		self.b1.placeShip(0, 0, 0, 2)
		self.assertTrue(self.b1.getCells()[0][1].getShipID() == 0)
		self.assertTrue(self.b1.shipCounter == 1)
		self.assertRaises(OutOfBoundsException, self.b1.placeShip, -1, 0, 0, 0)
		self.assertRaises(InvalidShipException, self.b1.placeShip, 1, 2, 0, 0)

	def test_isMyTurn(self):
		self.assertTrue(self.b1.myTurn)
		self.assertFalse(self.b2.myTurn)

	def test_changeTurn(self):
		self.b1.changeTurn()
		self.assertFalse(self.b1.myTurn)

	def test_fireShot(self):
		self.b1.fireShot(0, 0, self.b2)
		self.assertTrue(self.b1.myShots[0] == [0, 0])
		self.assertFalse(self.b1.myTurn)
		self.assertTrue(self.b2.getCells()[0][0].getShot())
		self.assertTrue(self.b2.myTurn)
		self.assertRaises(WrongPlayerException, self.b1.fireShot, 1, 1, self.b2)
		self.b2.fireShot(0, 0, self.b1)
		self.assertRaises(InvalidShotException, self.b1.fireShot, 0, 0, self.b2)

	def test_pastShot(self):
		self.b1.fireShot(3, 4, self.b2)
		self.assertTrue(self.b1.pastShot(0) == [3, 4])
		self.assertRaises(OutOfBoundsException, self.b1.pastShot, 3)

	def test_didItHit(self):
		self.b1.fireShot(3, 4, self.b2)
		self.assertFalse(self.b1.didItHit(0, self.b2))
		self.assertRaises(OutOfBoundsException, self.b1.didItHit, 3, self.b2)

	def test_isLoser(self):
		self.b2.placeShip(0, 0, 0, 0)
		self.b1.fireShot(0, 0, self.b2)
		self.assertTrue(self.b2.isLoser())

	def test_progress(self):
		self.b1.placeShip(0, 0, 0, 5)
		self.b2.placeShip(0, 0, 0, 1)
		self.b1.fireShot(0, 0, self.b2)
		self.b2.fireShot(0, 0, self.b1)
		self.assertTrue(self.b1.progress(self.b2) == 50)
		self.assertTrue(self.b2.progress(self.b1) == 16)

class battleshipTest(unittest.TestCase):

	def test_init(self):
		Battleship.init(5, 5)
		self.assertTrue(Battleship.p1.myTurn)
		self.assertTrue(Battleship.p1.r == 5)
		self.assertTrue(Battleship.p1.c == 5)
		self.assertFalse(Battleship.p2.myTurn)
		self.assertTrue(Battleship.p2.r == 5)
		self.assertTrue(Battleship.p2.c == 5)

	def test_player1(self):
		self.assertTrue(Battleship.player1().myTurn)
		self.assertTrue(Battleship.player1().r == 5)
		self.assertTrue(Battleship.player1().c == 5)

	def test_player2(self):
		self.assertFalse(Battleship.player2().myTurn)
		self.assertTrue(Battleship.player2().r == 5)
		self.assertTrue(Battleship.player2().c == 5)

if __name__ == '__main__':
	unittest.main()
