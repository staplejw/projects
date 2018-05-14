/*
Title: P0Scanner.cpp
Author: Justin Staples (001052815)
Parnter: Mahmoud Khattab (000853210)
Date: February 27th, 2018
Usage (on mills server): 
	g++ -std=c++0x -o script.out P0Scanner.cpp
	./script.out input.txt

This is a lexical analyzer for a simplified Pascal-like language 
called PO. The program takes one command line argument, which is 
the name of the input text file that will be analyzed. The output
of the lexical analysis is printed to the console. I have included 
an example program called "input.txt" which can be used to get an 
idea of how the program runs. 

*/

#include <stdlib.h> // atoi
#include <iostream> // output to console
#include <fstream> // reading from file stream
#include <string> // string manipulation

const int IdLen = 31; // number of significant characters in identifiers

// enumerated type for the symbols 
enum Symbols {
	null, TimesSym, DivSym, ModSym, AndSym, PlusSym, MinusSym
	, OrSym, EqlSym, NeqSym, LssSym, GeqSym, LeqSym, GtrSym
	, PeriodSym, CommaSym, ColonSym, RparenSym, RbrakSym, OfSym
	, ThenSym, DoSym, LparenSym, LbrakSym, NotSym, BecomesSym
	, NumberSym, IdentSym, SemicolonSym, EndSym, ElseSym, IfSym
	, WhileSym, ArraySym, RecordSym, ConstSym, TypeSym, VarSym
	, ProcedureSym, BeginSym, ProgramSym, EofSym
};

Symbols sym; // global for holding the current symbol
int val; // global for holding the value of a number
std::string id = ""; // global for holding the string identifier
int counter = 0;
bool error = false; // raise an error when an invalid character is detected

// maximum number of keywords
const int KW = 20;

// data structure for keywords. each one has its own symbol and string id
struct Keywords {
	Symbols sym;
	std::string id;
};

char ch; // global for holding the current character
int line = 1; // global for keeping track of the line location
int pos = 0; // global for keeping track of the position on each line
Keywords keyTab[20]; // array for holding the keywords

// initializing all of the keywords
struct Keywords OF = {Symbols::OfSym, "of"};
struct Keywords THEN = {Symbols::ThenSym, "then"};
struct Keywords DO = {Symbols::DoSym, "do"};
struct Keywords MOD = {Symbols::ModSym, "mod"};
struct Keywords END = {Symbols::EndSym, "end"};
struct Keywords ELSE = {Symbols::ElseSym, "else"};
struct Keywords IF = {Symbols::IfSym, "if"};
struct Keywords WHILE = {Symbols::WhileSym, "while"};
struct Keywords ARRAY = {Symbols::ArraySym, "array"};
struct Keywords RECORD = {Symbols::RecordSym, "record"};
struct Keywords CONST = {Symbols::ConstSym, "const"};
struct Keywords TYPE = {Symbols::TypeSym, "type"};
struct Keywords VAR = {Symbols::VarSym, "var"};
struct Keywords PROCEDURE = {Symbols::ProcedureSym, "procedure"};
struct Keywords BEGIN = {Symbols::BeginSym, "begin"};
struct Keywords PROGRAM = {Symbols::ProgramSym, "program"};

// after the character is grabbed, the line and position values are updated
void GetChar() {
    if (ch == '\n') {
    	line++;
    	pos = 0;
    } else {
        pos++;
    }
}

// used to mark where an error occurs
void Mark(std::string msg) {
	std::cout << "ERROR: " << msg << std::endl;
	std::cout << "Error at:" << std::endl;
	std::cout << "line: " << line << std::endl;
	std::cout << "position: " << pos << std::endl;
}

// for recognizing identifiers
void Ident(std::ifstream& is) {
	while (isalpha(is.peek())) {
		is.get(ch);
		pos++;
		if (counter < IdLen) {
			counter++;
			id += ch;
		}
	}
}

