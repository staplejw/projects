/** 
 * This class is a run-time exception. It is thrown when an 
 * invalid index is used on a list.
 * @author Justin Staples (staplejw, 001052815)
 * @since March 19th, 2017
 */
public class InvalidPositionException extends RuntimeException {
	/** 
	 * This is the constructor for InvalidPositionException.
	 * @param s message that will be show when exception is thrown.
	 */
	public InvalidPositionException(String s) {
		super(s);
	}
}