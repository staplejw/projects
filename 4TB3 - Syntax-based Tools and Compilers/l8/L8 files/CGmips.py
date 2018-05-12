"""
Pascal0 Code Generator for MIPS, Emil Sekerinski, February 2017.
Using delayed code generation for a one-pass compiler. The types of symbol
table entries for expressions, Var, Ref, Const, are extended by two more
types Reg for expression results in a register, and Cond, for short-circuited
Boolean expressions with two branch targets.

The generated code can be run in the SPIM simulator. To avoid confusion
between SPIM instructions and variables, all indentifer have _ as suffix.
The procedure calling convention is as follows:

Frame pointer $fp: last parameter at 0($fp), 2nd last at 4($fp), ...
    previous fp at -4($fp), return adr at -8($fp), 1st local at -12($fp)

Stack pointer $sp: points to last used location on stack

On procedure entry:
    caller pushes 1st parameter at -4($sp), 2nd at -8($sp), etc.
    caller calls callee
    callee saves $fp at S$spP - (parameter size + 4)
    callee saves $ra at $sp - (parameter size + 8)
    callee sets $fp to $sp - parameter size
    callee sets $sp to $fp - (local var size + 8)

On procedure exit:
    callee sets $sp to $fp + parameter size
    callee loads $ra from $fp - 8
    callee loads $fp from $fp - 4
    callee returns
"""

import SC  #  used for SC.error
from SC import TIMES, DIV, MOD, AND, PLUS, MINUS, OR, EQ, NE, LT, GT, LE, \
     GE, NOT, mark
from ST import Var, Ref, Const, Type, Proc, StdProc, Int, Bool

R0 = '$0'; FP = '$fp'; SP = '$sp'; LNK = '$ra'  # reserved registers

class Reg:
    """
    For integers or booleans stored in a register;
    register can be $0 for constants '0' and 'false'
    """
    def __init__(self, tp, reg):
        self.tp, self.reg = tp, reg

class Cond:
    """
    For a boolean resulting from comparing left and right by cond:
    left, right are either registers or constants, but one has to be a register;
    cond is one of 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE';
    labA, labB are lists of branch targets for when the result is true or false
    if right is $0, then cond 'EQ' and 'NE' can be used for branching depending
    on register left.
    """
    count = 0
    def __init__(self, cond, left, right):
        self.tp, self.cond, self.left, self.right = Bool, cond, left, right
        self.labA = ['C' + str(Cond.count)]; Cond.count += 1
        self.labB = ['C' + str(Cond.count)]; Cond.count += 1

# curlev is the current level of nesting of procedures
# regs is the set of available registers for expression evaluation
# asm is a list of triples; each triple consists of three strings
# - a label
# - an instruction, possibly with operands
# - a target (for branch and jump instructions)
# each of them can be the empty string

def obtainReg():
    if len(regs) == 0: mark('out of registers'); return R0
    else: return regs.pop()

def releaseReg(r):
    if r not in (R0, SP, FP, LNK): regs.add(r)

def putLab(lab, instr = ''):
    """Emit label lab with optional instruction; lab may be a single
    label or a list of labels"""
    if type(lab) == list:
        for l in lab[:-1]: asm.append((l, '', ''))
        asm.append((lab[-1], instr, ''))
    else: asm.append((lab, instr, ''))

def putInstr(instr, target = ''):
    """Emit an instruction"""
    asm.append(('', instr, target))

def put(op, a, b, c):
    """Emit instruction op with three operands, a, b, c"""
    putInstr(op + ' ' + a + ', ' + str(b) + ', ' + str(c))

def putB(op, a, b, c):
    putInstr(op + ' ' + a + ', ' + str(b), str(c))

def putM(op, a, b, c):
    """Emit load/store instruction at location or register b + offset c"""
    if b == R0: putInstr(op + ' ' + a + ', ' + str(c))
    else: putInstr(op + ' ' + a + ', ' + str(c) + '(' + b + ')')

def testRange(x):
    """Check if x is suitable for immediate addressing"""
    if x.val >= 0x8000 or x.val < -0x8000: mark('value too large')
    
