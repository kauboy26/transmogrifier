LADDI = 'addi'
LANDI = 'andi'
LADDR = 'addr'
LANDR = 'andr'
LNOT = 'not'
LLDR = 'ldr'
LSTR = 'str'
LRET = 'ret'
LHALT = 'halt'
LJSRR = 'jsrr'
LJMP = 'jmp'
LBR = 'br'
LTRAP = 'trap'

LPUTS = 'puts'
LGETC = 'getc'
LOUT = 'out'


# shouldn't be used much
LLEA = 'lea'
LLDI = 'ldi'
LLD = 'ld'
LST = 'st'
LJSR = 'jsr'

# Pseudo ops
LFILL = '.fill'
LSTRINGZ = '.stringz'

####################################
# The different registers

R0 = 0
R1 = 1
R2 = 2
R3 = 3
R4 = 4
R5 = 5
R6 = 6
R7 = 7

ACCUM = R0
OP0 = R0
OP1 = R1
TEMP = R2

ZERO = R3
TABLE = R4 # should hold value of TABLE_TXT

FP = R5
SP = R6
LINK = R7

TABLE_LBL = 'TABLE'
STACK_LBL = 'STACK'

STACK = 0xF000

STACK_TXT = 'xF000'
TABLE_TXT = 'x6000'
STR_TABLE_TXT = 'x6800'