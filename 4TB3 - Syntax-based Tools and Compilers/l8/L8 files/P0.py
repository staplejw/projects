"""
Pascal0 Parser, Emil Sekerinski, February 2017,
Main program, type-checks, folds constants, calls scanner SC and code
generator CG, uses symbol table ST
"""

from sys import argv
import SC  #  used for SC.init, SC.sym, SC.val, SC.error
from SC import TIMES, DIV, MOD, AND, PLUS, MINUS, OR, EQ, NE, LT, GT, \
     LE, GE, PERIOD, COMMA, COLON, RPAREN, RBRAK, OF, THEN, DO, LPAREN, \
     LBRAK, NOT, BECOMES, NUMBER, IDENT, SEMICOLON, END, ELSE, IF, WHILE, \
     ARRAY, RECORD, CONST, TYPE, VAR, PROCEDURE, BEGIN, PROGRAM, EOF, \
     getSym, mark
import ST  #  used for ST.init
from ST import Var, Ref, Const, Type, Proc, StdProc, Int, Bool, Enum, \
     Record, Array, newObj, find, openScope, topScope, closeScope


# first and follow sets for recursive descent parsing

FIRSTFACTOR = {IDENT, NUMBER, LPAREN, NOT}
FOLLOWFACTOR = {TIMES, DIV, MOD, AND, OR, PLUS, MINUS, EQ, NE, LT, LE, GT, GE,
                COMMA, SEMICOLON, THEN, ELSE, RPAREN, RBRAK, DO, PERIOD, END}
FIRSTEXPRESSION = {PLUS, MINUS, IDENT, NUMBER, LPAREN, NOT}
FIRSTSTATEMENT = {IDENT, IF, WHILE, BEGIN}
FOLLOWSTATEMENT = {SEMICOLON, END, ELSE}
FIRSTTYPE = {IDENT, RECORD, ARRAY, LPAREN}
FOLLOWTYPE = {SEMICOLON}
FIRSTDECL = {CONST, TYPE, VAR, PROCEDURE}
FOLLOWDECL = {BEGIN}
FOLLOWPROCCALL = {SEMICOLON, END, ELSE}
STRONGSYMS = {CONST, TYPE, VAR, PROCEDURE, WHILE, IF, BEGIN, EOF}

from sys import stdout

def write(s): stdout.write(s)
def writeln(): stdout.write('\n')
indent = '  '

# parsing procedures

def selector(x):
    """
    Parses
        selector = {"." «write('.')» ident «write(ident)» | "[" «write('[')» expression "]" «write(']')»}.
    Assumes x is the entry for the identifier in front of the selector;
    generates code for the selector if no error is reported
    """
    while SC.sym in {PERIOD, LBRAK}:
        if SC.sym == PERIOD:  #  x.f
            write('.')
            getSym()
            if SC.sym == IDENT:
                write(SC.val)
                if type(x.tp) == Record:
                    for f in x.tp.fields:
                        if f.name == SC.val:
                            x = CG.genSelect(x, f); break
                    else: mark("not a field")
                    getSym()
                else: mark("not a record")
            else: mark("identifier expected")
        else:  #  x[y]
            write('[')
            getSym(); y = expression()
            if type(x.tp) == Array:
                if y.tp == Int:
                    if type(y) == Const and \
                       (y.val < x.tp.lower or y.val >= x.tp.lower + x.tp.length):
                        mark('index out of bounds')
                    else: x = CG.genIndex(x, y)
                else: mark('index not integer')
            else: mark('not an array')
            if SC.sym == RBRAK: write(']'); getSym(); 
            else: mark("] expected")
    return x

