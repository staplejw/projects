/** 
 * This class is for an abstract object that represents
 * the map. The map contains obstacles, safezones, and destinations.
 * @author Justin Staples (staplejw, 001052815)
 * @since March 19th, 2017
 */
public class Map {

	/**
	 * The list of obstacle regions on the map.
	 */
	private static Obstacles obstacles;
	/**
	 * The list of destination regions on the map.
	 */
	private static Destinations destinations;
	/**
	 * The list of safe zone regions on the map.
	 */
	private static SafeZone safeZone;

	/** 
	 * This is the initializer method for the map.
	 * @param o the list of obstacles.
	 * @param d the list of destinations.
	 * @param sz the list of safe zones.
	 */
	public static void init(Obstacles o, Destinations d, SafeZone sz) {
		Map.obstacles = o;
		Map.destinations = d;
		Map.safeZone = sz;
	}

	/** 
	 * This is the getter method for the list of obstacles.
	 * @return returns the list of obstacles.
	 */
	public static Obstacles get_obstacles() {
		return Map.obstacles;
	}

	/** 
	 * This is the getter method for the list of destinations.
	 * @return returns the list of destinations.
	 */
	public static Destinations get_destinations() {
		return Map.destinations;
	}

	/** 
	 * This is the getter method for the list of safe zones.
	 * @return returns the list of safe zones.
	 */
	public static SafeZone get_safeZone() {
		return Map.safeZone;
	}

}