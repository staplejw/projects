package assignment_3;

import static org.junit.Assert.*;
import java.util.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class DfsPathTest {

	DfsPath d;
	
	@Before
	public void setUp() throws Exception {
		// Read in data and initialize all data structures
		Cities.init();
		Menu.init();
		Restaurants.init();
		Digraph.init();
		
		// run depth first search
		d = new DfsPath();
	}

	// iterate through every vertex and check that it has been marked during dfs. this shows that all cities have been examined/explored
	@Test
	public void testallCitiesVisited() {
		for (int v = 0; v < Digraph.V(); v++) {
			assertTrue(d.getMarked(v));
		}
	}
	
	// a valid path starts in Boston (index 0), ends in Minneapolis (index 21) and only contains edges that are defined in the graph
	@Test
	public void testvalidPath() {
		Iterator<Integer> I1 = d.pathTo(Digraph.getST().get("MINNEAPOLIS")).iterator(); // iterator for first vertex
		Iterator<Integer> I2 = d.pathTo(Digraph.getST().get("MINNEAPOLIS")).iterator(); // iterator for second vertex
		I2.next(); // move second iterator one vertex ahead
		while (I2.hasNext()) {
			int v = I1.next().intValue(); // step to the next value for each iterator
			int w = I2.next().intValue();
			System.out.println(v + " - " + w); // print the edge being considered
			assertTrue(Digraph.hasEdge(v, w)); // check that this edge is in the graph
		}
		System.out.println();
	}

}
