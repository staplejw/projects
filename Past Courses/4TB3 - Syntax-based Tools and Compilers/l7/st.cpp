/*
Title: st.cpp / st.h
Author: Justin Staples
Partner: Mahmoud Khattab
Date: March 5, 2018
Usage: g++ -o script st.cpp

A symbol table for the P0 (Pascal 0) language. 

*/

#include <iostream>
#include "st.h"

// SymbolTable::SymbolTable() {}

// getter method which returns the list of lists
list<list <Entry> > SymbolTable::get() {
	return this->st;
}

// add a new entry to the symbol table
void SymbolTable::NewObj(string n, Entry e) {
	// search the top scope to see if the name already exists, if it does throw an error and return
	list<Entry>::iterator it; 
	for (it = this->st.front().begin(); it != this->st.front().end(); it++) {
		if (n.compare(it->name) == 0) {
			cout << "ERROR: This name alreay exists in the current scope" << endl;
			return;
		}
	}
	// add the current level to the entry
	e.name = n;
	e.level = this->st.size() - 1;
	// add the new entry at the end of the top scope
	this->st.front().push_back(e);
}

// open a new scope and puts a HEAD entry at the front of the list
void SymbolTable::OpenScope() {
	Entry e = {HEAD};
	list<Entry> p;
	p.push_front(e);
	this->st.push_front(p);
}

// close a scope
void SymbolTable::CloseScope() {
	this->st.pop_front();
}

// get the list of entries in the top scope
list<Entry> SymbolTable::TopScope() {
	return this->st.front();
}

// try to find the name in the table and return its entry
// if a matching name cannot be found it return an empty entry
Entry SymbolTable::Find(string n) {
	list<list <Entry> >::iterator it1;
	for (it1 = this->st.begin(); it1 != this->st.end(); it1++) {
		list<Entry>::iterator it2;
		for (it2 = it1->begin(); it2 != it1->end(); it2++) {
			if (n.compare(it2->name) == 0) {
				return *it2;
			}
		}
	}
	Entry e;
	return e;
}

// main method for running test cases
int main() {

	// symbol table instance
	SymbolTable P0;
	// sample entries
	Entry e1, e2, e3;

	e1.cls = VAR;
	e1.tp = INTEGER;

	e2.cls = CONST;
	e2.tp = BOOL;
	e3.val = 0;

	e3.cls = PROC;
	e3.val = -1;

	// test that open scope creates a new empty list
	P0.OpenScope();
	if (P0.get().size() == 1) {
		cout << "open scope test passed" << endl;
	}
	// test open scope sets the first element to be the header
	if (P0.TopScope().front().cls == HEAD) {
		cout << "open scope test passed" << endl;
	}

	// test that close scope removes the most recent scope
	P0.CloseScope();
	if (P0.get().size() == 0) {
		cout << "close scope test passed" << endl;
	}

	// test that new object adds the object to the end of the scope
	P0.OpenScope();
	P0.NewObj("x", e1);
	if (P0.TopScope().size() == 2) {
		cout << "new obj test passed" << endl;
	}
	if (P0.TopScope().back().cls == VAR) {
		cout << "new obj test passed" << endl;
	}

	// this test should print an error message because the name already exists
	P0.NewObj("x", e2);

	// add another entry called "y"
	P0.NewObj("y", e3);

	// test that the name "x" is correctly found
	Entry test = P0.Find("x");
	if (test.cls == VAR) {
		cout << "find test passed" << endl;
	}
	if (test.tp == INTEGER) {
		cout << "find test passed" << endl;
	}

	return 0;
}