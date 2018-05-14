import sys

currentPosition = 0;
currentBlockPosition = 0;

def main():

	commentBlock = False;

	#scan input
	with open(sys.argv[0], "r") as word_list:
		words = word_list.read().split()

	#Remove comments, tabs, spaces, and newlines
	for i in range(len(words)-1):

		#Check for and disregard comments
		if (i<len(words)-1):
			if words[i] == '/' and words [i+1] == '/' or words[i] == '/' and words [i+1] == '*':
				commentBlock = True
			if words[i] == '*' and words [i+1] == '/' or words[i] == '\n':
				commentBlock = False
		if commentBlock:
			words[i] = 'comment'

		#Remove whitespace
		if words[i] == ' ' or words[i] == '\t' or words[i] == '\n':
			del words[i]
		
	words = [i for i in words if i != 'comment']
	
	getSym(words)

#First check if the word is a number. Then check for reserved words, then reserved symbols. If those aren't possibilities, assume an identifier has been reached.
def getSym(words):

	if (currentPosition < len(words)):

		#Check for reserved words in Java.
		checkForReservedWords(words[currentPosition], words)
		symList = list(words[currentPosition])

		#If the entire word isn't reserved, check individual characters.
		checkForReservedSymbols(symList,words)
		currentBlockPosition = 0;
		getSym(words)

	#Once all symbols have been checked, start parsing the scanned symbols.
	else :
		sys.stdout.write("EofSym\n");
		sys.exit()


def checkForReservedWords(sym, words):
	global currentPosition
	global currentBlockPosition

	checkForNum(sym)

	if sym == "not":
		sys.stdout.write("NotSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "or":
		sys.stdout.write("OrSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "and":
		sys.stdout.write("AndSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "of":
		sys.stdout.write("OfSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "then":
		sys.stdout.write("ThenSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "do":
		sys.stdout.write("DoSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "not":
		sys.stdout.write("NotSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "if":
		sys.stdout.write("IfSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "procedure":
		sys.stdout.write("ProcedureSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "exit":
		sys.stdout.write("ExitSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "else":
		sys.stdout.write("ElseSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "while":
		sys.stdout.write("WhileSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "public":
		sys.stdout.write("PublicSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "StaticSym":
		sys.stdout.write("StaticSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "void":
		sys.stdout.write("VoidSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "main":
		sys.stdout.write("MainSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "[]":
		sys.stdout.write("ArraySym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "String":
		sys.stdout.write("StringSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "args":
		sys.stdout.write("ArgsSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "becomes":
		sys.stdout.write("BecomesSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "System":
		sys.stdout.write("SystemSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "out":
		sys.stdout.write("OutSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "println":
		sys.stdout.write("PrintSym\n");
		currentPosition+=1;
		getSym(words)
	elif "*" in sym or "/" in sym or "%" in sym or "&" in sym or "+" in sym or "-" in sym or "&" in sym or "|" in sym or "." in sym or "," in sym or ":" in sym or "(" in sym or ")" in sym or "[" in sym or "]" in sym or ";" in sym:
		symList = list(words[currentPosition])
		checkForReservedSymbols(symList,words)
	else:
		sys.stdout.write("IdentSym\n");
		currentPosition+=1;
		getSym(words)


def checkForReservedSymbols(symList,words):
	global currentPosition
	global currentBlockPosition

	sym = symList[currentBlockPosition]
	while currentBlockPosition < len(symList):
		if sym == "<" or sym == "=" or sym == ">" or sym == "!":
			checkRelationalOp(words)
		elif sym == None:
			sys.stdout.write("null\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "*":
			sys.stdout.write("TimesSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "/":
			sys.stdout.write("DivSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "%":
			sys.stdout.write("ModSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "&":
			sys.stdout.write("AndSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "+":
			sys.stdout.write("PlusSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "-":
			sys.stdout.write("MinusSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "&":
			sys.stdout.write("AndSym\n");
			urrentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "|":
			sys.stdout.write("OrSym\n");
			urrentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == ".":
			sys.stdout.write("PeriodSym\n");
			urrentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == ",":
			sys.stdout.write("CommaSym\n");
			urrentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == ":":
			sys.stdout.write("ColonSym\n");
			urrentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "(":
			sys.stdout.write("RparenSym\n");
			urrentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == ")":
			sys.stdout.write("LparenSym\n");
			urrentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "[":
			sys.stdout.write("LbrakSym\n");
			urrentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "]":
			sys.stdout.write("RbrakSym\n");
			urrentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == ";":
			sys.stdout.write("SemicolonSym\n");
			urrentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
	

def checkForNum(sym):

	if type(sym) == int:
		sys.stdout.write("NumberSym\n");
		currentPosition+=1;


def checkRelationalOp(words):
	global currentPosition
	global currentBlockPosition

	sym = list(words[currentPosition])
	next = list(words[currentPosition])

	if sym == "!" and next == "=":
		sys.stdout.write("NeqSym\n");
		currentBlockPosition+=2;
		checkForReservedSymbols(symList,words)
	elif sym == "<" and next == "=":
		sys.stdout.write("LeqSym\n");
		currentBlockPosition+=2;
		checkForReservedSymbols(symList,words)
	elif sym == ">" and next == "=":
		sys.stdout.write("GeqSym\n");
		currentBlockPosition+=2;
		checkForReservedSymbols(symList,words)
	elif sym == ">":
		sys.stdout.write("GtrSym\n");
		currentBlockPosition+=2;
		checkForReservedSymbols(symList,words)
	elif sym == "<" and next == "=":
		sys.stdout.write("LssSym\n");
		currentBlockPosition+=2;
		checkForReservedSymbols(symList,words)
	elif sym == "=":
		sys.stdout.write("EqlSym\n");
		currentBlockPosition+=2;
		checkForReservedSymbols(symList,words)


if __name__ == "__main__": main()