def factor():
    """
    Parses
        factor = ident «write(ident)» selector |
                 integer «write(integer)» |
                 "(" «write('(')» expression ")" «write(')')» |
                 "not" «write('not ') factor.
    Generates code for the factor if no error is reported
    """
    if SC.sym not in FIRSTFACTOR:
        mark("expression expected"); getSym()
        while SC.sym not in FIRSTFACTOR | STRONGSYMS | FOLLOWFACTOR:
            getSym()
    if SC.sym == IDENT:
        x = find(SC.val)
        if type(x) in {Var, Ref}: x = CG.genVar(x)
        elif type(x) == Const: x = Const(x.tp, x.val); x = CG.genConst(x)
        else: mark('expression expected')
        write(SC.val); getSym(); x = selector(x)
    elif SC.sym == NUMBER:
        x = Const(Int, SC.val); x = CG.genConst(x); write(str(SC.val)); getSym()
    elif SC.sym == LPAREN:
        write('('); getSym(); x = expression()
        if SC.sym == RPAREN: write(')'); getSym()
        else: mark(") expected")
    elif SC.sym == NOT:
        write('not '); getSym(); x = factor()
        if x.tp != Bool: mark('not boolean')
        elif type(x) == Const: x.val = 1 - x.val # constant folding
        else: x = CG.genUnaryOp(NOT, x)
    else: x = Const(None, 0)
    return x

def term():
    """
    Parses
        term = factor {("*" «write(' * ')» | "div" «write(' div ')» | "mod" «write(' mod ')» | "and" «write(' and ')») factor}.
    Generates code for the term if no error is reported
    """
    x = factor()
    while SC.sym in {TIMES, DIV, MOD, AND}:
        op = SC.sym; getSym();
        if op == AND and type(x) != Const: write(' and '); x = CG.genUnaryOp(AND, x)
        if op == TIMES: write(' * ')
        elif op == DIV: write(' div ')
        elif op == MOD: write(' mod ')
        y = factor() # x op y
        if x.tp == Int == y.tp and op in {TIMES, DIV, MOD}:
            if type(x) == Const == type(y): # constant folding
                if op == TIMES: x.val = x.val * y.val
                elif op == DIV: x.val = x.val // y.val
                elif op == MOD: x.val = x.val % y.val
            else: x = CG.genBinaryOp(op, x, y)
        elif x.tp == Bool == y.tp and op == AND:
            if type(x) == Const: # constant folding
                if x.val: x = y # if x is true, take y, else x
            else: x = CG.genBinaryOp(AND, x, y)
        else: mark('bad type')
    return x

def simpleExpression():
    """
    Parses
        simpleExpression = ["+" «write(' + ')» | "-" «write(' - ')»] term {("+" «write(' + ')» | "-" «write(' - ')» | "or" «write(' or ')») term}.
    Generates code for the simpleExpression if no error is reported
    """
    if SC.sym == PLUS:
        write(' + ') 
        getSym(); x = term()
    elif SC.sym == MINUS:
        write(' - ')
        getSym(); x = term()
        if x.tp != Int: mark('bad type')
        elif type(x) == Const: x.val = - x.val # constant folding
        else: x = CG.genUnaryOp(MINUS, x)
    else: x = term()
    while SC.sym in {PLUS, MINUS, OR}:
        op = SC.sym; getSym()
        if op == OR and type(x) != Const: write(' or '); x = CG.genUnaryOp(OR, x)
        if op == PLUS: write(' + ')
        if op == MINUS: write(' - ')
        y = term() # x op y
        if x.tp == Int == y.tp and op in {PLUS, MINUS}:
            if type(x) == Const == type(y): # constant folding
                if op == PLUS: x.val = x.val + y.val
                elif op == MINUS: x.val = x.val - y.val
            else: x = CG.genBinaryOp(op, x, y)
        elif x.tp == Bool == y.tp and op == OR:
            if type(x) == Const: # constant folding
                if not x.val: x = y # if x is false, take y, else x
            else: x = CG.genBinaryOp(OR, x, y)
        else: mark('bad type')
    return x

