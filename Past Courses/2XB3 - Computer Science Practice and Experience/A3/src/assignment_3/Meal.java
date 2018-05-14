package assignment_3;

// this class represents an abstract data type for a Meal
public class Meal implements Comparable<Meal> {
	private String restaurant; // which restaurant this meal is available at
	private String name; // name of the meal
	private double cost; // cost of the meal
	private String meat; // sandwich meat
	
	// constructor for Meal
	public Meal(String rest, String name, double cost, String meat) {
		this.restaurant = rest;
		this.name = name;
		this.cost = cost;
		this.meat = meat;
	}
	
	// getter methods for type Meal
	public String getRest() {
		return this.restaurant;
	}
	
	public String getName() {
		return this.name;
	}
	
	public double getCost() {
		return this.cost;
	}
	
	public String getMeat() {
		return this.meat;
	}
	
	// writes a summary of the meal as a string
	public String toString() {
		return restaurant + ", " + name + ", " + cost + ", " + meat;
	}
	
	// compares meals based on their cost
	@Override
	public int compareTo(Meal that) {
		if (this.getCost() < that.getCost()) {
			return -1;
		} else if (this.getCost() == that.getCost()) {
			return 0;
		} else {
			return 1;
		}
	}
	
}
