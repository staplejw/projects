## @file testCircleDeque.py
#  @title Testing Module
#  @author Justin Staples
#  @details This module consists of four classes, each 
#  dedicated to testing one of the pointADT, lineADT, 
#  circleADT and deque modules. The tests are done using
#  PyUnit, a unit testing frame work that tests one 
#  method at a time. There is at least one test for every 
#  method. A more thorough description of the results of 
#  testing and rationale behind test cases will be given 
#  in the final lab report. 
# staplejw 
# 001052815

from deque import *
import unittest

## @brief This class tests all the methods in the pointADT
#  module.
class pointTests(unittest.TestCase):

	def setUp(self):
		self.p1 = PointT(1, 2)
		self.p2 = PointT(0, 0)
		self.p3 = PointT(1, 0)
		
	def tearDown(self):
		self.p1 = None
		self.p2 = None
		self.p3 = None

	def test_xcrd(self):
		self.assertTrue(self.p1.xcrd() == 1)
		
	def test_ycrd(self):
		self.assertTrue(self.p1.ycrd() == 2)

	def test_dist(self):
		self.assertTrue(self.p1.dist(self.p2) == math.sqrt(5))

	def test_rot(self):
		# no rotation
		x = PointT(self.p3.xcrd(), self.p3.ycrd())
		x.rot(0)
		self.assertAlmostEqual(x.xcrd(), 1, None, None, 0.001)
		self.assertAlmostEqual(x.ycrd(), 0, None, None, 0.001)
		# positive angle
		x = PointT(self.p3.xcrd(), self.p3.ycrd())
		x.rot(math.pi/4)
		self.assertAlmostEqual(x.xcrd(), math.sqrt(2)/2, None, None, 0.001)
		self.assertAlmostEqual(x.ycrd(), math.sqrt(2)/2, None, None, 0.001)
		# negative angle
		x = PointT(self.p3.xcrd(), self.p3.ycrd())
		x.rot(-math.pi/2)
		self.assertAlmostEqual(x.xcrd(), 0, None, None, 0.001)
		self.assertAlmostEqual(x.ycrd(), -1, None, None, 0.001)
		# greater than pi
		x = PointT(self.p3.xcrd(), self.p3.ycrd())
		x.rot(5*math.pi/4)
		self.assertAlmostEqual(x.xcrd(), -math.sqrt(2)/2, None, None, 0.001)
		self.assertAlmostEqual(x.ycrd(), -math.sqrt(2)/2, None, None, 0.001)

## @brief This class tests all the methods in the lineADT
#  module.
class lineTests(unittest.TestCase):

	def setUp(self):
		self.l1 = LineT(PointT(0, 0), PointT(0, 0))
		self.l2 = LineT(PointT(-1, 2), PointT(3, 4))
		self.l3 = LineT(PointT(0, 0), PointT(1, 4))
		self.l4 = LineT(PointT(-3, -3), PointT(-3, 3))
		self.l5 = LineT(PointT(0, 1), PointT(1, 0))

	def tearDown(self):
		self.l1 = None
		self.l2 = None
		self.l3 = None
		self.l4 = None
		self.l5 = None

	def test_beg(self):
		self.assertTrue(self.l1.beg().xcrd() == 0 and self.l1.beg().ycrd() == 0)
		self.assertTrue(self.l2.beg().xcrd() == -1 and self.l2.beg().ycrd() == 2)
		

	def test_end(self):
		self.assertTrue(self.l1.end().xcrd() == 0 and self.l1.end().ycrd() == 0)
		self.assertTrue(self.l2.end().xcrd() == 3 and self.l2.end().ycrd() == 4)

	def test_len(self):
		self.assertTrue(self.l1.len() == 0)
		self.assertTrue(self.l2.len() == math.sqrt(20))

	def test_mdpt(self):
		self.assertTrue(self.l1.mdpt().xcrd() == 0 and self.l1.mdpt().ycrd() == 0)
		self.assertTrue(self.l2.mdpt().xcrd() == 1 and self.l2.mdpt().ycrd() == 3)

	def test_rot(self):
		# no rotation
		self.l2.rot(0)
		self.assertAlmostEqual(self.l2.beg().xcrd(), -1, None, None, 0.001)
		self.assertAlmostEqual(self.l2.beg().ycrd(), 2, None, None, 0.001)
		self.assertAlmostEqual(self.l2.end().xcrd(), 3, None, None, 0.001)
		self.assertAlmostEqual(self.l2.end().ycrd(), 4, None, None, 0.001)
		# positive angle
		self.l3.rot(math.pi/2)
		self.assertAlmostEqual(self.l3.beg().xcrd(), 0, None, None, 0.001)
		self.assertAlmostEqual(self.l3.beg().ycrd(), 0, None, None, 0.001)
		self.assertAlmostEqual(self.l3.end().xcrd(), -4, None, None, 0.001)
		self.assertAlmostEqual(self.l3.end().ycrd(), 1, None, None, 0.001)
		# negative angle
		self.l4.rot(-math.pi/2)
		self.assertAlmostEqual(self.l4.beg().xcrd(), -3, None, None, 0.001)
		self.assertAlmostEqual(self.l4.beg().ycrd(), 3, None, None, 0.001)
		self.assertAlmostEqual(self.l4.end().xcrd(), 3, None, None, 0.001)
		self.assertAlmostEqual(self.l4.end().ycrd(), 3, None, None, 0.001)	
		# greater than pi
		self.l5.rot(5*math.pi/4)
		self.assertAlmostEqual(self.l5.beg().xcrd(), 0.7071, None, None, 0.001)
		self.assertAlmostEqual(self.l5.beg().ycrd(), -0.7071, None, None, 0.001)
		self.assertAlmostEqual(self.l5.end().xcrd(), -0.7071, None, None, 0.001)
		self.assertAlmostEqual(self.l5.end().ycrd(), -0.7071, None, None, 0.001)		

