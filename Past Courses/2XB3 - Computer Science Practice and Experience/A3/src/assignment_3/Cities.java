package assignment_3;
import java.io.File;
import java.util.*;

// This class represents an abstract object that is an array of City objects
public class Cities {
	private static int N; // total number of cities
	private static City[] cities; // array of City objects
	private static ArrayList<String> names; // list of city names, 
	
	// initializes the array of cities
	public static void init() { 
		N = 32;
		cities = new City[N];
		readInCities("data/UScities.csv"); // populates the array
	}
	
	// returns the number of cities
	public static int getN() { 
		return N;
	}
	
	// gets the City at the given index
	public static City getCity(int i) { 
		return cities[i];
	}
	
	// gets the ArrayList of names of all the cities
	public static ArrayList<String> getNames() {
		return names;
	}
	
	// reads in a file and populates the array with City objects
	private static void readInCities(String filename) {
		Scanner x;
		names = new ArrayList<String>();
		try {
			x = new Scanner(new File(filename)); // read data from file
			String line; // holds the current line of the file
			String[] fields; // holds the data fields for each line
			line = x.nextLine(); // skip the first line 
			int i = 0; // array index
			while (x.hasNextLine()) {
				line = x.nextLine();
				fields = line.split(","); // comma separated values
				String a = fields[2].trim(); // read in strings, removing trailing and leading white space
				String n = fields[3].trim();
				double la = Double.parseDouble(fields[4].trim());
				double lo = Double.parseDouble(fields[5].trim());
				if (!names.contains(n)) { // make sure to not read in the same city twice (Atlanta)
					names.add(n);
					cities[i] = new City(a, n, la, lo); // create new city object
					i++;
				}				
			}
		} catch(Exception e) { // catch potential file not found error
			e.printStackTrace();
		}
	}
	
}
