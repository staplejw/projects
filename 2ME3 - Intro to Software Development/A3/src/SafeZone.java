/** 
 * This class represents the abstract data type
 * for a Path. This class extends GenericList, and 
 * is a list of regions.
 * @author Justin Staples (staplejw, 001052815)
 * @since March 19th, 2017
 */
public class SafeZone extends GenericList<RegionT> {

	/** 
	 * SafeZone uses a different max size, which is equal to 1.
	 */
	public static final int MAX_SIZE = 1;

	/** 
	 * The add method is redefined for SafeZone to allow the use of
	 * its different max size. This is needed for FullSequenceException 
	 * to be thrown at the right time.
	 * @param i index where the element will be added.
	 * @param p the element that will be added.
	 */
	public void add(int i, RegionT p) {
		if (this.size() == MAX_SIZE) {
			throw new FullSequenceException("The maximum size cannot be exceeded");
		}
		if (!(0 <= i && i <= this.size())) {
			throw new InvalidPositionException("That index is not a valid position");
		}
		s.add(i, p);
	}

}