def expression():
    """
    Parses
        expression = simpleExpression
                     {("=" «write(' = ')» | "<>" «write(' <> ')» | "<" «write(' < ')» | "<=" «write(' <= ')» | ">" «write(' > ')» | ">=" «write(' >= ')») simpleExpression}.
    Generates code for the expression if no error is reported
    """
    x = simpleExpression()
    while SC.sym in {EQ, NE, LT, LE, GT, GE}:
        op = SC.sym
        if op == EQ: write(' = ')
        elif op == NE: write(' <> ')
        elif op == LT: write(' < ')
        elif op == LE: write(' <= ')
        elif op == GT: write(' > ')
        elif op == GE: write(' >= ')
        getSym(); y = simpleExpression() # x op y
        if x.tp == Int == y.tp:
            x = CG.genRelation(op, x, y)
        else: mark('bad type')
    return x

def compoundStatement(l):
    """
    Parses
        compoundStatement(l) =
            "begin" «writeln; write(l * indent + 'begin')»
            statement(l + 1) {";" «write(';')» statement(l + 1)}
            "end" «writeln; write(l * ident + 'end')»
    Generates code for the compoundStatement if no error is reported
    """
    if SC.sym == BEGIN: writeln(); write(l * indent + 'begin'); getSym()
    else: mark("'begin' expected")
    x = statement(l + 1)
    while SC.sym == SEMICOLON or SC.sym in FIRSTSTATEMENT:
        if SC.sym == SEMICOLON: write(';'); getSym()
        else: mark("; missing")
        y = statement(l + 1); x = CG.genSeq(x, y)
    if SC.sym == END: writeln(); write(l * indent + 'end'); getSym()
    else: mark("'end' expected")
    return x

def statement(l):
    """
    Parses
        statement =
            ident «write(writeln; l * indent + ident)» selector ":="  
                «write(' := ')» expression |
            ident «write(writeln; l * indent + ident)» "(" «write('(')» [expression
                {"," «write(', ')» expression}] ")" «write(')')» |
            compoundStatement(l) |
            "if" «writeln; write(l * indent + 'if ')» expression
                "then" «write(' then ')» statement(l + 1)
                ["else" «writeln; write(l * indent + 'else')» statement(l + 1)] |
            "while" «writeln; write(l * indent + 'while ')» expression "do" statement.
    Generates code for the statement if no error is reported
    """
    if SC.sym not in FIRSTSTATEMENT:
        mark("statement expected"); getSym()
        while SC.sym not in FIRSTSTATEMENT | STRONGSYMS | FOLLOWSTATEMENT:
            getSym()
    if SC.sym == IDENT:
        x = find(SC.val); writeln(); write(l * indent + SC.val); getSym()
        x = CG.genVar(x)
        if type(x) in {Var, Ref}:
            writeln()
            write(l * indent + SC.val)
            x = selector(x)
            if SC.sym == BECOMES:
                write(' := ')
                getSym(); y = expression()
                if x.tp == y.tp in {Bool, Int}: # and not SC.error: type(y) could be Type 
                    #if type(x) == Var: ### and type(y) in {Var, Const}: incomplete, y may be Reg
                        x = CG.genAssign(x, y)
                    #else: mark('illegal assignment')
                else: mark('incompatible assignment')
            elif SC.sym == EQ:
                mark(':= expected'); getSym(); y = expression()
            else: mark(':= expected')
        elif type(x) in {Proc, StdProc}:
            writeln()
            write(l * indent + SC.val)
            fp, i = x.par, 0  #  list of formals, count of actuals
            if SC.sym == LPAREN:
                write('('); getSym()
                if SC.sym in FIRSTEXPRESSION:
                    y = expression()
                    if i < len(fp):
                        if (type(fp[i]) == Var or type(y) == Var) and \
                           fp[i].tp == y.tp:
                            if type(x) == Proc: CG.genActualPara(y, fp[i], i)
                            i = i + 1
                        else: mark('illegal parameter mode')
                    else: mark('extra parameter')
                    while SC.sym == COMMA:
                        write(', '); getSym()
                        y = expression()
                        if i < len(fp):
                            if (type(fp[i]) == Var or type(y) == Var) and \
                               fp[i].tp == y.tp:
                                if type(x) == Proc: CG.genActualPara(y, fp[i], i)
                                i = i + 1
                            else: mark('illegal parameter mode')
                        else: mark('extra parameter')
                if SC.sym == RPAREN: write(')'); getSym()
                else: mark("')' expected")
            if i < len(fp): mark('too few parameters')
            if type(x) == StdProc:
                if x.name == 'read': x = CG.genRead(y)
                elif x.name == 'write': x = CG.genWrite(y)
                elif x.name == 'writeln': x = CG.genWriteln()
            else: x = CG.genCall(x)
        else: mark("variable or procedure expected")
    elif SC.sym == BEGIN: x = compoundStatement(l + 1)
    elif SC.sym == IF:
        writeln(); write(l * indent + 'if '); getSym(); x = expression();
        if x.tp == Bool: x = CG.genCond(x)
        else: mark('boolean expected')
        if SC.sym == THEN: write(' then '); getSym()
        else: mark("'then' expected")
        y = statement(l + 1)
        if SC.sym == ELSE:
            if x.tp == Bool: y = CG.genThen(x, y);
            writeln(); write(l * indent + 'else'); getSym()
            z = statement(l + 1);
            if x.tp == Bool: x = CG.genIfElse(x, y, z)
        else:
            if x.tp == Bool: x = CG.genIfThen(x, y)
    elif SC.sym == WHILE:
        getSym(); t = CG.genTarget(); x = expression()
        if x.tp == Bool: x = CG.genCond(x)
        else: mark('boolean expected')
        if SC.sym == DO: getSym()
        else: mark("'do' expected")
        y = statement(l + 1)
        if x.tp == Bool: x = CG.genWhile(t, x, y)
    else: x = None
    return x

