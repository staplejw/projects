COMP SCI 2XB3
Justin Staples
001052815
March 05, 2017
The work that I am submitting is my own individual work. 

Design Decisions:

 - My implementations of merge sort and heap sort were developed with the help
of the Sedgewick algorithms textbook as a guide. Full credit goes to him and 
his team for producing these algorithms. The versions of merge sort and heap 
sort presented here are adopted from these versions and have been modified to 
suit the needs of this assignment. 

 - There are a number of available options for measuring times using stopwatch. 
 I decided to go with the example that was shown in the Lab 5 walkthrough. This was
 also adopted from Sedgewick algorithms, so full credit to him for providing this 
 class.
 
 - My project contains a test suite called SortTest that runs InsertionTest, MergeTest, 
 and HeapTest. InsertionTest contains three methods, each tests one of the insertion 
 sort routines, for a total of 5 test methods. 
 
 - Instead of putting all of my stopwatch measurement in the testing environment, I chose 
 to create a separate class called RunTime. I did this to avoid having a lot of clutter
 and repeated code in my test classes, as well to make my program more modular. RunTime
 simply contains one method that just runs all the test and outputs them to the correct 
 output file.
 
 - I have also included another extra class called GenJobs. This class also has just one 
 method, which reads all the input data from the file and creates an array list of jobs 
 to be processed. Again, I think having separate classes for reading my input and writing 
 my output makes my program more modular and easier to understand. 