package sort;


/**
 * This class contains the methods for using the insertion sort
 * algorithms, with or without the comparable interface, as well as 
 * a binary search version.
 * @author Justin Staples
 * @since 02/03/2017
 */
public class Insertion {
	/**
	 * regular insertion sort
	 * @param x - the input array containing processing times of jobs that need to be sorted.
	 */
	public static void sortInsert ( Job[] x ) {
		int N = x.length;
		for (int i = 1; i < N; i++) {
			for (int j = i; j > 0; j--) {
				if (x[j].getArrivalTime() < x[j - 1].getArrivalTime()) {
					Job temp = x[j];
					x[j] = x[j - 1];
					x[j - 1] = temp;
				} else if (x[j].getArrivalTime() == x[j - 1].getArrivalTime()) {
					if (x[j].getProcessingTime() < x[j - 1].getProcessingTime()) {
						Job temp = x[j];
						x[j] = x[j - 1];
						x[j - 1] = temp;
					} else {
						break;
					}
				} else {
					break;
				}
			}
		}
	}
	/**
	 * insertion sort using Comparable
	 * @param x - the input array containing times of jobs that need to be sorted.
	 * @param n - the size of the input array
	 */
	public static void sortComparable ( Comparable[] x, int n ) {
		for (int i = 1; i < n; i++) {
			for (int j = i; j > 0 && x[j].compareTo(x[j - 1]) < 0 ; j--) {
					Comparable temp = x[j];
					x[j] = x[j - 1];
					x[j - 1] = temp;
			}
		}
	}

	/**
	 * This method uses the binary search algorithm to determine
	 * at what index an element should be inserted into an array.
	 * @param x - array of job objects
	 * @param y - the job to be inserted
	 * @param lo - the lower bound on the indexes considered
	 * @param hi - the upper boudn on the indexes considered
	 * @return The index where the job should be inserted
	 */
	private static int binaryIndex( Comparable[] x, Comparable y, int lo, int hi ) {
		if (hi < lo) {
			return lo;
		}
		int mid = lo + (hi - lo) / 2;
		int cmp = y.compareTo(x[mid]);
		if (cmp < 0) {
			return binaryIndex(x, y, lo, mid - 1);
		} else if (cmp > 0) {
			return binaryIndex(x, y, mid + 1, hi);
		} else {
			return mid;
		}
	}
	
	/**
	 * This method shifts all the indexes in array to the right one 
	 * spot to make room for the item being inserted
	 * @param x - array of job objects
	 * @param index - the index that shows where to start shifting
	 * @param current - the index of the current element to be inserted.
	 */
	private static void shift( Comparable[] x, int index, int current) {
		Comparable temp = x[current];
		for (int i = current; i > index; i--) {
			x[i] = x[i - 1];
		}
		x[index] = temp;
	}
	
	/**
	 * optimized insertion sort
	 * @param x - the input array containing times of jobs that need to be sorted.
	 * @param n - the size of the input array
	 */
	public static void sortBinary ( Comparable[] x, int n ) {
		for (int i = 1; i < n; i++) {
			int index = binaryIndex(x, x[i], 0, i - 1);
			shift(x, index, i);
		}
	}
	
	/**
	 * A method adopted from the textbook. Check to see
	 * if an array is sorted.
	 * @param x - the array under consideratino
	 * @return a boolean value. True, if the array is sorted and false otherwise.
	 */
	public static boolean isSorted( Comparable[] x ) {
		for (int i = 1; i < x.length; i++) {
			if (x[i].compareTo(x[i - 1]) < 0) {
				return false;
			}
		}
		return true;
	}
	
}
