/** 
 * This class represents an abstract data type for a 2-d point.
 * @author Justin Staples (staplejw, 001052815)
 * @since March 19th, 2017
 */
public class PointT {

	/** 
	 * X-coordinate of the point.
	 */
	private double xc;
	/** 
	 * Y-coordinate of the point.
	 */
	private double yc;

	/** 
	 * This is the constructor for PointT.
	 * @param x X-coordinate of the point.
	 * @param y Y-coordinate of the point.
	 */
	public PointT(double x, double y) {
		if (!(0 <= x && x <= Constants.MAX_X) || !(0 <= y && y <= Constants.MAX_Y)) {
			throw new InvalidPointException("This is not a valid point");
		}
		this.xc = x;
		this.yc = y;
	}

	/** 
	 * This is the getter for the x-coordinate.
	 * @return x-coordinate.
	 */
	public double xcrd() {
		return this.xc;
	}

	/** 
	 * This is the getter for the y-coordinate.
	 * @return y-coordinate.
	 */
	public double ycrd() {
		return this.yc;
	}

	/** 
	 * This method gives the distance between two points.
	 * @param p The second point used for calculating distance.
	 * @return x-coordinate.
	 */
	public double dist(PointT p) {
		double xdist = this.xcrd() - p.xcrd();
		double ydist = this.ycrd() - p.ycrd();
		return Math.sqrt(Math.pow(xdist, 2) + Math.pow(ydist, 2));
	}

}