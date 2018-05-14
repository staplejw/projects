import java.util.ArrayList;

/** 
 * This class contains represents the abstract data type
 * for a generic list of objects.
 * @author Justin Staples (staplejw, 001052815)
 * @since March 19th, 2017
 */
public class GenericList<T> {

	/**
	 * The sequence that is used that contains the elements.
	 */
	protected ArrayList<T> s;
	/**
	 * The maximum size of the list (100).
	 */
	public static final int MAX_SIZE = 100;

	/** 
	 * This is the constructor for GenericList.
	 */
	public GenericList() {
		this.s = new ArrayList<T>();
	}

	/** 
	 * This is the method for adding elements to the list
	 * at a particular index.
	 * @param i index where the element will be added.
	 * @param p the element that will be added.
	 */
	public void add(int i, T p) {
		if (this.size() == MAX_SIZE) {
			throw new FullSequenceException("The maximum size cannot be exceeded");
		}
		if (!(0 <= i && i <= this.size())) {
			throw new InvalidPositionException("That index is not a valid position");
		}
		s.add(i, p);
	}

	/** 
	 * This is the method for deleting elements from the list
	 * at a particular index.
	 * @param i index where the element will be deleted.
	 */
	public void del(int i) {
		if (!(0 <= i && i <= this.size() - 1)) {
			throw new InvalidPositionException("That index is not a valid position");
		}
		s.remove(i);
	}

	/** 
	 * This is the method for setting the value for a 
	 * particular index.
	 * @param i index where the element will be set.
	 * @param p the element that will be added.
	 */
	public void setval(int i, T p) {
		if (!(0 <= i && i <= this.size() - 1)) {
			throw new InvalidPositionException("That index is not a valid position");
		}
		s.set(i, p);
	}

	/** 
	 * This is the method for getting the value at a
	 * particular index
	 * @param i index of the value that is being returned.
	 * @return returns the element at that index.
	 */
	public T getval(int i) {
		if (!(0 <= i && i <= this.size() - 1)) {
			throw new InvalidPositionException("That index is not a valid position");
		}
		return s.get(i);
	}	

	/** 
	 * This is the method for getting the size, which tells
	 * how many elements are in the list.
	 * @return How many elements are in the list.
	 */
	public int size() {
		return s.size();
	}

}