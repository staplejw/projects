/** 
 * This class is a run-time exception. It is thrown when there 
 * are invalid inputs for the PointT constructor.
 * @author Justin Staples (staplejw, 001052815)
 * @since March 19th, 2017
 */
public class InvalidPointException extends RuntimeException {
	/** 
	 * This is the constructor for InvalidPointException.
	 * @param s message that will be show when exception is thrown.
	 */
	public InvalidPointException(String s) {
		super(s);
	}
}