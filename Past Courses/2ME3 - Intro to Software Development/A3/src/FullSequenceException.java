/** 
 * This class is a run-time exception. It is thrown when an attempt
 * is made to add to a full sequence.
 * @author Justin Staples (staplejw, 001052815)
 * @since March 19th, 2017
 */
public class FullSequenceException extends RuntimeException {
	/** 
	 * This is the constructor for FullSequenceException.
	 * @param s message that will be show when exception is thrown.
	 */
	public FullSequenceException(String s) {
		super(s);
	}
}