package sort;
import java.util.*;
import java.io.*;

/**
 * This class contains the methods for using the heap sort
 * algorithm.
 * @author Justin Staples
 * @since 02/03/2017
 */
public class Heap {

	/**
	 * Sink is a subroutine for heap sort. It takes an element
	 * that is out of place in a binary heap and places it correctly.
	 * @param x - the input array of jobs
	 * @param i - the index of the job element that needs to be sunk
	 * @param n - the size of the input array
	 */
	private static void sink(Comparable[] x, int i, int n) {
		while (2*i <= n) { 
			int j = 2*i;
			if (j < n && x[j-1].compareTo(x[j]) < 0) {
				j++;
			}
			if (!(x[i-1].compareTo(x[j-1]) < 0)) {
				break;
			}
			Comparable temp = x[i-1];
			x[i-1] = x[j-1];
			x[j-1] = temp;
			i = j;
		}
	}
	/**
	 * Heap sort implemented with the comparable interface.
	 * @param x - the input array containing times of jobs that need to be sorted.
	 * @param n - the size of the input array
	 */
	public static void sortHeap ( Comparable[] x, int n ) {
		for (int i = n/2; i >= 1; i--) { // build a binary heap
			sink(x, i, n);
		}
		while (n > 1) {
			Comparable temp = x[0]; // exchange root of heap with the right most node, then sink
			x[0] = x[n-1];
			x[n-1] = temp;
			n--;
			sink(x, 1, n);
		}
	}
	
}
