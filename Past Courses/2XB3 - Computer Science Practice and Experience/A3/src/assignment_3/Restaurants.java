package assignment_3;

import java.io.File;
import java.util.*;

// the purpose of this class is to read in all of the restaurant information and assign boolean values to all the cities, showing which restaurants they have
public class Restaurants {
	
	// Initialize all of the restaurants
	public static void init() {
		readInRestaurant("data/mcdonalds.csv");
		readInRestaurant("data/burgerking.csv");
		readInRestaurant("data/wendys.csv");
	}

	//	reads data in from a file and assigns each city boolean values for which restaurant they have
	private static void readInRestaurant(String filename) {
		Scanner x;
		try {
			x = new Scanner(new File(filename));
			String line; // strings to hold the information
			String[] fields;
			String rest;
			String[] rest_city;
			while (x.hasNextLine()) {
				line = x.nextLine();
				fields = line.split(","); // split each line by commas
				double la = Double.parseDouble(fields[1].trim());
				double lo = Double.parseDouble(fields[0].trim());
				rest_city = fields[2].split("-");
				rest = rest_city[0].substring(1, 2); // first letter of the restaurant name
				rest = rest.trim(); 
				for (int i = 0; i < Cities.getN(); i++) { // iterate through the cities and check if the current lat/long fall within this city's range
					City C = Cities.getCity(i);
					if (C.getLat() - 0.5 <= la && la <= C.getLat() + 0.5) {
						if (C.getLong() - 0.5 <= lo && lo <= C.getLong() + 0.5) { // if the restaurant is within range of a city, check the name and set the boolean value
							if (rest.equals("M")) {
								Cities.getCity(i).setMcDonalds(true);
							} else if (rest.equals("B")) {
								Cities.getCity(i).setBurgerKing(true);
							} else {
								Cities.getCity(i).setWendys(true);
							}
						}
					}
				}
			}
		} catch(Exception e) {
			e.printStackTrace();
		}
	}
	
}
