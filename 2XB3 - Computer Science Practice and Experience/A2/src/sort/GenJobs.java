package sort;
import java.io.*;
/**
 * This is separate class that just contains one method for 
 * generating an array list of all the Job objects
 * @author Justin Staples
 * @since 02/03/2017
 */
import java.util.*;

class GenJobs {
	/**
	 * This method reads the input file and creates new Job objects.
	 * @return An array list of all the Jobs in the input file
	 */
	public static List<Job[]> generate() {
		List<Job[]> all = new ArrayList<Job[]>(); // array list will hold 5 arrays, one for each line of the input file
		int[] sizes = {16, 64, 256, 1024, 4096, 16384, 65536, 262144}; // known sizes of the input arrays
//		, 16384, 65536, 262144
		Scanner x; 
		try {
			x = new Scanner(new File("data/a2_in.txt")); // read data from file
			for (int i = 0; i < sizes.length; i++) {
				Job[] jobs = new Job[sizes[i]]; // for each size, create a new array of jobs
				String line = x.next(); // line is the next line of the file
				StringTokenizer st = new StringTokenizer(line, "},{"); // break up each line into job fields
				for (int j = 0; j < sizes[i]; j++) { // for each set of three tokens, create a new job
					String id = st.nextToken();
					int p = Integer.parseInt(st.nextToken());
					int a = Integer.parseInt(st.nextToken());
					jobs[j] = new Job(id, p, a); // fill the array with the new jobs
				}
				all.add(jobs); // add each array to the array list
			}
		} catch(Exception e) {
			e.printStackTrace();
		}
		return all; // return the list of job arrays;
	}
	
}
