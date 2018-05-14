package assignment_3;

import java.io.FileWriter;

// this class is used for bfs queries on the digraph
public class BfsPath {
	private boolean[] marked; // has this node been visited before?
	private int[] edgeTo; // what was the last node visited?
	
	// constructor for BfsPath
	public BfsPath() {
		marked = new boolean[Digraph.V()]; // initialize the arrays
		edgeTo = new int[Digraph.V()];
		bfs(0); // perform bfs on node 0 (Boston)
	}
	
	// implementation of bfs, adapted from Sedgewick/Wayne
	private void bfs(int s) {
		Queue<Integer> queue = new Queue<Integer>();
		marked[s] = true;
		queue.enqueue(s);
		while (!queue.isEmpty()) {
			int v = queue.dequeue();
			for (int w : Digraph.adj(v)) {
				if (!marked[w]) {
					edgeTo[w] = v;
					marked[w] = true;
					queue.enqueue(w);
				}
			}
		}
	}
	 // getter methods for BfsPath
	public boolean getMarked(int v) {
		return marked[v];
	}
	
	public int getEdgeTo(int v) {
		return edgeTo[v];
	}
	
	// writes the bfs path to the output file a3_out.txt
	public void printPath() {
		FileWriter y; // create new filewriter object
		try {
			y = new FileWriter("a3_out.txt", true);
			y.write("BFS: ");
			Iterable<Integer> path = pathTo(Digraph.getST().get("MINNEAPOLIS")); // stack of integers  
			for (Integer i : path) { // for each vertex, write the city name to output, separated by commas
				if (!i.equals(21)) { // don't print a comma after Minneapolis, the last city
					y.write(Cities.getCity(i).getName() + ", ");
				} else {
					y.write(Cities.getCity(i).getName());
				}
			}
			y.write("\n"); 
			y.close();
		} catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	// returns a stack of integers that represent the path of vertices from the source to any node v
	public Iterable<Integer> pathTo(int v) {
		Stack<Integer> path = new Stack<Integer>();
		for (int x = v; x != 0; x = edgeTo[x]) { 
			path.push(x);
		}
		path.push(0);
		return path;
	}

}