def typ(l):
    """
    Parses
        type(l) = ident «write(ident)» |
               "array" «writeln; write((l + 1) * indent + 'array ')» "[" «write('[')» expression ".." «write(' .. ')» expression "]" «write(']')» "of" «write(' of ')» type(l)|
               "record" «writeln; write((l + 1) * indent + 'record')» typedIds(l) {";" «write(';')» typedIds(l)} "end" «writeln; write((l + 1) * indent + 'end')».
    Returns a type descriptor 
    """
    if SC.sym not in FIRSTTYPE:
        getSym(); mark("type expected")
        while SC.sym not in FIRSTTYPE | STRONGSYMS | FOLLOWTYPE:
            getSym()
    if SC.sym == IDENT:
        write(SC.val)
        ident = SC.val; x = find(ident); getSym()
        if type(x) == Type: x = Type(x.tp)
        else: mark('not a type'); x = Type(None)
    elif SC.sym == ARRAY:
        writeln()
        write((l + 1) * indent + 'array ')
        getSym()
        if SC.sym == LBRAK: write('['); getSym()
        else: mark("'[' expected")
        x = expression()
        if SC.sym == PERIOD: write(' .'); getSym()
        else: mark("'.' expected")
        if SC.sym == PERIOD: write('. '); getSym()
        else: mark("'.' expected")
        y = expression()
        if SC.sym == RBRAK: write(']'); getSym()
        else: mark("']' expected")
        if SC.sym == OF: write(' of '); getSym()
        else: mark("'of' expected")
        z = typ(l + 1).tp;
        if type(x) != Const or x.val < 0:
            mark('bad lower bound'); x = Type(None)
        elif type(y) != Const or y.val < x.val:
            mark('bad upper bound'); y = Type(None)
        else: x = Type(CG.genArray(Array(z, x.val, y.val - x.val + 1)))
    elif SC.sym == RECORD:
        writeln()
        write((l + 1) * indent + 'record ')
        writeln()
        write((l + 2) * indent)
        getSym(); openScope(); typedIds(Var, l + 2)
        while SC.sym == SEMICOLON:
            write(';')
            writeln()
            write((l + 2) * indent)
            getSym(); typedIds(Var, l + 2)
        if SC.sym == END: writeln(); write((l + 1) * indent + 'end'); getSym()
        else: mark("'end' expected")
        r = topScope(); closeScope()
        x = Type(CG.genRec(Record(r)))
    else: x = Type(None)
    return x

