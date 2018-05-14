/*
Title: assignment3.c
Author: Justin Staples
Partner: Mahmoud Khattab
Date: April 8th, 2018
Usage: gcc -o prog assignment3.c

This program provides implementations of common disk scheduling 
algorithms. It processes the requests in request.bin and then prints
the results to the console.
*/

#include <stdio.h> // reading file input 
#include <stdlib.h> // atoi
#include <string.h> // for easier string manipulation

typedef enum {RIGHT, LEFT} dir; // custom type for the head direction

int requests[20]; // integer array of requests
int initial_position; // first command line argument
dir direction; // second command line argument

// this compare function defines an ordering for integer requests (increasing)
// this function is passed to qsort where the sorting is performed
int compare(const void * a, const void * b) {
	int * x = (int *) a;
	int * y = (int *) b;
	return *x - *y;
}

void FCFS(int * requests, int initial_position, dir direction) {
	// initial movement to get to the first request
	int movement = abs(requests[0] - initial_position);

	// then, simply add the movements between successive requests
	for (int i = 1; i < 20; i++) {
		movement += abs(requests[i] - requests[i - 1]);
	}

	// print the output
	printf("FCFS DISK SCHEDULING ALGORITHM:\n");
	for (int i = 0; i < 20; i++) {
		printf("%d ", requests[i]);
	}

	printf("\n");
	printf("FCFS - Total head movements = %d\n", movement);
	printf("######################################################################\n");
}

void SSTF(int * requests, int initial_position, dir direction) {
	printf("SSTF DISK SCHEDULING ALGORITHM:\n");
	int movement = 0;

	// find the first request as the shortest seek time from the initial position
	int min = abs(requests[0] - initial_position);
	int index = 0;
	for (int i = 0; i < 20; i++) {
		if (abs(requests[i] - initial_position) < min) {
			min = abs(requests[i] - initial_position);
			index = i;
		}
	}
	movement += min; // increment the movement
	initial_position = requests[index]; // update the new position
	printf("%d ", initial_position); // print the output
	requests[index] = 10000; // set that index to a large value so it cannot be considered again

	// carry on in the same way for the other 19 requests	
	for (int j = 0; j < 19; j++) {
		int min = abs(requests[0] - initial_position);
		int index = 0;
		for (int i = 0; i < 20; i++) {
			if (abs(requests[i] - initial_position) < min) {
				min = abs(requests[i] - initial_position);
				index = i;
			}
		}
		movement += min;
		initial_position = requests[index];
		printf("%d ", initial_position);
		requests[index] = 10000;
	}

	printf("\n");
	printf("SSTF - Total head movements = %d\n", movement);
	printf("######################################################################\n");
}

void SCAN(int * requests, int initial_position, dir direction) {
	printf("SCAN DISK SCHEDULING ALGORITHM:\n");

	// start out by sorting the requests
	qsort(requests, 20, sizeof(int), compare);
	int movement;
	int upper;
	int lower;

	// split the requests into two groups, find upper and lower indices which serve as starting points for requests
	for (int i = 0; i < 20; i++) {
		if (requests[i] >= initial_position) {
			if (requests[i] == initial_position && direction == RIGHT) {
				upper = i;
				lower = i - 1;
			} else if (requests[i] == initial_position && direction == LEFT) {
				upper = i + 1;
				lower = i;
			} else {
				upper = i;
				lower = i - 1;
			}
			break;
		}
	}

	// if the head is moving left, start from lower and work down, then move to upper and work up
	if (direction == LEFT) {
		movement = abs(initial_position - 0) + abs(0 - requests[19]);
		for (int j = lower; j >= 0; j--) {
			printf("%d ", requests[j]);
		}
		for (int k = upper; k < 20; k++) {
			printf("%d ", requests[k]);
		}
	} else { // if the head is moving right, start from upper and work up, then move to lower and work down
		movement = abs(initial_position - 299) + abs(299 - requests[0]);
		for (int k = upper; k < 20; k++) {
			printf("%d ", requests[k]);
		}
		for (int j = lower; j >= 0; j--) {
			printf("%d ", requests[j]);
		}
	}

	printf("\n");
	printf("SCAN - Total head movements = %d\n", movement);
	printf("######################################################################\n");
}

void CSCAN(int * requests, int initial_position, dir direction) {
	printf("C-SCAN DISK SCHEDULING ALGORITHM:\n");

	// start out by sorting the requests
	qsort(requests, 20, sizeof(int), compare);
	int movement;
	int upper;
	int lower;

	// split the requests into two groups, find upper and lower indices which serve as starting points for requests
	for (int i = 0; i < 20; i++) {
		if (requests[i] >= initial_position) {
			if (requests[i] == initial_position && direction == RIGHT) {
				upper = i;
				lower = i - 1;
			} else if (requests[i] == initial_position && direction == LEFT) {
				upper = i + 1;
				lower = i;
			} else {
				upper = i;
				lower = i - 1;
			}
			break;
		}
	}

	// if the head is moving left, start from lower and work down, then move to the other end and work down to upper
	if (direction == LEFT) {
		movement = abs(initial_position - 0) + abs(299 - 0) + abs(299 - requests[upper]);
		for (int j = lower; j >= 0; j--) {
			printf("%d ", requests[j]);
		}
		for (int k = 19; k >= upper; k--) {
			printf("%d ", requests[k]);
		}
	} else { // if the head is moving right, start from upper and work up, then move to the other end and work up to lower
		movement = abs(initial_position - 299) + abs(299 - 0) + abs(0 - requests[lower]);
		for (int k = upper; k < 20; k++) {
			printf("%d ", requests[k]);
		}
		for (int j = 0; j <= lower; j++) {
			printf("%d ", requests[j]);
		}
	}

	printf("\n");
	printf("C-SCAN - Total head movements = %d\n", movement);
	printf("######################################################################\n");
}