def loadItemReg(x, r):
    """Assuming item x is Var, Const, or Reg, loads x into register r"""
    if type(x) == Var: 
        putM('lw', r, x.reg, x.adr); releaseReg(x.reg)
    elif type(x) == Const:
        testRange(x); put('addi', r, R0, x.val)
    elif type(x) == Reg: # move to register r
        put('add', r, x.reg, R0)
    else: assert False

def loadItem(x):
    """Assuming item x is Var or Const, loads x into a new register and
    returns a new Reg item"""
    if type(x) == Const and x.val == 0: r = R0 # use R0 for "0"
    else: r = obtainReg(); loadItemReg(x, r)
    return Reg(x.tp, r)

def loadBool(x):
    """Assuming x is Var or Const and x has type Bool, loads x into a
    new register and returns a new Cond item"""
    # improve by allowing c.left to be a constant
    if type(x) == Const and x.val == 0: r = R0 # use R0 for "false"
    else: r = obtainReg(); loadItemReg(x, r)
    c = Cond(NE, r, R0)
    return c

def putOp(cd, x, y):
    """For operation op with mnemonic cd, emit code for x op y, assuming
    x, y are Var, Const, Reg"""
    if type(x) != Reg: x = loadItem(x)
    if x.reg == R0: x.reg, r = obtainReg(), R0
    else: r = x.reg # r is source, x.reg is destination
    if type(y) == Const:
        testRange(y); put(cd, r, x.reg, y.val)
    else:
        if type(y) != Reg: y = loadItem(y)
        put(cd, x.reg, r, y.reg); releaseReg(y.reg)
    return x

def assembly(l, i, t):
    """Convert label l, instruction i, target t to assembly format"""
    return (l + ':\t' if l else '\t') + i + (', ' + t if t else '')

# public functions

def init():
    """initializes the code generator"""
    global asm, curlev, regs
    asm, curlev = [], 0
    regs = {'$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7', '$t8'}
                                
def genRec(r):
    """Assuming r is Record, determine fields offsets and the record size"""
    s = 0
    for f in r.fields:
        f.offset, s = s, s + f.tp.size
    r.size = s
    return r

def genArray(a):
    """Assuming r is Array, determine its size"""
    # adds size
    a.size = a.length * a.base.size
    return a

def genLocalVars(sc, start):
    """For list sc of local variables, starting at index start, determine the
    $fp-relative addresses of variables"""
    s = 0 # local block size
    for i in range(start, len(sc)):
        if type(sc[i]) == Var:
            s = s + sc[i].tp.size
            sc[i].adr = - s - 8
    return s

def genGlobalVars(sc, start):
    """For list sc of global variables, starting at index start, determine the
    address of each variable, which is its name with a trailing _"""
    for i in range(len(sc) - 1, start - 1, - 1):
        if type(sc[i]) == Var:
            sc[i].adr = sc[i].name + '_'
            putLab(sc[i].adr, '.space ' + str(sc[i].tp.size))

def progStart():
    putInstr('.data')

def progEntry(ident):
    putInstr('.text')
    putInstr('.globl main')
    putInstr('.ent main')
    putLab('main')

def progExit(x):
    putInstr('li $v0, 10')
    putInstr('syscall')
    putInstr('.end main')
    return '\n'.join(assembly(l, i, t) for (l, i, t) in asm)
        
def procStart():
    global curlev, parblocksize
    curlev = curlev + 1
    putInstr('.text')

def genFormalParams(sc):
    """For list sc with formal procedure parameters, determine the $fp-relative
    address of each parameters; each parameter must be type integer, boolean
    or must be a reference parameter"""
    s = 0 # parameter block size
    for p in reversed(sc):
        if p.tp == Int or p.tp == Bool or type(p) == Ref:
            p.adr, s = s, s + 4
        else: mark('no structured value parameters')
    return s

def genProcEntry(ident, parsize, localsize):
    """Declare procedure name, generate code for procedure entry"""
    putInstr('.globl ' + ident)        # global declaration directive
    putInstr('.ent ' + ident)          # entry point directive
    putLab(ident)                      # procedure entry label
    putM('sw', FP, SP, - parsize - 4)  # push frame pointer
    putM('sw', LNK, SP, - parsize - 8) # push return address
    put('sub', FP, SP, parsize)        # set frame pointer
    put('sub', SP, FP, localsize + 8)  # set stack pointer