def typedIds(kind, l):
    """
    Parses
        typedIds(l) = ident «write(ident)» {"," «write(', ')» ident «write(ident)»} ":" «write(': ')» type(l).
    Updates current scope of symbol table
    Assumes kind is Var or Ref and applies it to all identifiers
    Reports an error if an identifier is already defined in the current scope
    """
    if SC.sym == IDENT: write(SC.val); tid = [SC.val]; getSym()
    else: mark("identifier expected"); tid = []
    while SC.sym == COMMA:
        write(', ')
        getSym()
        if SC.sym == IDENT: write(SC.val); tid.append(SC.val); getSym()
        else: mark('identifier expected')
    if SC.sym == COLON:
        write(': ')
        getSym(); tp = typ(l).tp
        if tp != None:
            for i in tid: newObj(i, kind(tp))
    else: mark("':' expected")

def declarations(allocVar, l):
    """
    Parses
        declarations(l) =
            {"const" «writeln; write(l * indent + 'const')» ident «writeln; write((l + 1) * indent + ident)» "=" «write(' = ')» expression ";" «write(';')»}
            {"type" «writeln; write(l * indent + 'type')» ident «writeln; write((l + 1) * indent + ident)» "=" «write(' = ')» type(l + 1) ";" «write(';')»}
            {"var" «writeln; write(l * indent + 'var')» «writeln; write((l + 1) * indent)» typedIds(l + 1) ";" «write(';')»}
            {"procedure" «writeln; write(l * indent + 'procedure ')» ident «write(ident)» ["(" «write('(')» [["var" «write('var ')»] typedIds(l) {";" «write('; ')» ["var" «write('var ')»] typedIds(l)}] ")" «write(')')»] ";" «write(";")»
                declarations(l + 1) compoundStatement(l + 1) ";"}.
    Updates current scope of symbol table.
    Reports an error if an identifier is already defined in the current scope.
    For each procedure, code is generated
    """
    if SC.sym not in FIRSTDECL | FOLLOWDECL:
        getSym(); mark("'begin' or declaration expected")
        while SC.sym not in FIRSTDECL | STRONGSYMS | FOLLOWDECL: getSym()
    while SC.sym == CONST:
        writeln()
        write(l * indent + 'const')
        getSym()
        if SC.sym == IDENT:
            writeln()
            write((l + 1) * indent + SC.val)
            ident = SC.val; getSym()
            if SC.sym == EQ: write(' = '); getSym()
            else: mark("= expected")
            x = expression()
            if type(x) == Const: newObj(ident, x)
            else: mark('expression not constant')
        else: mark("constant name expected")
        if SC.sym == SEMICOLON: write(';'); getSym()
        else: mark("; expected")
    while SC.sym == TYPE:
        writeln()
        write(l * indent + 'type')
        getSym()
        if SC.sym == IDENT:
            writeln()
            write((l + 1) * indent + ident)
            ident = SC.val; getSym()
            if SC.sym == EQ: write(' = '); getSym()
            else: mark("= expected")
            x = typ(l + 1); newObj(ident, x)  #  x is of type ST.Type
            if SC.sym == SEMICOLON: write(';'); getSym()
            else: mark("; expected")
        else: mark("type name expected")
    start = len(topScope())
    while SC.sym == VAR:
        writeln()
        write(l * indent + 'var')
        getSym()
        writeln()
        write((l + 1) * indent)
        typedIds(Var, l + 1)
        if SC.sym == SEMICOLON: write(';'); getSym()
        else: mark("; expected")
    varsize = allocVar(topScope(), start)
    while SC.sym == PROCEDURE:
        writeln()
        write(l * indent + 'procedure ')
        getSym()
        if SC.sym == IDENT: write(SC.val); getSym()
        else: mark("procedure name expected")
        ident = SC.val; newObj(ident, Proc([])) #  entered without parameters
        sc = topScope()
        CG.procStart(); openScope() # new scope for parameters and body
        if SC.sym == LPAREN:
            write('(')
            getSym()
            if SC.sym in {VAR, IDENT}:
                if SC.sym == VAR: write('var '); getSym(); typedIds(Ref, l)
                else: typedIds(Var, l)
                while SC.sym == SEMICOLON:
                    write('; ')
                    getSym()
                    if SC.sym == VAR: write('var '); getSym(); typedIds(Ref, l)
                    else: typedIds(Var, l)
            else: mark("formal parameters expected")
            fp = topScope()
            sc[-1].par = fp[:] #  procedure parameters updated
            if SC.sym == RPAREN: write(')'); getSym()
            else: mark(") expected")
        else: fp = []
        parsize = CG.genFormalParams(fp)
        if SC.sym == SEMICOLON: write(';'); getSym()
        else: mark("; expected")
        localsize = declarations(CG.genLocalVars, l + 1)
        CG.genProcEntry(ident, parsize, localsize)
        x = compoundStatement(l + 1); CG.genProcExit(x, parsize, localsize)
        closeScope() #  scope for parameters and body closed
        if SC.sym == SEMICOLON: write(';'); getSym()
        else: mark("; expected")
    return varsize

