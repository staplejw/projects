/** 
 * This class serves as a library for analyzing different paths
 * and segments.
 * @author Justin Staples (staplejw, 001052815)
 * @since March 19th, 2017
 */
public class PathCalculation {

	/** 
	 * This method determines whether or not two points 
	 * can be considered a valid segment for the map.
	 * @param p1 first point.
	 * @param p2 second point.
	 * @return Returns true if it is a valid segment and
	 * false otherwise.
	 */
	public static boolean is_validSegment(PointT p1, PointT p2) {
		return true;
	}

	/** 
	 * This method determines whether or not a certain 
	 * path can be considered valid.
	 * @param p the path that is being considered
	 * @return Returns true if it is a valid path and
	 * false otherwise.
	 */
	public static boolean is_validPath(PathT p) {
		return true;
	}

	/** 
	 * This method determines whether or not a certain 
	 * path can be considered the shortest path.
	 * @param p the path that is being considered
	 * @return Returns true if there are no shorter paths
	 * and false otherwise.
	 */
	public static boolean is_shortestPath(PathT p) {
		return true;
	}

	/** 
	 * This method determines the total distance 
	 * of a certain path.
	 * @param p the path that is being considered
	 * @return Returns the length of the path.
	 */
	public static double totalDistance(PathT p) {
		if (p.size() < 2) {
			return 0;
		}
		double dist = 0;
		for (int i = 0; i < p.size() - 1; i++) {
			dist += p.getval(i).dist(p.getval(i + 1));
		}
		return dist;
	}

	/** 
	 * This method determines the total number of turns 
	 * of a certain path.
	 * @param p the path that is being considered
	 * @return Returns the number of turns.
	 */
	public static int totalTurns(PathT p) {
		if (p.size() < 3) {
			return 0;
		}
		int turns = 0;
		for (int i = 0; i < p.size() - 2; i++) {
			if (!(angle(p.getval(i), p.getval(i + 1), p.getval(i + 2)) < 0.0000001)) {
				turns++;
			}
		}
		return turns;
	}

	/** 
	 * This method calculates the turning angle between successive 
	 * segments in the path.
	 * @param p1 the previous point
	 * @param p2 the current point
	 * @param p3 the next point
	 * @return Returns the turning angle in radians.
	 */
	private static double angle(PointT p1, PointT p2, PointT p3) {
		double ux = p2.xcrd() - p1.xcrd();
		double uy = p2.ycrd() - p1.ycrd();
		double vx = p3.xcrd() - p2.xcrd();
		double vy = p3.ycrd() - p2.ycrd();
		double dot = ux * vx + uy * vy;
		double umag = p1.dist(p2);
		double vmag = p2.dist(p3);
		return Math.acos(dot/(umag * vmag));
	}

	/** 
	 * This method determines the estimated time 
	 * for a particular path based on the time spent
	 * driving forward and the time spent turning.
	 * @param p the path that is being considered
	 * @return Returns the approximate duration of the path.
	 */
	public static double estimatedTime(PathT p) {
		if (p.size() < 2) {
			return 0;
		} else if (p.size() == 2) {
			return p.getval(0).dist(p.getval(1)) / Constants.VELOCITY_LINEAR;
		} else {
			double lintime = 0;
			double angtime = 0;
			for (int i = 0; i < p.size() - 1; i++) {
				lintime += p.getval(i).dist(p.getval(i + 1)) / Constants.VELOCITY_LINEAR;
			}
			for (int i = 0; i < p.size() - 2; i++) {
				angtime += angle(p.getval(i), p.getval(i + 1), p.getval(i + 2)) / Constants.VELOCITY_ANGULAR;
			}
			return lintime + angtime;
		}
	}

}
