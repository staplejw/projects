package assignment_3;

import java.io.*;
import java.util.*;

// this class is used shortest path queries on the digraph
public class ShortestPath {
	private int[] edgeTo; // what was the last node visited?
	private double[] costTo; // what is the cost of travelling to this node via the shortest path found?
	private ArrayList<Meal>[] mealsTo; // what meals have been eaten along the shortest path?
	private IndexMinPQ<Double> pq; // priority queue for keeping track of vertices in dijkstra's
	
	// constructor for ShortestPath
	public ShortestPath() {
		edgeTo = new int[Digraph.V()]; // initialize data structures
		costTo = new double[Digraph.V()];
		mealsTo = (ArrayList<Meal>[]) new ArrayList[Digraph.V()];
		for (int i = 0; i < Digraph.V(); i++) {
			mealsTo[i] = new ArrayList<Meal>();
		}
		pq = new IndexMinPQ<Double>(Digraph.V());
		for (int v = 0; v < Digraph.V(); v++) // set costTo to positive infinity
			costTo[v] = Double.POSITIVE_INFINITY;
		costTo[0] = 0.0; // set costTo of source (Boston) to 0
		pq.insert(0, 0.0); // start at source
		while (!pq.isEmpty()) // while the priority queue is not empty, relax all edges adjacent to vertex
			relax(pq.delMin());
	}
	
	// getter methods for ShortestPath
	public int getEdgeTo(int v) {
		return edgeTo[v];
	}
	
	public double getCostTo(int v) {
		return costTo[v];
	}
	
	public ArrayList<Meal> getMealsTo(int v) {
		return mealsTo[v];
	}
	
	// relaxes all edges adjacent to v. this means update the costTo if there is a better path discovered
	private void relax(int v) {
		Menu.refreshMenu(mealsTo[v]); // refresh menu if all the options at one restaurant have been eaten
		for(int w : Digraph.adj(v)) // for all edges adjacent to v, update the cost if needed
		{
			if (costTo[w] > costTo[v] + Menu.getCheapestMeal(Cities.getCity(w), mealsTo[v]).getCost()) // compares costTo[v] plus the cheapest meal at w, with the previous value of costTo[w]
			{
				costTo[w] = costTo[v] + Menu.getCheapestMeal(Cities.getCity(w), mealsTo[v]).getCost(); // if a cheaper option is available update costTo[w]
				edgeTo[w] = v; // update edgeTo[w]
				mealsTo[w] = new ArrayList<Meal>(); // update mealsTo[w] by first creating a new list
				for (Meal m : mealsTo[v]) { // for all the meals that were in mealsTo[v], add them to w's new list
					mealsTo[w].add(m);
				}
				mealsTo[w].add(Menu.getCheapestMeal(Cities.getCity(w), mealsTo[v])); // then add the meal eaten at [w]
				if (pq.contains(w)) pq.change(w, costTo[w]); // update pq
				else pq.insert(w, costTo[w]);
			}
		}
	}
	
	// this method finds the path to Minneapolis and writes all the necessary information to the output file in the form of a table
	public void printPath() {
		FileWriter y; // new filewriter object
		try {
			y = new FileWriter("a3_out.txt", true);
			y.write("\n");
			y.write("City\t\t\t|Meal\t\t\t\t\t\t\t\t\t\t |Cost\t\t\t\t\t\t\t\t\t\n"); // title row
			y.write("--------------------------------------------------------------------\n");
			
			Iterable<Integer> path = pathTo(Digraph.getST().get("MINNEAPOLIS")); // get path to Minneapolis
			Iterator<Meal> meals = mealsTo[Digraph.getST().get("MINNEAPOLIS")].iterator(); // get iterator for arraylist of meals
			for (Integer i : path) { // for each node in the path, write the required information to the table
				if (i.equals(0)) { // info for Boston is different because no meal is eaten there
					y.write(Cities.getCity(i).getName() + "\t\t\t" + "|N/A" + "\t\t\t\t\t\t\t\t\t\t" + " |N/A\n");
				} else { // write the info for the other cities
					Meal next = meals.next();
					String city = Cities.getCity(i).getName() + "           ";
					city = city.substring(0, 16);
					String meal = next.getName() + " (" + next.getRest() + ")" + "                        ";
					meal = meal.substring(0, 44);
					y.write(city + "|" + meal + "|$" + next.getCost() + "\t\t\t\t\t\n");
				}
			}
			y.write("--------------------------------------------------------------------\n");
			y.write("TOTAL\t\t\t\t\t\t\t\t\t\t\t\t\t\t  " + "$" + costTo[21] + "\n"); // write total cost of trip
			y.write("\n");
			y.close();
		} catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	// this method returns a stack of integers that represent the vertices visited
	public Iterable<Integer> pathTo(int v) {
		Stack<Integer> path = new Stack<Integer>();
		for (int e = v; e != 0; e = edgeTo[e]) // trace back through edgeTo to get the path
			path.push(e);
		path.push(0); // push the source
		return path;
	}
	
}
