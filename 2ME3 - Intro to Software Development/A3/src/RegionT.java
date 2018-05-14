/** 
 * This class represents the abstract data type
 * for a 2-d rectangular region.
 * @author Justin Staples (staplejw, 001052815)
 * @since March 19th, 2017
 */
public class RegionT {

	/**
	 * This represents the lower left point of the region.
	 */
	private PointT lower_left;
	/**
	 * This represents the width of the region.
	 */
	private double width;
	/**
	 * This represents the height of the region.
	 */
	private double height;

	/** 
	 * This is the constructor for RegionT.
	 * @param p lower left point.
	 * @param w width.
	 * @param h height.
	 * @exception InvalidRegionException if the region specified
	 * would extend outside of the map region.
	 */
	public RegionT(PointT p, double w, double h) {
		if (!(w > 0 && h > 0 && (p.xcrd() + w) <= Constants.MAX_X && (p.ycrd() + h) <= Constants.MAX_Y)) {
			throw new InvalidRegionException("This is not a valid region");
		}
		this.lower_left = p;
		this.width = w;
		this.height = h;
	}

	/** 
	 * This method determines if a point is inside or within
	 * tolerance of the region.
	 * @param p point that is being checked to see if it 
	 * is in the region.
	 * @return returns true if the point is considered in the region
	 * and false otherwise.
	 */
	public boolean pointInRegion(PointT p) {
		double px = p.xcrd();
		double py = p.ycrd();
		double llx = this.lower_left.xcrd();
		double lly = this.lower_left.ycrd();
		double llxw = this.lower_left.xcrd() + this.width;
		double llyh = this.lower_left.ycrd() + this.height;
		double T = Constants.TOLERANCE;
		PointT ul = new PointT(llx, llyh);
		PointT ur = new PointT(llxw, llyh);
		PointT lr = new PointT(llxw, lly);

		if (px < llx) {
			if (py < lly) {
				return p.dist(this.lower_left) <= T;
			} else if (lly <= py && py <= llyh) {
				return px >= llx - T;
			} else {
				return p.dist(ul) <= T;
			}
		} else if (llx <= px && px <= llxw) {
			if (py < lly) {
				return py >= lly - T;
			} else if (lly <= py && py <= llyh) {
				return true;
			} else {
				return py <= llyh + T;
			}
		} else {
			if (py < lly) {
				return p.dist(lr) <= T;
			} else if (lly <= py && py <= llyh) {
				return px <= llxw + T;
			} else {
				return p.dist(ur) <= T;
			}
		}
	}
	
}