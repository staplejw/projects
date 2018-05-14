import org.junit.*;
import static org.junit.Assert.*;

/** 
 * This class serves as a testing class for all the 
 * methods in PathCalculation.
 * @author Justin Staples (staplejw, 001052815)
 * @since March 19th, 2017
 */
public class TestPathCalculation {

    /** 
     * sample paths for unit testing
     */
	private PathT p0, p1, p2, p3, p4, p5, p6, p7;

    /** 
     * tolerance for assertEquals tests
     */
	private static final double DELTA = 1e-4;

    /** 
     * This method is the set up routine. It populates
     * all of the sample paths with new points.
     */
    @Before
    public void setUp()
    {
    	// p0 : path with 0 points, length 0
    	p0 = new PathT();
    	p1 = new PathT();
    	p2 = new PathT();
    	p3 = new PathT();
    	p4 = new PathT();
    	p5 = new PathT();
    	p6 = new PathT();
    	p7 = new PathT();

    	// p1 : path with 1 point, length 0
    	p1.add(0, new PointT(0, 0));

    	// p2 : path with 2 points
    	p2.add(0, new PointT(1, 3));
    	p2.add(1, new PointT(1, 4));

    	// p3 : simple path with 1 turn
    	p3.add(0, new PointT(0, 0));
    	p3.add(1, new PointT(3, 0));
    	p3.add(2, new PointT(3, 4));

    	// p4 : simple path with colinear segments, 0 turns
    	p4.add(0, new PointT(0, 0));
    	p4.add(1, new PointT(1, 1));
    	p4.add(2, new PointT(2, 2));
    	p4.add(3, new PointT(3, 3));

    	// p5 : path with multiple cw and ccw turns
    	p5.add(0, new PointT(0, 0));
    	p5.add(1, new PointT(1, 0));
    	p5.add(2, new PointT(1, 1));
    	p5.add(3, new PointT(2, 1));
    	p5.add(4, new PointT(2, 0));
    	p5.add(5, new PointT(3, 0));

    	// p6 : path with just two coincident points, length 0
    	p6.add(0, new PointT(2, 3));
    	p6.add(1, new PointT(2, 3));

    	// p7 : complex path that crosses over itself multiple times
    	p7.add(0, new PointT(0, 0));
    	p7.add(1, new PointT(1, 2));
    	p7.add(2, new PointT(2, 1));
    	p7.add(3, new PointT(1, 0));
    	p7.add(4, new PointT(2, 0));
    	p7.add(5, new PointT(2, 2));
    	p7.add(6, new PointT(1, 1));
    	p7.add(7, new PointT(0, 2));
    	p7.add(8, new PointT(0, 1));

    }

    /** 
     * This method is the tear down routine. It sets all
     * of the paths to null.
     */
    @After
    public void tearDown()
    {
      	p0 = null;
      	p1 = null;
      	p2 = null;
      	p3 = null;
      	p4 = null;
      	p5 = null;
      	p6 = null;
      	p7 = null;
    }

    /** 
     * This method tests totalDistance.
     */
    @Test
    public void testtotalDistance() {
    	assertEquals(PathCalculation.totalDistance(p0), 0, DELTA);
      assertEquals(PathCalculation.totalDistance(p1), 0, DELTA);
    	assertEquals(PathCalculation.totalDistance(p2), 1, DELTA);
    	assertEquals(PathCalculation.totalDistance(p3), 7, DELTA);
    	assertEquals(PathCalculation.totalDistance(p4), 4.24264, DELTA);
    	assertEquals(PathCalculation.totalDistance(p5), 5, DELTA);
    	assertEquals(PathCalculation.totalDistance(p6), 0, DELTA);
    	assertEquals(PathCalculation.totalDistance(p7), 11.89292, DELTA);
    }

    /** 
     * This method tests totalTurns.
     */
    @Test 
    public void testtotalTurns()
    { 
    	assertEquals(PathCalculation.totalTurns(p0), 0);
    	assertEquals(PathCalculation.totalTurns(p1), 0);
    	assertEquals(PathCalculation.totalTurns(p2), 0);
    	assertEquals(PathCalculation.totalTurns(p3), 1);
    	assertEquals(PathCalculation.totalTurns(p4), 0);
    	assertEquals(PathCalculation.totalTurns(p5), 4);
    	assertEquals(PathCalculation.totalTurns(p6), 0);
    	assertEquals(PathCalculation.totalTurns(p7), 7);
    } 

    /** 
     * This method tests estimatedTime.
     */
    @Test
    public void testestimatedTime() {
    	assertEquals(PathCalculation.estimatedTime(p0), 0, DELTA);
    	assertEquals(PathCalculation.estimatedTime(p1), 0, DELTA);
    	assertEquals(PathCalculation.estimatedTime(p2), 0.06667, DELTA);
    	assertEquals(PathCalculation.estimatedTime(p3), 0.51903, DELTA);
    	assertEquals(PathCalculation.estimatedTime(p4), 0.28284, DELTA);
    	assertEquals(PathCalculation.estimatedTime(p5), 0.54278, DELTA);
    	assertEquals(PathCalculation.estimatedTime(p6), 0, DELTA);
    	assertEquals(PathCalculation.estimatedTime(p7), 1.24865, DELTA);    
    }
    
}