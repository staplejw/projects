import sys
import os
import fileinput

currentPosition = 0;
currentBlockPosition = 0;
args = ""

def main():

	#Clear the output file which the scanner symbols will be written to
	f = open('symbols.txt','w')
	f.write('')
	f.close()

	commentBlock = False;

	#scan input
	with open(sys.argv[1], "r") as word_list:
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
	
	print(words)

	try:
		getSym(words)
	except:
		print("Scanning Complete")
	

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

		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'EofSym')
		f.close()

		sys.stdout.write("EofSym\n");

		#First line is always blank - remove it
		with open('symbols.txt', 'r') as fin:
    			data = fin.read().splitlines(True)
		with open('symbols.txt', 'w') as fout:
    			fout.writelines(data[1:])

    		#start the parser, passing in the symbols
    		os.system('python rdparser.py symbols.txt')

		sys.exit()


def checkForReservedWords(sym, words):
	global currentPosition
	global currentBlockPosition
	global args

	currentBlockPosition = 0

	checkForNum(sym)

	sym = words[currentPosition]

	if sym == "not":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'NotSym')
		f.close()

		sys.stdout.write("NotSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "or":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'OrSym')
		f.close()
		
		sys.stdout.write("OrSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "and":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'AndSym')
		f.close()

		sys.stdout.write("AndSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "of":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'OrSym')
		f.close()

		sys.stdout.write("OfSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "then":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'ThenSym')
		f.close()

		sys.stdout.write("ThenSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "do":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'DoSym')
		f.close()

		sys.stdout.write("DoSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "not":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'NotSym')
		f.close()

		sys.stdout.write("NotSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "if":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'IfSym')
		f.close()

		sys.stdout.write("IfSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "exit":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'ExitSym')
		f.close()

		sys.stdout.write("ExitSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "else":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'ElseSym')
		f.close()

		sys.stdout.write("ElseSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "while":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'WhileSym')
		f.close()

		sys.stdout.write("WhileSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "{":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'LCurlSym')
		f.close()

		sys.stdout.write("LCurlSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "}":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'RCurlSym')
		f.close()

		sys.stdout.write("RCurlSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "public":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'PublicSym')
		f.close()

		sys.stdout.write("PublicSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "static":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'StaticSym')
		f.close()

		sys.stdout.write("StaticSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "void":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'VoidSym')
		f.close()

		sys.stdout.write("VoidSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "main":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'MainSym')
		f.close()

		sys.stdout.write("MainSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "[]":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'ArraySym')
		f.close()

		sys.stdout.write("ArraySym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "String":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'StringSym')
		f.close()

		sys.stdout.write("StringSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "args":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'ArgsSym')
		f.close()

		sys.stdout.write("ArgsSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "System":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'SystemSym')
		f.close()

		sys.stdout.write("SystemSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "out":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'OutSym')
		f.close()

		sys.stdout.write("OutSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "println":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'PrintSym')
		f.close()

		sys.stdout.write("PrintSym\n");
		currentPosition+=1;
		getSym(words)
	elif sym == "class":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'ClassSym')
		f.close()

		sys.stdout.write("ClassSym\n");
		currentPosition+=1;
		getSym(words)
	elif "*" in sym or "/" in sym or "%" in sym or "&" in sym or "+" in sym or "-" in sym or "&" in sym or "|" in sym or "." in sym or "," in sym or ":" in sym or "(" in sym or ")" in sym or "[" in sym or "]" in sym or ";" in sym:
		symList = list(words[currentPosition])
		checkForReservedSymbols(symList,words)
	else:
		#Append the symbol to the output file and the global linked list of print arguments
		args += sym
		f = open('symbols.txt','a')
		f.write('\n' + 'IdentSym')
		f.close()

		sys.stdout.write("IdentSym\n");
		currentPosition+=1;
		getSym(words)


def checkForReservedSymbols(symList,words):
	global currentPosition
	global currentBlockPosition

	if currentBlockPosition < len(symList):

		sym = symList[currentBlockPosition]

		if sym == "<" or sym == "=" or sym == ">" or sym == "!":
			checkRelationalOp(words)
		elif sym == None:
			sys.stdout.write("null\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "*":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'TimesSym')
			f.close()

			sys.stdout.write("TimesSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "/":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'DivSym')
			f.close()

			sys.stdout.write("DivSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "%":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'ModSym')
			f.close()

			sys.stdout.write("ModSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "&":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'AndSym')
			f.close()

			sys.stdout.write("AndSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "+":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'PlusSym')
			f.close()

			sys.stdout.write("PlusSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "-":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'MinusSym')
			f.close()

			sys.stdout.write("MinusSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "|":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'OrSym')
			f.close()

			sys.stdout.write("OrSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == ".":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'PeriodSym')
			f.close()

			sys.stdout.write("PeriodSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == ",":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'CommaSym')
			f.close()

			sys.stdout.write("CommaSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == ":":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'ColonSym')
			f.close()

			sys.stdout.write("ColonSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "(":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'LparenSym')
			f.close()

			sys.stdout.write("LparenSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == ")":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'RparenSym')
			f.close()

			sys.stdout.write("RparenSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "[":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'LbrakSym')
			f.close()

			sys.stdout.write("LbrakSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == "]":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'RbrakSym')
			f.close()

			sys.stdout.write("RbrakSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
		elif sym == ";":
			#Append the symbol to the output file
			f = open('symbols.txt','a')
			f.write('\n' + 'SemicolonSym')
			f.close()

			sys.stdout.write("SemicolonSym\n");
			currentBlockPosition+=1;
			checkForReservedSymbols(symList,words)
	else:
		currentPosition+=1
		getSym(words)
	

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
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'NeqSym')
		f.close()

		sys.stdout.write("NeqSym\n");
		currentBlockPosition+=2;
		checkForReservedSymbols(symList,words)
	elif sym == "<" and next == "=":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'LeqSym')
		f.close()

		sys.stdout.write("LeqSym\n");
		currentBlockPosition+=2;
		checkForReservedSymbols(symList,words)
	elif sym == ">" and next == "=":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'GeqSym')
		f.close()

		sys.stdout.write("GeqSym\n");
		currentBlockPosition+=2;
		checkForReservedSymbols(symList,words)
	elif sym == ">":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'GtrSym')
		f.close()

		sys.stdout.write("GtrSym\n");
		currentBlockPosition+=2;
		checkForReservedSymbols(symList,words)
	elif sym == "<" and next == "=":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'LssSym')
		f.close()

		sys.stdout.write("LssSym\n");
		currentBlockPosition+=2;
		checkForReservedSymbols(symList,words)
	elif sym == "=":
		#Append the symbol to the output file
		f = open('symbols.txt','a')
		f.write('\n' + 'EqlSym')
		f.close()

		sys.stdout.write("EqlSym\n");
		currentBlockPosition+=2;
		checkForReservedSymbols(symList,words)


if __name__ == "__main__": main()