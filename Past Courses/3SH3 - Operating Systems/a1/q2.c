/*
Title: q2.c
Author: Justin Staples
Partner: Mahmoud Khattab
Date: February 12th, 2018

This program represents a very simple operating system shell, which 
can be used to enter commands like 'pwd' or 'ls'. It also has a history 
feature which keeps track of the most recent commands used.
*/

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <ctype.h>


#define MAX_LINE 80 // maximum number of characters per input

char ** history[] = {NULL, NULL, NULL, NULL, NULL, NULL}; // stores the history of commands
int noc = 0; //  number of commands entered so far

int main(void)  {

	char * line = (char *) malloc(MAX_LINE * sizeof(char)); // each command line input
	char * args[MAX_LINE/2 + 1]; // maximum number of arguments, 
    
    int should_run = 1; // exit command sets this flag to false
		
    while (should_run){   
        printf("osh> "); // prompt
        fflush(stdout); 
        fgets(line, MAX_LINE + 1, stdin); // grab user input
        
        // throw an error if too many characters are entered
        if (strlen(line) >= MAX_LINE) {
            printf("The maximum number of characters per line is 80\n");
            return -1;
        }

        // split the input into tokens and update the history
        int i = 0;
        char * word = strtok(line, " \t\n");
        while (word != NULL) {
            args[i] = word;
            word = strtok(NULL, " \t\n");
            i++;
        }
        printf("%d\n", noc);
        args[i] = NULL;
        if (noc < 6) {
            history[noc] = args;
        } else {
            for (int k = 4; i >= 0; i--) {
                history[k] = history[k + 1];
            }
            history[5] = args;
        }

        pid_t pid;
        // entering nothing but white space should just go back to the prompt
        if (i == 0) {} 
        // if just one token is entered...
        else if (i == 1) {
            // if the token is "!!" execute last command, if possible
            if (strcmp(args[i - 1], "!!") == 0) {
                pid = fork();
                if (pid == 0) { //  child
                    if (noc == 0) { // error
                        printf("No commands in history\n");
                        exit(1);
                    } else if (noc < 6) {
                        history[noc] = history[noc - 1];
                        execvp(history[noc][0], history[noc]);
                        noc++;
                        exit(0);
                    } else {
                        history[5] = history[4];
                        execvp(history[5][0], history[5]);
                        noc++;
                        exit(0);             
                    } 
                } else if (pid > 0) { // parent
                    wait(NULL);
                } // if the one token is !3 or something like that
            } else if (strlen(args[i - 1]) == 2 && strcmp(&args[i - 1][0], "!") == 0 && isdigit(args[i - 1][1])) {
                pid = fork();
                if (pid == 0) {
                    int num = atoi(&args[i - 1][1]);
                    if (num > 0 && num <= 5) {
                        if (noc == 0) {
                            printf("No such command in history\n");
                            exit(1);
                        } else if (noc < 6) {
                            if (noc - num >= 0) {
                                history[noc] = history[num - 1];
                                execvp(history[noc][0], history[noc]);
                                noc++;
                                exit(0);
                            } else {
                                printf("No such command in history\n");
                                exit(1);          
                            }
                        } else {
                            history[5] = history[num - 1];
                            execvp(history[5][0], history[5]);
                            noc++;
                            exit(0);   
                        } 
                    } 
                } else if (pid > 0) {
                    wait(NULL);
                } 
            } else { // otherwise just execute the command like normal
                pid = fork();
                if (pid == 0) {
                    noc++;
                    printf("%d\n", noc);
                    execvp(args[0], args);
                    exit(0);
                } else if (pid > 0) {
                    wait(NULL);
                }
            } 
        } else {
            pid = fork();
            if (pid == 0) {
                noc++;
                printf("%d\n", noc);
                execvp(args[0], args);
                exit(0);
            } else if (pid > 0) {
                wait(NULL);
            }
        }
    }
	return 0;
}