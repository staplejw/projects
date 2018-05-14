package sort;

/**
 * This class contains the methods for using the merge sort
 * algorithm.
 * @author Justin Staples
 * @since 02/03/2017
 */
public class Merge {
	/**
	 * merge sort requires an auxilliary array to merge.
	 */
	private static Comparable[] aux;
	
	/**
	 * This method merges two sub arrays that are already sorted 
	 * @param x - the array of job to be sorted 
	 * @param lo - the lower bound on the index
	 * @param mid - the mid way index of the array, the point at which it is split
	 * @param hi - the upper bound on the index of the array
	 */
	private static void merge(Comparable[] x, int lo, int mid, int hi) {
		int i = lo;
		int j = mid + 1;
		
		for (int k = lo; k <= hi; k++) {
			aux[k] = x[k];
		}
		
		for (int k = lo; k <= hi; k++) {
			if (i > mid) {
				x[k] = aux[j++];
			} else if (j > hi) {
				x[k] = aux[i++];
			} else if (aux[j].compareTo(aux[i]) < 0) {
				x[k] = aux[j++];
			} else {
				x[k] = aux[i++];
			}
		}
		
	}
	
	/**
	 * This method is a sub routine for merge sort. It is a recursive method that 
	 * splits the array and then merges it.
	 * @param x - the array of jobs
	 * @param lo - the lower bound on the index 
	 * @param hi - the lower bound on the index
	 */
	private static void sort(Comparable[] x, int lo, int hi) {
		if (hi <= lo) {
			return;
		}
		int mid = lo + (hi - lo) / 2;
		sort(x, lo, mid);
		sort(x, mid + 1, hi);
		merge(x, lo, mid, hi);
	}
	
	/**
	 * This is the method for merge sort. It uses the subroutine sort and indexes the full 
	 * size of the array.
	 * @param x - the array of jobs
	 * @param n - the size of the array
	 */
	public static void sortMerge ( Comparable[] x, int n ) {
		aux = new Comparable[n];
		sort(x, 0, n - 1);
	}
	
}
