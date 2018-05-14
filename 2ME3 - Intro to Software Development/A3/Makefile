##########################################
# Author: 	Justin Staples   			 #
# Revised: 	Sunday, March 19th, 2017	 #
# Description:	"MAKEFILE"		     	 #
##########################################

.SUFFIXES: .java .class
.java.class:
	javac -g -cp $(CLASSPATH):.:src:/usr/share/java/junit4.jar $*.java

CLASSES = \
	src/Constants.java \
	src/PointT.java \
	src/InvalidPointException.java \
	src/RegionT.java \
	src/GenericList.java \
	src/InvalidRegionException.java \
	src/PathT.java \
	src/Obstacles.java \
	src/Destinations.java \
	src/SafeZone.java \
	src/FullSequenceException.java \
	src/InvalidPositionException.java \
	src/Map.java \
	src/PathCalculation.java \
	src/TestPathCalculation.java \

MAIN = TestPathCalculation

test: classes junit

doc: 
	doxygen doxConfig
	cd latex && $(MAKE)
	echo '**********************************************************'
	echo '* 				MESSAGE TO MARKER!!!!		   	       *'
	echo '*														   *'
	echo '*	MY DOXYGEN HTML LINKS WORK WELL ON MY MACHINE, BUT DO  *'
	echo '* NOT SEEM TO WORK PROPERLY ON MILLS. I AM NOT SURE IF   *'
	echo '* THIS WILL BE THE SAME FOR YOU. MY DOCUMENTATION IS     *'
	echo '* COMPLETE THOUGH AND CAN BE VIEWED WITH THE refman.pdf  *'
	echo '* THAT IS LOCATED IN THE LATEX FOLDER. THANK YOU. 	   *'
	echo '**********************************************************'

classes: $(CLASSES:.java=.class)

junit: src/$(MAIN).class
	java -cp $(CLASSPATH):.:src:/usr/share/java/junit4.jar org.junit.runner.JUnitCore $(MAIN)

clean:
	$(RM) src/*.class
	rm -rf html
	rm -rf latex