// for recognizing numbers
void Number(std::ifstream& is) {
	while (isdigit(is.peek())) {
		is.get(ch);
		pos++;
		val = 10 * val + atoi(&ch);
	}
}

// for recognizing comments
void Comment(std::ifstream& is) {	
	while (is.peek() != '}') {
		is.get(ch);
		pos++;
	}
	is.get(ch);
	pos++;
}

// lexcial analysis, looks at the characters and assigns the correct symbol
void GetSym(std::ifstream& is) {
	if (isalpha(ch)) {
		id += ch;
		counter++;
		Ident(is);
		counter = 0;

		if (id.compare(keyTab[0].id) == 0) {
			sym = Symbols::OfSym;
			std::cout << "OfSym" << std::endl;
		} else if (id.compare(keyTab[1].id) == 0) {
			sym = Symbols::ThenSym;
			std::cout << "ThenSym" << std::endl;
		} else if (id.compare(keyTab[2].id) == 0) {
			sym = Symbols::DoSym;
			std::cout << "DoSym" << std::endl;
		} else if (id.compare(keyTab[3].id) == 0) {
			sym = Symbols::ModSym;
			std::cout << "ModSym" << std::endl;
		} else if (id.compare(keyTab[4].id) == 0) {
			sym = Symbols::EndSym;
			std::cout << "EndSym" << std::endl;
		} else if (id.compare(keyTab[5].id) == 0) {
			sym = Symbols::ElseSym;
			std::cout << "ElseSym" << std::endl;
		} else if (id.compare(keyTab[6].id) == 0) {
			sym = Symbols::IfSym;
			std::cout << "IfSym" << std::endl;
		} else if (id.compare(keyTab[7].id) == 0) {
			sym = Symbols::WhileSym;
			std::cout << "WhileSym" << std::endl;
		} else if (id.compare(keyTab[8].id) == 0) {
			sym = Symbols::ArraySym;
			std::cout << "ArraySym" << std::endl;
		} else if (id.compare(keyTab[9].id) == 0) {
			sym = Symbols::RecordSym;
			std::cout << "RecordSym" << std::endl;
		} else if (id.compare(keyTab[10].id) == 0) {
			sym = Symbols::ConstSym;
			std::cout << "ConstSym" << std::endl;
		} else if (id.compare(keyTab[11].id) == 0) {
			sym = Symbols::TypeSym;
			std::cout << "TypeSym" << std::endl;
		} else if (id.compare(keyTab[12].id) == 0) {
			sym = Symbols::VarSym;
			std::cout << "VarSym" << std::endl;
		} else if (id.compare(keyTab[13].id) == 0) {
			sym = Symbols::ProcedureSym;
			std::cout << "ProcedureSym" << std::endl;
		} else if (id.compare(keyTab[14].id) == 0) {
			sym = Symbols::BeginSym;
			std::cout << "BeginSym" << std::endl;
		} else if (id.compare(keyTab[15].id) == 0) {
			sym = Symbols::ProgramSym;
			std::cout << "ProgramSym" << std::endl;
		} else {
			sym = Symbols::IdentSym;
			std::cout << "IdentSym" << std::endl;
		}		
		id = "";
	} else if (isdigit(ch)) {
		val = atoi(&ch);
		Number(is);
		sym = Symbols::NumberSym;
		std::cout << "NumberSym" << std::endl;
	} else {
		switch (ch) {
	        case ' ':
	        case '\t':
	        case '\n':
	            break;
	        case '{':
	        	Comment(is);
	        	break;
	        case '*':
	        	sym = Symbols::TimesSym;
	        	std::cout << "TimesSym" << std::endl;
	        	break;
	        case '/':
	        	sym = Symbols::DivSym;
	        	std::cout << "DivSym" << std::endl;
	        	break;
	        case '&':
	        	sym = Symbols::AndSym;
	        	std::cout << "AndSym" << std::endl;
	        	break;
	        case '+':
	        	sym = Symbols::PlusSym;
	        	std::cout << "PlusSym" << std::endl;
	        	break;
	        case '-':
	        	sym = Symbols::MinusSym;
	        	std::cout << "MinusSym" << std::endl;	
	        	break;
	        case '|':
	        	sym = Symbols::OrSym;
	        	std::cout << "OrSym" << std::endl;  
	        	break;      	
	        case '=':
	        	sym = Symbols::EqlSym;
	        	std::cout << "EqlSym" << std::endl;
	        	break;
	        case '#':
	        	sym = Symbols::NeqSym;
	        	std::cout << "NeqSym" << std::endl;
	        	break;
	        case '<':
	        	if (is.peek() == '=') {
	        		is.get(ch);
	        		pos++;
		        	sym = Symbols::LeqSym;
		        	std::cout << "LeqSym" << std::endl;
	        	} else {
		        	sym = Symbols::LssSym;
		        	std::cout << "LssSym" << std::endl;	        		
	        	} break;
	        case '>':
	        	if (is.peek() == '=') {
	        		is.get(ch);
	        		pos++;
		        	sym = Symbols::GeqSym;
		        	std::cout << "GeqSym" << std::endl;
	        	} else {
		        	sym = Symbols::GtrSym;
		        	std::cout << "GtrSym" << std::endl;	        		
	        	} break;
	        case '.':
	        	sym = Symbols::PeriodSym;
	        	std::cout << "PeriodSym" << std::endl;
	        	break;
	        case ',':
	        	sym = Symbols::CommaSym;
	        	std::cout << "CommaSym" << std::endl;
	        	break;
	        case ':':
	        	if (is.peek() == '=') {
	        		is.get(ch);
	        		pos++;
		        	sym = Symbols::BecomesSym;
		        	std::cout << "BecomesSym" << std::endl;
	        	} else {
		        	sym = Symbols::ColonSym;
		        	std::cout << "ColonSym" << std::endl;	        		
	        	} break;
	        case '(':
	        	sym = Symbols::LparenSym;
	        	std::cout << "LParenSym" << std::endl;	
	        	break;
	        case ')':
	        	sym = Symbols::RparenSym;
	        	std::cout << "RparenSym" << std::endl;  
	        	break;      	
	        case '[':
	        	sym = Symbols::LbrakSym;
	        	std::cout << "LbrakSym" << std::endl;
	        	break;
	        case ']':
	        	sym = Symbols::RbrakSym;
	        	std::cout << "RbrakSym" << std::endl;
	        	break;
	        case '~':
	        	sym = Symbols::NotSym;
	        	std::cout << "NotSym" << std::endl;
	        	break;
	        case ';':
	        	sym = Symbols::SemicolonSym;
	        	std::cout << "SemicolonSym" << std::endl;
	        	break;
	        default: 
	        	error = true;
	        	sym = Symbols::null;
	        	std::string error_msg = "invalid character";
	        	Mark(error_msg);
		}
	}
}

int main(int argc, char * argv[]) {
	// filling the ketTab array with the keywords
	keyTab[0] = OF;
	keyTab[1] = THEN;
	keyTab[2] = DO;
	keyTab[3] = MOD;
	keyTab[4] = END;
	keyTab[5] = ELSE;
	keyTab[6] = IF;
	keyTab[7] = WHILE;
	keyTab[8] = ARRAY;
	keyTab[9] = RECORD;
	keyTab[10] = CONST;
	keyTab[11] = TYPE;
	keyTab[12] = VAR;
	keyTab[13] = PROCEDURE;
	keyTab[14] = BEGIN;
	keyTab[15] = PROGRAM;

	// create an input file stream object
	std::ifstream f;
	f.open((argv[1])); // program takes one command line argument that is the name of the input file

	// if the file opened properly, then continuously read input characters until EOF is detected.
    if (f.is_open()) {
        while (f.get(ch)) {
        	GetChar();
        	GetSym(f);
        }
        sym = Symbols::EofSym;
        std::cout << "EofSym" << std::endl;
    } else { 
        std::cout << "input not opened!"; 
    }

    // close the file stream
    f.close();

	return 0;
}

