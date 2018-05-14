package assignment_3;

// This class is the main program. It is the only class that contains a main method. 
public class Program {
	
	public static void main(String[] args) {
		// Read in data and initialize all data structures
		Cities.init();
		Menu.init();
		Restaurants.init();
		Digraph.init();
		
		// run depth first search and write the path to the output file
		DfsPath d = new DfsPath();
		d.printPath();
		
		
		// run breadth first search and write the path to the output file
		BfsPath b = new BfsPath();
		b.printPath();

		// run dijkstra's algorithm to find the lowest cost path and write it to the output file
		ShortestPath p = new ShortestPath();
		p.printPath();
	}

}