## @brief This class tests all the methods in the circleADT
#  module.
class circleTests(unittest.TestCase):

	def setUp(self):
		self.c1 = CircleT(PointT(0, 0), 1)
		self.c2 = CircleT(PointT(3, 0), 1)
		self.c3 = CircleT(PointT(6, 0), 1)
		self.c4 = CircleT(PointT(0, 3), 1)
		self.c5 = CircleT(PointT(3, 4), 2)
		self.c6 = CircleT(PointT(8, 0), 1)
		self.f1 = lambda r: 1/r**2
		self.f2 = lambda r: r + 1

	def tearDown(self):
		self.c1 = None
		self.c2 = None
		self.c3 = None
		self.c4 = None
		self.c5 = None
		self.c6 = None

	def test_cen(self):
		self.assertTrue(self.c5.cen().xcrd() == 3 and self.c5.cen().ycrd() == 4)

	def test_rad(self):
		self.assertTrue(self.c5.rad() == 2)

	def test_area(self):
		self.assertAlmostEqual(self.c1.area(), 3.14159, None, None, 0.001)

	def test_intersect(self):
		# c3 and c6 do intersect at a point
		self.assertTrue(self.c3.intersect(self.c6))
		# c1 and c2 do not intersect, so assertFalse is used
		self.assertFalse(self.c1.intersect(self.c2))

	def test_connection(self):
		l = self.c3.connection(self.c4)
		self.assertTrue(l.beg().xcrd() == 6 and l.beg().ycrd() == 0)
		self.assertTrue(l.end().xcrd() == 0 and l.end().ycrd() == 3)

	def test_force(self):
		self.assertAlmostEqual(self.c1.force(self.f1)(self.c6), 0.1542, None, None, 0.001)
		self.assertAlmostEqual(self.c1.force(self.f2)(self.c5), 236.8705, None, None, 0.001)

