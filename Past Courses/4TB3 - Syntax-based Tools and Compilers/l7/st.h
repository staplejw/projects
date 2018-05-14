#include <list>
#include <string>
using namespace std;

// enumerated type for the different classes of symbol table entries
enum Classes {
	HEAD, VAR, PAR, CONST, FIELD, TYPE, PROC, SPROC
};

// enumerated type for the different types in the language
enum Type {
	INTEGER, BOOL, RECORD, ARRAY
};

// data type for symbol table entries. class, level, type and value.
struct Entry {
	Classes cls;
	Type tp;
	int val;
	string name;
	int level;
};

class SymbolTable {
	private:
		list<list <Entry> > st;

	public:
		SymbolTable() = default;
		list<list <Entry> > get();
		void NewObj(string n, Entry e);
		void OpenScope();
		void CloseScope();
		list<Entry> TopScope();
		Entry Find(string n);
};