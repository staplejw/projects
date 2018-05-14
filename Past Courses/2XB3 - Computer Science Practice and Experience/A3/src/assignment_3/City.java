package assignment_3;

// This class represents an abstract data type for a city
public class City {
	private String abbrev; // state abbreviation
	private String name; // city name 
	private double latitude; // city latitude
	private double longitude; // city longitude
	private boolean McDonalds; // does this city have a McDonalds nearby?
	private boolean BurgerKing; // does this city have a BurgerKing nearby?
	private boolean Wendys; // does this city have a Wendys nearby?
	
	public City(String abbrev, String name, double latitude, double longitude) {
		this.abbrev = abbrev;
		this.name = name;
		this.latitude = latitude;
		this.longitude = longitude;
		this.McDonalds = false;
		this.BurgerKing = false;
		this.Wendys = false;
	}
	
	// getter methods for type City
	public String getAbbrev() {
		return this.abbrev;
	}
	
	public String getName() {
		return this.name;
	}
	
	public double getLat() {
		return this.latitude;
	}
	
	public double getLong() {
		return this.longitude;
	}
	
	public boolean getMcDonalds() {
		return this.McDonalds;
	}
	
	public boolean getBurgerKing() {
		return this.BurgerKing;
	}
	
	public boolean getWendys() {
		return this.Wendys;
	}
	
	// setter methods for which restaurants this City has, all values initialized to false
	public void setMcDonalds(boolean B) {
		this.McDonalds = B;
	}
	
	public void setBurgerKing(boolean B) {
		this.BurgerKing = B;
	}
	
	public void setWendys(boolean B) {
		this.Wendys = B;
	}
	
	// summary of the city as a string
	public String toString() {
		return abbrev + ", " + name + ", " + latitude + ", " + longitude;
	}
	
}