def program():
    """
    Parses
        program = "program" «write('program ')» ident «write(ident)»
            ";" «write(';')» declarations(1) compoundStatement(1).
    Generates code if no error is reported
    """
    newObj('boolean', Type(Bool)); Bool.size = 4
    newObj('integer', Type(Int)); Int.size = 4
    newObj('true', Const(Bool, 1))
    newObj('false', Const(Bool, 0))
    newObj('read', StdProc([Ref(Int)]))
    newObj('write', StdProc([Var(Int)]))
    newObj('writeln', StdProc([]))
    CG.progStart()
    if SC.sym == PROGRAM: write('program '); getSym()
    else: mark("'program' expected")
    ident = SC.val
    if SC.sym == IDENT: write(ident); getSym()
    else: mark('program name expected')
    if SC.sym == SEMICOLON: write(';'); getSym()
    else: mark('; expected')
    declarations(CG.genGlobalVars, 1); CG.progEntry(ident)
    x = compoundStatement(1)
    return CG.progExit(x)

def compileString(src, dstfn = None, target = 'mips'):
    """Compiles string src; if dstfn is provided, the code is written to that
    file, otherwise printed on the screen"""
    global CG
    #  used for init, genRec, genArray, progStart, genGlobalVars, \
    #  progEntry, progExit, procStart, genFormalParams, genActualPara, \
    #  genLocalVars, genProcEntry, genProcExit, genSelect, genIndex, \
    #  genVar, genConst, genUnaryOp, genBinaryOp, genRelation, genSeq, \
    #  genAssign, genCall, genRead, genWrite, genWriteln, genCond, \
    #  genIfThen, genThen, genIfElse, genTarget, genWhile
    if target == 'mips': import CGmips as CG
    elif target == 'ast': import CGast as CG
    elif target == 'pretty': import CGpretty as CG
    else: print('unknown target'); return
    SC.init(src)
    ST.init()
    CG.init()
    p = program()
    if p != None and not SC.error:
        if dstfn == None: print(p)
        else:
            with open(dstfn, 'w') as f: f.write(p);

def compileFile(srcfn):
    if srcfn.endswith('.p'):
        with open(srcfn, 'r') as f: src = f.read()
        dstfn = srcfn[:-2] + '.s'
        compileString(src, dstfn)
    else: print("'.p' file extension expected")

# sampe usage:
# import os
# os.chdir('/path/to/my/directory')
# compileFile('myprogram.p')
