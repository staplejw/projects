######################################################################
# Lab Question 1													 #
######################################################################

SC.py:

- TILDE, AMP, and BAR have been added to the enumerated symbols at the top of SC.py
- getSym() has been modified to recognize TILDE, AMP, and BAR and assigns these symbols to sym appropriately. 

P0.py:

- The productions of factor, term, and expression are modified appropriately:

factor = ident selector | integer | "(" expression ")" | "not" factor | "~" factor.

term = factor {("*" | "div" | "mod" | "and" | "&") factor}.

simpleExpression = ["+" | "-"] term {("+" | "-" | "or" | "|") term}.

- factor(), term(), and simlpeExpression() have been modified in P0.py to recognize and parse these new symbols. 

- TILDE has been added to first(factor) and first(exression), while AMP and BAR have been added to follow(factor). 

CGmips.py:

- genUnaryOp() has been mofified to generate code for TILDE. nor-ing an element with 0 is equivalent to inverting all of the bits. So, bitwise negation is implemented as a 'nor' operation between the given element and 0. 

- genBinaryOp() has been modified to generate for AMP and BAR. These are implemented using the 'and' and 'or' operations that already exist in the MIPS architecture. 

######################################################################
# Lab Question 2													 #
######################################################################

- To implement single line comments, I have added another 'elif' branch inside of getSym() in SC.py. The code will execute this branch if it discovers that the next character is '/'. Then, it grabs the next character again. If it finds another '/', then it enters the routine singleLineComment(). Otherwise, it marks an invalid character. 

- The singleLineComment() routine is meant to work exactly as comment() does. Once the double slash has been recognized, the routine eats through characters (by calling getChar()) until a newline character or EOF is detected. If the comment is terminated by a newline character, then regular parsing resumes. If it is termined by an EOF, then parsing is over and sym will get assigned EOF on the next call to getSym().