package sort;

import static org.junit.Assert.*;
import java.io.*;
import java.util.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

/**
 * This is a testing class that tests the implementation of the insertion sort
 * methods to check to see if the arrays of jobs are sorted properly. It contains
 * three methods, each of which are dedicated to testing a different implementation
 * of insertion sort.All test classes use the isSorted method found in the Insertion class.
 * @author Justin Staples
 * @since 02/03/2017
 */
public class InsertionTest {

	List<Job[]> all;
	
	@Before
	public void setUp() throws Exception {
		all = GenJobs.generate();
	}

	@After
	public void tearDown() throws Exception {
		all = null;
	}

	@Test
	public void testSortInsert() {
		assertFalse(Insertion.isSorted(all.get(0))); // assert false to show that the array begins unsorted
		Insertion.sortInsert(all.get(0)); // this step sorts the array using the appropriate sorting algorithm
		assertTrue(Insertion.isSorted(all.get(0))); // now checks that the array is sorted
		assertFalse(Insertion.isSorted(all.get(1))); // repeat for the other arrays
		Insertion.sortInsert(all.get(1));
		assertTrue(Insertion.isSorted(all.get(1)));
		assertFalse(Insertion.isSorted(all.get(2)));
		Insertion.sortInsert(all.get(2));
		assertTrue(Insertion.isSorted(all.get(2)));
		assertFalse(Insertion.isSorted(all.get(3)));
		Insertion.sortInsert(all.get(3));
		assertTrue(Insertion.isSorted(all.get(3)));
		assertFalse(Insertion.isSorted(all.get(4)));
		Insertion.sortInsert(all.get(4));
		assertTrue(Insertion.isSorted(all.get(4)));
	}

	@Test
	public void testSortComparable() {
		assertFalse(Insertion.isSorted(all.get(0)));
		Insertion.sortComparable(all.get(0), all.get(0).length);
		assertTrue(Insertion.isSorted(all.get(0)));
		assertFalse(Insertion.isSorted(all.get(1)));
		Insertion.sortComparable(all.get(1), all.get(1).length);
		assertTrue(Insertion.isSorted(all.get(1)));
		assertFalse(Insertion.isSorted(all.get(2)));
		Insertion.sortComparable(all.get(2), all.get(2).length);
		assertTrue(Insertion.isSorted(all.get(2)));
		assertFalse(Insertion.isSorted(all.get(3)));
		Insertion.sortComparable(all.get(3), all.get(3).length);
		assertTrue(Insertion.isSorted(all.get(3)));
		assertFalse(Insertion.isSorted(all.get(4)));
		Insertion.sortComparable(all.get(4), all.get(4).length);
		assertTrue(Insertion.isSorted(all.get(4)));

	}

	@Test
	public void testSortBinary() {
		assertFalse(Insertion.isSorted(all.get(0)));
		Insertion.sortBinary(all.get(0), all.get(0).length);
		assertTrue(Insertion.isSorted(all.get(0)));
		assertFalse(Insertion.isSorted(all.get(1)));
		Insertion.sortBinary(all.get(1), all.get(1).length);
		assertTrue(Insertion.isSorted(all.get(1)));
		assertFalse(Insertion.isSorted(all.get(2)));
		Insertion.sortBinary(all.get(2), all.get(2).length);
		assertTrue(Insertion.isSorted(all.get(2)));
		assertFalse(Insertion.isSorted(all.get(3)));
		Insertion.sortBinary(all.get(3), all.get(3).length);
		assertTrue(Insertion.isSorted(all.get(3)));
		assertFalse(Insertion.isSorted(all.get(4)));
		Insertion.sortBinary(all.get(4), all.get(4).length);
		assertTrue(Insertion.isSorted(all.get(4)));
	}

}