## @brief This class tests all the methods in the deque
#  module.
class dequeTests(unittest.TestCase):

	def setUp(self):
		self.c1 = CircleT(PointT(0, 0), 1)
		self.c2 = CircleT(PointT(3, 0), 1)
		self.c3 = CircleT(PointT(6, 0), 1)
		self.c4 = CircleT(PointT(0, 3), 1)
		self.c5 = CircleT(PointT(3, 4), 2)
		self.c6 = CircleT(PointT(8, 0), 1)
		self.f1 = lambda r: 1/r**2
		self.f2 = lambda r: r + 1

	def tearDown(self):
		self.c1 = None
		self.c2 = None
		self.c3 = None
		self.c4 = None
		self.c5 = None
		self.c6 = None

	def test_init(self):
		Deq.init()
		self.assertTrue(Deq.size() == 0)

	def test_pushBack(self):
		# pushBack tested with just one element in the queue
		Deq.init()
		Deq.pushBack(self.c1)
		self.assertTrue(Deq.back().cen().xcrd() == 0)
		self.assertTrue(Deq.back().cen().ycrd() == 0)
		self.assertTrue(Deq.back().rad() == 1)
		# same test, but with three circles in the queue
		Deq.init()
		Deq.pushBack(self.c3)
		Deq.pushBack(self.c4)
		Deq.pushBack(self.c5)
		self.assertTrue(Deq.back().cen().xcrd() == 3)
		self.assertTrue(Deq.back().cen().ycrd() == 4)
		self.assertTrue(Deq.back().rad() == 2)		
		# filling the queue to test FULL exception
		Deq.init()
		for i in range(0, 20):
			Deq.pushBack(self.c2)
		self.assertRaises(FULL, Deq.pushBack, self.c2)

	def test_pushFront(self):
		# pushFront tested with just one element in the queue
		Deq.init()
		Deq.pushFront(self.c1)
		self.assertTrue(Deq.front().cen().xcrd() == 0)
		self.assertTrue(Deq.front().cen().ycrd() == 0)
		self.assertTrue(Deq.front().rad() == 1)
		# same test, but with three circles in the queue
		Deq.init()
		Deq.pushFront(self.c3)
		Deq.pushFront(self.c4)
		Deq.pushFront(self.c5)
		self.assertTrue(Deq.front().cen().xcrd() == 3)
		self.assertTrue(Deq.front().cen().ycrd() == 4)
		self.assertTrue(Deq.front().rad() == 2)		
		# filling the queue to test FULL exception
		Deq.init()
		for i in range(0, 20):
			Deq.pushFront(self.c2)
		self.assertRaises(FULL, Deq.pushBack, self.c2)

	def test_popBack(self):
		# push two elements at the back, then pop the back and check the first element
		Deq.init()
		Deq.pushBack(self.c2)
		Deq.pushBack(self.c6)
		Deq.popBack()
		self.assertTrue(Deq.back().cen().xcrd() == 3)
		self.assertTrue(Deq.back().cen().ycrd() == 0)
		self.assertTrue(Deq.back().rad() == 1)
		# popping an empty queue to test EMPTY exception
		Deq.init()
		self.assertRaises(EMPTY, Deq.popBack)

	def test_popFront(self):
		# push two elements to the front, then pop the front and check the first element
		Deq.init()
		Deq.pushFront(self.c4)
		Deq.pushFront(self.c5)
		Deq.popFront()
		self.assertTrue(Deq.front().cen().xcrd() == 0)
		self.assertTrue(Deq.front().cen().ycrd() == 3)
		self.assertTrue(Deq.front().rad() == 1)
		# popping an empty queue to test EMPTY exception
		Deq.init()
		self.assertRaises(EMPTY, Deq.popFront)

	def test_back(self):
		# push three circles and check the back element
		Deq.init()
		Deq.pushBack(self.c3)
		Deq.pushBack(self.c4)
		Deq.pushBack(self.c5)
		self.assertTrue(Deq.back().cen().xcrd() == 3)
		self.assertTrue(Deq.back().cen().ycrd() == 4)
		self.assertTrue(Deq.back().rad() == 2)	
		# asking for the back element of an empty queue gives EMPTY exception
		Deq.init()
		self.assertRaises(EMPTY, Deq.back)

	def test_front(self):
		# push three circles and check the front element
		Deq.init()
		Deq.pushFront(self.c3)
		Deq.pushFront(self.c4)
		Deq.pushFront(self.c5)
		self.assertTrue(Deq.front().cen().xcrd() == 3)
		self.assertTrue(Deq.front().cen().ycrd() == 4)
		self.assertTrue(Deq.front().rad() == 2)	
		# asking for the front element of an empty queue gives EMPTY exception
		Deq.init()
		self.assertRaises(EMPTY, Deq.front)

	def test_size(self):
		Deq.init()
		self.assertTrue(Deq.size() == 0)
		Deq.pushFront(self.c2)
		Deq.pushBack(self.c1)
		self.assertTrue(Deq.size() == 2)

	def test_disjoint(self):
		# disjoint with 0 circles should raise EMPTY exception
		Deq.init()
		self.assertTrue(EMPTY, Deq.disjoint)
		# disjoint with 1 circle should return True
		Deq.pushBack(self.c1)
		self.assertTrue(Deq.disjoint())
		# disjoint with multiple disjoint circles should return True
		Deq.pushBack(self.c2)
		Deq.pushBack(self.c3)
		Deq.pushBack(self.c4)
		Deq.pushBack(self.c5)
		self.assertTrue(Deq.disjoint())
		# now adding a circle that breaks disjoint condition should return False
		Deq.pushBack(self.c6)
		self.assertFalse(Deq.disjoint())

	def test_sumFx(self):
		# sumFx with empty queue should raise EMPTY exception
		Deq.init()
		self.assertRaises(EMPTY, Deq.sumFx, self.f1)
		Deq.pushFront(self.c1)
		Deq.pushBack(self.c2)
		Deq.pushBack(self.c5)
		self.assertAlmostEqual(Deq.sumFx(self.f1), 2.0441, None, None, 0.001)

if __name__ == '__main__':
	unittest.main()