void LOOK(int * requests, int initial_position, dir direction) {
	printf("LOOK DISK SCHEDULING ALGORITHM:\n");

	// start out by sorting the requests
	qsort(requests, 20, sizeof(int), compare);
	int movement;
	int upper;
	int lower;

	// split the requests into two groups, find upper and lower indices which serve as starting points for requests
	for (int i = 0; i < 20; i++) {
		if (requests[i] >= initial_position) {
			if (requests[i] == initial_position && direction == RIGHT) {
				upper = i;
				lower = i - 1;
			} else if (requests[i] == initial_position && direction == LEFT) {
				upper = i + 1;
				lower = i;
			} else {
				upper = i;
				lower = i - 1;
			}
			break;
		}
	}

	// if the head is moving left, start from lower and work down, then move to upper and work up
	if (direction == LEFT) {
		movement = abs(initial_position - requests[0]) + abs(requests[0] - requests[19]);
		for (int j = lower; j >= 0; j--) {
			printf("%d ", requests[j]);
		}
		for (int k = upper; k < 20; k++) {
			printf("%d ", requests[k]);
		}
	} else { // if the head is moving right, start from upper and work up, then move to lower and work down
		movement = abs(initial_position - requests[19]) + abs(requests[19] - requests[0]);
		for (int k = upper; k < 20; k++) {
			printf("%d ", requests[k]);
		}
		for (int j = lower; j >= 0; j--) {
			printf("%d ", requests[j]);
		}
	}

	printf("\n");
	printf("LOOK - Total head movements = %d\n", movement);
	printf("######################################################################\n");
}

void CLOOK(int * requests, int initial_position, dir direction) {
	printf("C-LOOK DISK SCHEDULING ALGORITHM:\n");

	// start out by sorting the requests
	qsort(requests, 20, sizeof(int), compare);
	int movement;
	int upper;
	int lower;

	// split the requests into two groups, find upper and lower indices which serve as starting points for requests
	for (int i = 0; i < 20; i++) {
		if (requests[i] >= initial_position) {
			if (requests[i] == initial_position && direction == RIGHT) {
				upper = i;
				lower = i - 1;
			} else if (requests[i] == initial_position && direction == LEFT) {
				upper = i + 1;
				lower = i;
			} else {
				upper = i;
				lower = i - 1;
			}
			break;
		}
	}

	// if the head is moving left, start from lower and work down, then move to the other end and work down to upper
	if (direction == LEFT) {
		movement = abs(initial_position - requests[0]) + abs(requests[19] - requests[0]) + abs(requests[19] - requests[upper]);
		for (int j = lower; j >= 0; j--) {
			printf("%d ", requests[j]);
		}
		for (int k = 19; k >= upper; k--) {
			printf("%d ", requests[k]);
		}
	} else { // if the head is moving right, start from upper and work up, then move to the other end and work up to lower
		movement = abs(initial_position - requests[19]) + abs(requests[19] - requests[0]) + abs(requests[0] - requests[lower]);
		for (int k = upper; k < 20; k++) {
			printf("%d ", requests[k]);
		}
		for (int j = 0; j <= lower; j++) {
			printf("%d ", requests[j]);
		}
	}

	printf("\n");
	printf("C-LOOK - Total head movements = %d\n", movement);
	printf("######################################################################\n");
}

int main(int argc, char * argv[]) {
	// error check the number of arguments
	if (argc != 3) {
		printf("Please enter the intial position of the disk head (0 - 299), followed by the head direction ('LEFT' or 'RIGHT')\n");
		return -1;
	}

	// error check the initial position of the disk head
	if (atoi(argv[1]) < 0 || atoi(argv[1]) > 299) {
		printf("First argument must be an integer ranging from 0 to 299\n");
		return -1;
	}

	// error check the direction of the head
	if (strcmp(argv[2], "LEFT") != 0 && strcmp(argv[2], "RIGHT") != 0) {
		printf("Second argument must be the string 'LEFT' or 'RIGHT'\n");
		return -1;
	}

	// fill in globals using command line arguments
	initial_position = atoi(argv[1]);
	dir direction = strcmp(argv[2], "RIGHT") == 0 ? RIGHT : LEFT;

	// if valid arguments are given, read the contents of the binary file into an array
	FILE * file = fopen("request.bin", "rb");
	fread(&requests, sizeof(int), 20, file);
	fclose(file);

	FCFS(requests, initial_position, direction);
	SSTF(requests, initial_position, direction);

	// all algorithms (except FCFS) modify the contents of the requests array, so this re-initializes it
	file = fopen("request.bin", "rb");
	fread(&requests, sizeof(int), 20, file);
	fclose(file);

	SCAN(requests, initial_position, direction);

	file = fopen("request.bin", "rb");
	fread(&requests, sizeof(int), 20, file);
	fclose(file);

	CSCAN(requests, initial_position, direction);

	file = fopen("request.bin", "rb");
	fread(&requests, sizeof(int), 20, file);
	fclose(file);

	LOOK(requests, initial_position, direction);

	file = fopen("request.bin", "rb");
	fread(&requests, sizeof(int), 20, file);
	fclose(file);

	CLOOK(requests, initial_position, direction);

	return 0;
}