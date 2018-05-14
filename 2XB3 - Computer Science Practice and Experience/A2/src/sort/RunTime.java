package sort;

import java.io.*;
import java.util.*;

/**
 * This is a separate class that contains a single method, times().
 * this method performs all stopwatch measurements for all the sorts for 
 * all 8 data sets. Every time this class is run, a new set of results are written
 * (in tabular form) to the output file a2_out.txt.
 * @author Justin
 *
 */
public class RunTime {
	
	/**
	 * This method runs all of the sorts for all data sets and writes the results in a 
	 * tabular format to the correct output file.
	 */
	private static void times() {
		FileWriter y;
		try {
			y = new FileWriter("data/a2_out.txt", true);
			
			// Regular insertion sort
			y.write("\n");
			y.write("Insertion Sort (normal)\n");
			y.write("Data set size\t\t\tRunning Time (s)\n");
			y.write("----------------------------------------\n");
			List<Job[]> all = GenJobs.generate();
			for (int i = 0; i < all.size(); i++) {
				Stopwatch stopwatch = new Stopwatch();
				double startTime = stopwatch.elapsedTime();
				Insertion.sortInsert(all.get(i));
				double endTime = stopwatch.elapsedTime();
				double elapsed = (endTime - startTime);
				y.write(String.format("%04d\t\t\t\t\t%f\n", all.get(i).length, elapsed));
			}
			
			// Comparable insertion sort
			y.write("\n");
			y.write("Insertion Sort (Comparable)\n");
			y.write("Data set size\t\t\tRunning Time (s)\n");
			y.write("----------------------------------------\n");
			all = GenJobs.generate();
			for (int i = 0; i < all.size(); i++) {
				Stopwatch stopwatch = new Stopwatch();
				double startTime = stopwatch.elapsedTime();
				Insertion.sortComparable(all.get(i), all.get(i).length);
				double endTime = stopwatch.elapsedTime();
				double elapsed = (endTime - startTime);
				y.write(String.format("%04d\t\t\t\t\t%f\n", all.get(i).length, elapsed));
			}
			
			// Binary insertion sort
			y.write("\n");
			y.write("Insertion Sort (binary search)\n");
			y.write("Data set size\t\t\tRunning Time (s)\n");
			y.write("----------------------------------------\n");
			all = GenJobs.generate();
			for (int i = 0; i < all.size(); i++) {
				Stopwatch stopwatch = new Stopwatch();
				double startTime = stopwatch.elapsedTime();
				Insertion.sortBinary(all.get(i), all.get(i).length);
				double endTime = stopwatch.elapsedTime();
				double elapsed = (endTime - startTime);
				y.write(String.format("%04d\t\t\t\t\t%f\n", all.get(i).length, elapsed));
			}
			
			// Merge sort
			y.write("\n");
			y.write("Merge Sort\n");
			y.write("Data set size\t\t\tRunning Time (s)\n");
			y.write("----------------------------------------\n");
			all = GenJobs.generate();
			for (int i = 0; i < all.size(); i++) {
				Stopwatch stopwatch = new Stopwatch();
				double startTime = stopwatch.elapsedTime();
				Merge.sortMerge(all.get(i), all.get(i).length);
				double endTime = stopwatch.elapsedTime();
				double elapsed = (endTime - startTime);
				y.write(String.format("%04d\t\t\t\t\t%f\n", all.get(i).length, elapsed));
			}
			
			// Heap sort
			y.write("\n");
			y.write("Heap Sort\n");
			y.write("Data set size\t\t\tRunning Time (s)\n");
			y.write("----------------------------------------\n");
			all = GenJobs.generate();
			for (int i = 0; i < all.size(); i++) {
				Stopwatch stopwatch = new Stopwatch();
				double startTime = stopwatch.elapsedTime();
				Heap.sortHeap(all.get(i), all.get(i).length);
				double endTime = stopwatch.elapsedTime();
				double elapsed = (endTime - startTime);
				y.write(String.format("%04d\t\t\t\t\t%f\n", all.get(i).length, elapsed));
			}
			
			y.close();
			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	
	public static void main(String [] args) {
		times();
	}

}
