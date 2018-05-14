package sort;

/**
 * This is a stopwatch class that was used in lab walkthrough 5. It uses 
 * millisecond time to measure the time between two events.
 * @author Justin
 * @since 02/03/2017
 */
public class Stopwatch { 

    private final long start;

    /**
     * Constructor for new stopwatch object.
     */
    public Stopwatch() {
        start = System.currentTimeMillis();
    } 

    /**
     * This method calculates the elapsed time since the stopwatch 
     * @return the time since the stopwatch has been created.
     */
    public double elapsedTime() {
        long now = System.currentTimeMillis();
        return (now - start) / 1000.0;
    }

} 