def genProcExit(x, parsize, localsize): # generates return code
    global curlev
    curlev = curlev - 1
    put('add', SP, FP, parsize)
    putM('lw', LNK, FP, - 8)
    putM('lw', FP, FP, - 4)
    putInstr('jr $ra')

def genSelect(x, f):
    # x.f, assuming y is name in one of x.fields
    x.tp, x.adr = f.tp, x.adr + f.offset if type(x.adr) == int else \
                        x.adr + '+' + str(f.offset)
    return x

def genIndex(x, y):
    # x[y], assuming x is ST.Var or ST.Ref, x.tp is ST.Array, y.tp is ST.Int
    # assuming y is Const and y.val is valid index, or Reg integer
    if type(y) == Const:
        offset = (y.val - x.tp.lower) * x.tp.base.size
        x.adr = x.adr + (offset if type(x.adr) == int else '+' + str(offset))
    else:
        if type(y) != Reg: y = loadItem(y)
        put('sub', y.reg, y.reg, x.tp.lower)
        put('mul', y.reg, y.reg, x.tp.base.size)
        if x.reg != R0:
            put('add', y.reg, x.reg, y.reg); releaseReg(x.reg)
        x.reg = y.reg
    x.tp = x.tp.base
    return x

def genVar(x):
    # assuming x is ST.Var, ST.Ref, ST.Const
    # for ST.Const: no code, x.val is constant
    # for ST.Var: x.reg is FP for local, 0 for global vars,
    #   x.adr is relative or absolute address
    # for ST.Ref: address is loaded into register
    # returns ST.Var, ST.Const
    if type(x) == Const: y = x
    else:
        if x.lev == 0: s = R0
        elif x.lev == curlev: s = FP
        else: mark('level!'); s = R0
        y = Var(x.tp); y.lev = x.lev
        if type(x) == Ref: # reference is loaded into register
            r = obtainReg(); putM('lw', r, s, x.adr)
            y.reg, y.adr = r, 0
        elif type(x) == Var:
            y.reg, y.adr = s, x.adr
        else: y = x # error, pass dummy item
    return y

def genConst(x):
    # assumes x is ST.Const
    return x

def genUnaryOp(op, x):
    """If op is MINUS, NOT, x must be an Int, Bool, and op x is returned.
    If op is AND, OR, x is the first operand (in preparation for the second
    operand"""
    if op == MINUS: # subtract from 0
        if type(x) == Var: x = loadItem(x)
        put('sub', x.reg, 0, x.reg)
    elif op == NOT: # switch condition and branch targets, no code
        if type(x) != Cond: x = loadBool(x)
        x.cond = negate(x.cond); x.labA, x.labB = x.labB, x.labA
    elif op == AND: # load first operand into register and branch
        if type(x) != Cond: x = loadBool(x)
        putB(condOp(negate(x.cond)), x.left, x.right, x.labA[0])
        releaseReg(x.left); releaseReg(x.right); putLab(x.labB)
    elif op == OR: # load first operand into register and branch
        if type(x) != Cond: x = loadBool(x)
        putB(condOp(x.cond), x.left, x.right, x.labB[0])
        releaseReg(x.left); releaseReg(x.right); putLab(x.labA)
    else: assert False
    return x

def genBinaryOp(op, x, y):
    """assumes x.tp == Int == y.tp and op is TIMES, DIV, MOD
    or op is AND, OR"""
    if op == PLUS: y = putOp('add', x, y)
    elif op == MINUS: y = putOp('sub', x, y)
    elif op == TIMES: y = putOp('mul', x, y)
    elif op == DIV: y = putOp('div', x, y)
    elif op == MOD: y = putOp('mod', x, y)
    elif op == AND: # load second operand into register 
        if type(y) != Cond: y = loadBool(y)
        y.labA += x.labA # update branch targets
    elif op == OR: # load second operand into register
        if type(y) != Cond: y = loadBool(y)
        y.labB += x.labB # update branch targets
    else: assert False
    return y

