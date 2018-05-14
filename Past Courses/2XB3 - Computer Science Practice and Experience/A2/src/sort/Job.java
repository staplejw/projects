package sort;

/**
 * Abstract data type represting jobs for the CPU to process
 * @author Justin
 * @since 02/03/2017
 */
public class Job implements Comparable<Job>{
	/**
	 * Instance variables for the Job type
	 */
	private String jobID;
	private int processingTime;
	private int arrivalTime;
	
	/**
	 * Constructor for the Job data type.
	 * @param id - The job ID
	 * @param pTime - The processing time of the job
	 * @param aTime - The arrival time of the job
	 */
	public Job(String id, int pTime, int aTime)
	{
		this.jobID = id;
		this.processingTime = pTime;
		this.arrivalTime = aTime;
	}
	
	/**
	 * Getter method for processing time.
	 * @return - returns the processing time of a job instance.
	 */
	public int getProcessingTime()
	{
		return this.processingTime;
	}
	
	/**
	 * Setter method for processing time
	 * @param t - The desired processing time of a certain job
	 */
	public void setProcessingTime(int t)
	{
		this.processingTime = t;
	}
	
	/**
	 * Getter method for arrival time.
	 * @return - returns the arrival time of a job instance.
	 */
	public int getArrivalTime()
	{
		return this.arrivalTime;
	}
	
	/**
	 * Setter method for arrival time
	 * @param t - The desired arrival time of a certain job
	 */
	public void setArrivalTime(int t)
	{
		this.arrivalTime = t;
	}
	
	/**
	 * Getter method for job ID.
	 * @return - returns the job ID string of a job instance.
	 */
	public String getJobID()
	{
		return this.jobID;
	}
	
	/**
	 * Setter method for job ID
	 * @param t - The desired job ID of a certain job
	 */
	public void setJobID(String id)
	{
		this.jobID = id;
	}
	
	/**
	 * This method is the compareTo method for Jobs. It allows 
	 * jobs to be directly comparable based on their arrival and
	 * processing time
	 * @param - another instance of type Job
	 * @return returns -1, 0, or 1 depending on if this job is less than that job, 
	 * equal to, or greather than.
	 */
	@Override
	public int compareTo(Job other)
	{
		if (this.arrivalTime > other.arrivalTime) {
			return 1;
		} else if (this.arrivalTime == other.arrivalTime) {
			if (this.processingTime > other.processingTime) {
				return 1;
			} else if (this.processingTime == other.processingTime) {
				return 0;
			} else {
				return -1;
			}
		} else {
			return -1;
		}
	}
	
	/**
	 * This method simply return a string version of the job
	 * @return a string that contains all of the fields of the job instance between parentheses. 
	 */
	public String toString()
	{
		return ("{" + jobID + "," + processingTime + "," + arrivalTime + "}");
	}

}
