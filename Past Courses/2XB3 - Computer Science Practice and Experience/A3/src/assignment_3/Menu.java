package assignment_3;
import java.io.File;
import java.util.*;

//This class represents an abstract object that is an array of meals
public class Menu {
	private static int N; // total number of menu items
	private static Meal[] meals; // array of Meal objects
	
	 // initializes the array of Meals
	public static void init() {
		N = 40; // the number of meals on the menu
		meals = new Meal[N];
		readInMeals("data/menu.csv"); // populates the array
	}
	
	// getter methods for the menu
	public static int getN() {
		return N;
	}
	
	public static Meal getMeal(int i) {
		return meals[i];
	}

	// this methods determines the cheapest meal available at a city
	// this method is used for handling dynamic weights for dijkstra's algorithm
	public static Meal getCheapestMeal(City C, ArrayList<Meal> L) { // takes as input a city and a list of meals and returns the cheapest meal at that city that is not in the list
		boolean M = C.getMcDonalds(); // checks what restaurants are available at this city
		boolean B = C.getBurgerKing();
		boolean W = C.getWendys();
		ArrayList<Meal> city_menu = new ArrayList<Meal>(); // new list of meals
		if (M) { // if McDonald's is available at this city, populate the list with all McDonald's meals
			for (int i = 0; i <= 17; i++) {
				city_menu.add(Menu.getMeal(i));
			}
		}
		if (B) { // same for Burger King
			for (int i = 18; i <= 29; i++) {
				city_menu.add(Menu.getMeal(i));
			}
		}
		if (W) { // same for Wendy's
			for (int i = 30; i <= 39; i++) {
				city_menu.add(Menu.getMeal(i));
			}
		}
		double min = 10.0; // set min to a value larger than the cost of any meal
		int j = 0;
		for (int i = 0; i < city_menu.size(); i++) { // iterate through all the meals that this city has, finding the minimum cost meal that is not in the list
			if (city_menu.get(i).getCost() < min && !L.contains(city_menu.get(i))) {
				min = city_menu.get(i).getCost(); // update min 
				j = i;
			}	
		}
		return city_menu.get(j); // return cheapest meal
	}
	
	// this method is used to refresh a menu that has already eaten every possible meal at a given restaurant 
	public static void refreshMenu(ArrayList<Meal> meals) {
		int M = 0;
		int B = 0;
		int W = 0;
		for (Meal m : meals) { // count the number of meals at each restaurant in the list
			if (m.getName().equals("McD")) {
				M++;
			} else if (m.getName().equals("Bur")) {
				B++;
			} else {
				W++;
			}
		}
		Iterator<Meal> I = meals.iterator();
		if (M == 18 ) { // if there have been 18 McDonald's meals eaten, refresh the menu by removing all of them from the list
			while (I.hasNext()) {
				Meal blah = I.next();
				if (blah.getName().equals("McD")) {
					meals.remove(blah);
				}
			}
		}
		I = meals.iterator();
		if (B == 12 ) { // same for Burger King
			while (I.hasNext()) {
				Meal blah = I.next();
				if (blah.getName().equals("Bur")) {
					meals.remove(blah);
				}
			}
		}
		I = meals.iterator();
		if (W == 10 ) { // same for Wendy's
			while (I.hasNext()) {
				Meal blah = I.next();
				if (blah.getName().equals("Wen")) {
					meals.remove(blah);
				}
			}
		}
	}
	
	// reads in a file and populates the array with Meal Objects
	private static void readInMeals(String filename) {
		Scanner x;
		try {
			x = new Scanner(new File(filename)); // read data from file
			String line; // holds the current line of the file
			String[] fields; // holds the data fields for each line
			line = x.nextLine(); // skip the first line 
			int i = 0; // array index
			while (x.hasNextLine()) {
				line = x.nextLine();
				fields = line.split(","); // comma separated values
				String r = fields[0].trim().substring(0, 3); // read in strings, removing trailing and leading white space
				String n = fields[1].trim();
				double c = Double.parseDouble(fields[2].trim().substring(1));
				String m = fields[3].trim();
				meals[i] = new Meal(r, n, c, m); // create new meal object
				i++;
			}
		} catch(Exception e) { // catch potential file not found error
			e.printStackTrace();
		}
	}
	
}
