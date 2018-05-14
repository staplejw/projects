/* 
Title: script.c
Author: Justin Staples
Date: January 26th, 2018
Usage: gcc -o script script.c

A recursive descent parser for the following EBNF grammar, with Q as the 
starting symbol. 

Q 	->	'w' '(' E ')' '{' {S} '}'
S	->	V '=' E ';'
V   ->  I ['[' E ']']
E   ->  '(' E ')'
E   ->  N ('+' | '-') N
E   ->  B ('|' | '&') B
N   ->  D {D}
I   ->  L {L} 
D   ->  '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '0' |  
L   ->  'a' | 'b' | 'c' | 'd' | 'e'
B   ->  't' | 'f'

Here are some examples of sentences that are accepted by the grammar:

w(1+2){a=4+5;}
w(2+4){b[3-4]=t|f;}
w((3-5)){c[(((1+1)))]=1+1;}
w(245136687-11996684){}
w(((f&f))){dedede[t|t]=2+3;}
w(1+1){a=4-5;c=t&f;}
w(((666+111))){abc[(t|f)]=1+1;e=(1+1);}
*/

#include <stdio.h> // input/output
#include <ctype.h> // isalpha, isdigit

// global variable declarations
int charClass; // group the keyboard characters into classes
char nextChar; // read the next character in the sentence
int nextToken; // identify the next token in the sentence
int accepted; // determine if the sentence is accepted by the language

char sentence[100]; // user input is stored in this variable
int counter = 0; // counter for iterating through the sentence

// character classes
#define LETTER 2
#define DIGIT 1
#define OTHER 99

// token codes
#define INT_LIT 16
#define IDENT 17
#define BOO 18
#define LEFT_PAREN 19
#define RIGHT_PAREN 20
#define LEFT_SQUARE 21
#define RIGHT_SQUARE 22
#define LEFT_SQUIGLY 23
#define RIGHT_SQUIGLY 24
#define ASSIGN_OP 25
#define PIPE 26
#define AMPERSAND 27
#define SEMICOLON 28
#define DOUBLE_U 29
#define PLUS_OP 30
#define MINUS_OP 33

// lookup table for special characters that have their own token code
int lookup(char ch) {
	switch (ch) {
		case '(':
			nextToken = LEFT_PAREN;
			break;
		case ')':
			nextToken = RIGHT_PAREN;
			break;
		case '[':
			nextToken = LEFT_SQUARE;
			break;
		case ']':
			nextToken = RIGHT_SQUARE;
			break;
		case '{':
			nextToken = LEFT_SQUIGLY;
			break;
		case '}':
			nextToken = RIGHT_SQUIGLY;
			break;
		case '=':
			nextToken = ASSIGN_OP;
			break;
		case '|':
			nextToken = PIPE;
			break;
		case '&':
			nextToken = AMPERSAND;
			break;
		case ';':
			nextToken = SEMICOLON;
			break;
		case '+':
			nextToken = PLUS_OP;
			break;
		case '-':
			nextToken = MINUS_OP;
			break;
	}
	return nextToken;
}

// grabs the next character in the input sentence and assigns it the correct character class
void get() {
	nextChar = sentence[counter++];
	// printf("Next character: %c\n", nextChar);
	if (isalpha(nextChar)) {
		charClass = LETTER;
	} else if (isdigit(nextChar)) {
		charClass = DIGIT;
	} else {
		charClass = OTHER;
	}
}

// lex grabs the next character and then uses the character class to assign the correct token
int lex() {
	get();

	switch (charClass) {
		case LETTER:
			switch (nextChar) {
				case 'w':
					nextToken = DOUBLE_U;
					break;
				case 'a':
				case 'b':
				case 'c':
				case 'd':
				case 'e':
					nextToken = IDENT;
					break;
				case 't':
				case 'f':
					nextToken = BOO;
					break;
			} 
			break;
		case DIGIT:
			nextToken = INT_LIT;
			break;
		case OTHER:
			lookup(nextChar);
			break;
	}
	return nextToken;
}

// parses terms in the language generated by the production B
void B() {
	switch (nextChar) {
		case 't':
		case 'f':
			lex();
			break;
		default:
			accepted = 0;
			return;
	} 
}

// parses terms in the language generated by the production L
void L() {
	switch (nextChar) {
		case 'a':
		case 'b':
		case 'c':
		case 'd':
		case 'e':
			lex();
			break;
		default:
			accepted = 0;
			return;
	}
}

// parses terms in the language generated by the production D
void D() {
	switch (nextChar) {
		case '0':
		case '1':
		case '2':
		case '3':
		case '4':
		case '5':
		case '6':
		case '7':
		case '8':
		case '9':
			lex();
			break;
		default:
			accepted = 0;
			return;
	}
}

// parses terms in the language generated by the production I
void I() {
	L();
	while (nextToken == IDENT) {
		L();
	}
}

// parses terms in the language generated by the production N
void N() {
	D();
	// printf("ACCEPTED: %d\n", accepted);
	while (nextToken == INT_LIT) {
		D();
	}
}

// parses terms in the language generated by the production E
void E() {
	switch (nextToken) {
		case LEFT_PAREN:
			if (nextToken == LEFT_PAREN) {
				lex();
			} else {
				accepted = 0;
				return;
			}
			E();
			if (nextToken == RIGHT_PAREN) {
				lex();
			} else {
				accepted = 0;
				return;
			}
			break;
		case INT_LIT:
			N();
			if (nextToken == PLUS_OP || nextToken == MINUS_OP) {
				lex();
			}
			N();
			break;
		case BOO:
			B();
			if (nextToken == PIPE || nextToken == AMPERSAND) {
				lex();
			}
			B();
			break;
		default:
			accepted = 0;
			return;
	}
}

// parses terms in the language generated by the production V
void V() {
	I();
	if (nextToken == LEFT_SQUARE) {
		if (nextToken == LEFT_SQUARE) {
			lex();
		} else {
			accepted = 0;
			return;
		}
		E();
		if (nextToken == RIGHT_SQUARE) {
			lex();
		} else {
			accepted = 0;
			return;
		}
	}
}

// parses terms in the language generated by the production S
void S() {
	V();
	if (nextToken == ASSIGN_OP) {
		lex();
	} else {
		accepted = 0;
		return;
	}
	E();
	if (nextToken == SEMICOLON) {
		lex();
	} else {
		accepted = 0;
		return;
	}
}

// parses terms in the language generated by the production Q
void Q() {
	if (nextToken == DOUBLE_U) {
		lex();
	} else {
		accepted = 0;
		return;
	}
	if (nextToken == LEFT_PAREN) {
		lex();
	} else {
		accepted = 0;
		return;
	}
	E();
	if (nextToken == RIGHT_PAREN) {
		lex();
	} else {
		accepted = 0;
		return;
	}
	if (nextToken == LEFT_SQUIGLY) {
		lex();
	} else {
		accepted = 0;
		return;
	}
	while (nextToken == IDENT) {
		S();
	} 
	if (nextToken == RIGHT_SQUIGLY) {
		lex();
	} else {
		accepted = 0;
		return;
	}
}

/* the main method first prompts the user for an input sentence, 
then calls lex to grab the first character. After this, the method
for the start symbol, Q, is called, which begins the recursive descent. 
The sentence is either accepted or rejected and the result is printed to the terminal.
*/
int main() {
	accepted = 1; // automatically assume that every word will be accepted. Once a bad character is recognized, set accepted = 0

	printf("Please type the sentence that you would like to test, then press Enter\n");
	scanf("%s", sentence);

	lex();
	Q();

	accepted ? printf("accepted\n") : printf("rejected\n");
}













