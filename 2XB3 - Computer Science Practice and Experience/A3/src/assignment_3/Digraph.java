package assignment_3;

import java.io.*;
import java.util.*;

// this class represents an abstract object that is a directed graph of all the Cities 
public class Digraph {
	private static int V; // number of vertices (cities)
	private static int E; // number of edges (connected routes between cities)
	private static Bag<Integer>[] adj; // adjacency lists for every vertex
	private static ST<String, Integer> city_id; // a symbol table that maps each city name to a unique index
	
	public static void init() {
		V = 32; // 32 total cities
		E = 0; // graph starts initially empty (no edges)
		adj = (Bag<Integer>[]) new Bag[V]; // initialize arrays
		for (int v = 0; v < V; v++)
			adj[v] = new Bag<Integer>();
		city_id = new ST<String, Integer>(); // fill the symbol table 
		for (int i = 0; i < V; i++) {
			city_id.put(Cities.getCity(i).getName(), i);
		}
		buildGraph("data/connectedCities.txt"); // read in edges
	}

	// getter methods for the digraph
	public static int V() {
		return V;
	}
	
	public static int E() {
		return E;
	}

	public static Iterable<Integer> adj(int v) {
		return adj[v];
	}
	
	public static ST<String, Integer> getST() {
		return city_id;
	}

	// adds a new edge to the graph
	public static void addEdge(String from, String to) { // takes two strings, the names of the cities
		adj[city_id.get(from)].add(city_id.get(to)); // uses the ST to get the vertex ID, adds the edge to the adjacency list
		E++;
	}
	
	// returns true iff there exists a directed edge from v to w in the graph
	public static boolean hasEdge(int v, int w) {
		Iterator<Integer> I = adj[v].iterator(); 
		while (I.hasNext()) {
			if (I.next().intValue() == w) {
				return true;
			}
		}
		return false;
	}
	
	// reads in a file and populates the graph with directed edges between cities
	private static void buildGraph(String filename) {
		Scanner x; // new scanner object
		try {
			x = new Scanner(new File(filename));
			String line; // strings that will hold different pieces of each line
			String[] parts;
			String[] first_parts;
			String[] second_parts;
			while (x.hasNextLine()) {
				String first = ""; // will store the 'from' city
				String second = ""; // will store the 'to' city
				line = x.nextLine();
				parts = line.split("\\),"); // splits each line of the file into two parts
				first_parts = parts[0].trim().split(" "); // splits each part further by spaces
				second_parts = parts[1].trim().split(" ");
				int j = 0;
				if (first_parts.length == 1) { // handles 'Portland(OR)' error which has no space
					first = first_parts[0].substring(0, first_parts[0].indexOf("("));
					while (!second_parts[j].substring(0, 1).equals("(")) {
						second += second_parts[j] + " ";
						j++;
					}
				} else { // scans the pieces and appends them until the '(' is found, then stops
					while (!first_parts[j].substring(0, 1).equals("(")) {
						first += first_parts[j] + " ";
						j++;
					}
					j = 0;
					while (!second_parts[j].substring(0, 1).equals("(")) {
						second += second_parts[j] + " ";
						j++;
					}
				}
				first = first.trim().toUpperCase(); // remove white space and uses upper case to match with USCities.csv
				second = second.trim().toUpperCase();
				Digraph.addEdge(first, second); // add the edge from the first city to the second
			}
		} catch(Exception e) {
			e.printStackTrace();
		}
	}
	
}
