package sort;


/**
 * This is a testing class that tests the implementation of merge sort
 * to check to see if the arrays of jobs are sorted properly. All test
 * classes use the isSorted method found in the Insertion class.
 * @author Justin Staples
 * @since 02/03/2017
 */
import static org.junit.Assert.*;

import java.util.List;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class MergeTest {

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
	public void testSortMerge() {
		assertFalse(Insertion.isSorted(all.get(0)));
		Merge.sortMerge(all.get(0), all.get(0).length);
		assertTrue(Insertion.isSorted(all.get(0)));
		assertFalse(Insertion.isSorted(all.get(1)));
		Merge.sortMerge(all.get(1), all.get(1).length);
		assertTrue(Insertion.isSorted(all.get(1)));
		assertFalse(Insertion.isSorted(all.get(2)));
		Merge.sortMerge(all.get(2), all.get(2).length);
		assertTrue(Insertion.isSorted(all.get(2)));
		assertFalse(Insertion.isSorted(all.get(3)));
		Merge.sortMerge(all.get(3), all.get(3).length);
		assertTrue(Insertion.isSorted(all.get(3)));
		assertFalse(Insertion.isSorted(all.get(4)));
		Merge.sortMerge(all.get(4), all.get(4).length);
		assertTrue(Insertion.isSorted(all.get(4)));
	}

}