def negate(cd):
    """Assume cd in {EQ, NE, LT, LE, GT, GE}, return not cd"""
    return NE if cd == EQ else \
           EQ if cd == NE else \
           GE if cd == LT else \
           GT if cd == LE else \
           LE if cd == GT else \
           LT

def condOp(cd):
    """Assumes cd in {EQ, NE, LT, LE, GT, GE}, return instruction mnemonic"""
    return 'beq' if cd == EQ else \
           'bne' if cd == NE else \
           'blt' if cd == LT else \
           'ble' if cd == LE else \
           'bgt' if cd == GT else \
           'bge'

def genRelation(cd, x, y):
    """Assumes x, y are Int and cd is EQ, NE, LT, LE, GT, GE;
    x and y cannot be both constants; return Cond for x cd y"""
    if type(x) != Reg: x = loadItem(x)
    if type(y) != Reg: y = loadItem(y)
    return Cond(cd, x.reg, y.reg)

assignCount = 0

def genAssign(x, y):
    """Assume x is Var, generate x := y"""
    global assignCount, regs
    if type(y) == Cond: # 
        putB(condOp(negate(y.cond)), y.left, y.right, y.labA[0])
        releaseReg(y.left); releaseReg(y.right); r = obtainReg()
        putLab(y.labB); put('addi', r, R0, 1) # load true
        lab = 'A' + str(assignCount); assignCount += 1
        putInstr('b', lab)
        putLab(y.labA); put('addi', r, R0, 0) # load false 
        putLab(lab)
    elif type(y) != Reg: y = loadItem(y); r = y.reg
    else: r = y.reg
    putM('sw', r, x.reg, x.adr); releaseReg(r)

def genActualPara(ap, fp, n):
    """Pass parameter, ap is actual parameter, fp is the formal parameter,
    either Ref or Var, n is the parameter number"""
    if type(fp) == Ref:  #  reference parameter, assume p is Var
        if ap.adr != 0:  #  load address in register
            r = obtainReg(); putM('la', r, ap.reg, ap.adr)
        else: r = ap.reg  #  address already in register
        putM('sw', r, SP, - 4 * (n + 1)); releaseReg(r)
    else:  #  value parameter
        if type(ap) != Cond:
            if type(ap) != Reg: ap = loadItem(ap)
            putM('sw', ap.reg, SP, - 4 * (n + 1)); releaseReg(ap.reg)
        else: mark('unsupported parameter type')

def genCall(pr):
    """Assume pr is Proc"""
    putInstr('jal', pr.name)

def genRead(x):
    """Assume x is Var"""
    putInstr('li $v0, 5'); putInstr('syscall')
    putM('sw', '$v0', x.reg, x.adr)

def genWrite(x):
    """Assumes x is Ref, Var, Reg"""
    loadItemReg(x, '$a0'); putInstr('li $v0, 1'); putInstr('syscall')

def genWriteln():
    putInstr('li $v0, 11'); putInstr("li $a0, '\\n'"); putInstr('syscall')

def genSeq(x, y):
    """Assume x and y are statements, generate x ; y"""
    pass

def genCond(x):
    """Assume x is Bool, generate code for branching on x"""
    if type(x) != Cond: x = loadBool(x)
    putB(condOp(negate(x.cond)), x.left, x.right, x.labA[0])
    releaseReg(x.left); releaseReg(x.right); putLab(x.labB)
    return x

def genIfThen(x, y):
    """Generate code for if-then: x is condition, y is then-statement"""
    putLab(x.labA)

ifCount = 0

def genThen(x, y):
    """Generate code for if-then-else: x is condition, y is then-statement"""
    global ifCount
    lab = 'I' + str(ifCount); ifCount += 1
    putInstr('b', lab)
    putLab(x.labA); 
    return lab

def genIfElse(x, y, z):
    """Generate code of if-then-else: x is condition, y is then-statement,
    z is else-statement"""
    putLab(y)

loopCount = 0

def genTarget():
    """Return target for loops with backward branches"""
    global loopCount
    lab = 'L' + str(loopCount); loopCount += 1
    putLab(lab)
    return lab

def genWhile(lab, x, y):
    """Generate code for while: lab is target, x is condition, y is body"""
    putInstr('b', lab)
    putLab(x.labA); 

