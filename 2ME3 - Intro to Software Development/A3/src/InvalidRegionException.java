/** 
 * This class is a run-time exception. It is thrown when invalid 
 * inputs are given to the RegionT constructor.
 * @author Justin Staples (staplejw, 001052815)
 * @since March 19th, 2017
 */
public class InvalidRegionException extends RuntimeException {
	/** 
	 * This is the constructor for InvalidRegionException.
	 * @param s message that will be show when exception is thrown.
	 */
	public InvalidRegionException(String s) {
		super(s);
	}
}