"""
This module helps with printing on to an ASM file.

For the x_t methods below, "o" stands for operation, "r" for register,
"i" for immediate, "c" for CC, "l" for label. 
"""

from core.lc3_consts import *

ORRR_T = {LADDR: 0, LANDR: 0}
ORRI_T = {LADDI: 0, LANDI: 0, LLDR: 0, LSTR: 0}

ORR_T = {LNOT: 0, }

O_T = {LRET: 0, LHALT: 0, LPUTS: 0, LGETC: 0, LOUT: 0}

OR_T = {LJSRR: 0, LJMP: 0}

OI_T = {LTRAP: 0}

OCI_T = {LBR: 0}

ORL_T = {LLD: 0, LST: 0, LLDI: 0, LLEA: 0}

OL_T = { LJSR: 0}

EXTRA = {LADDI: 'add', LADDR: 'add', LANDI: 'and', LANDR: 'and'}

def orrr_t(op, rs):
    r1, r2, r3 = rs
    return '\t{} R{}, R{}, R{}\n'.format(op, r1, r2, r3)

def orri_t(op, rs):
    r1, r2, imm = rs
    return '\t{} R{}, R{}, #{}\n'.format(op, r1, r2, imm)

def orr_t(op, rs):
    r1, r2 = rs
    return '\t{} R{}, R{}\n'.format(op, r1, r2)

def o_t(op, rs=None):
    return '\t{}\n'.format(op)

def or_t(op, r1):
    return '\t{} R{}\n'.format(op, r1)

def oci_t(op, rs):
    cc, imm = rs
    return '\t{}{} #{}\n'.format(op, cc, imm)

def ocl_t(op, rs):
    cc, lbl = rs
    return '\t{}{} {}\n'.format(op, cc, lbl)

def ol_t(op, lbl):
    return '\t{} {}\n'.format(op, lbl)

def orl_t(op, rs):
    r1, lbl = rs
    return '\t{} R{}, {}\n'.format(op, r1, lbl)

def oi_t(op, imm):
    return '\t{} {}\n'
  
def conv_instruction(instruction):
    op, rs = instruction
    if op in ORRR_T:
        if op in EXTRA:
            return orrr_t(EXTRA[op], rs)
        return orrr_t(op, rs)
    elif op in ORRI_T:
        if op in EXTRA:
            return orri_t(EXTRA[op], rs)
        return orri_t(op, rs)
    elif op in ORR_T:
        return orr_t(op, rs)
    elif op in OR_T:
        return or_t(op, rs)
    elif op in O_T:
        return o_t(op)
    elif op in OL_T:
        return ol_t(op, rs)
    elif op in ORL_T:
        return orl_t(op, rs)
    elif op in OCI_T:
        return oci_t(op, rs)
    elif op in OI_T:
        return oi_t(op, rs)


def gen_asm(tree, table, str_table=[]):

    output = ''

    i = 0
    j = 0

    output += '.orig {}\n;; JUMP TABLE:\n'.format(TABLE_TXT)
    
    for lbl, val in table:
        output += '\t.fill \tx{}\t; {}\n'.format(format(0x3003 + val, '04x'), lbl)

    output += ';; END OF JUMP TABLE\n.end\n'

    output += '\n\n.orig {}\n;; STR TABLE:\n'.format(STR_TABLE_TXT)

    for s in str_table:
        output += '\t.stringz \t"{}"\n'.format(repr(s)[1:-1])

    output += ';; END OF STR TABLE\n.end\n\n'

    output += '.orig x3000\n;; CODE:\n'
    output += '\n\tbrnzp #2 \t; The code effectively starts at x3003\n'
    output += '{}\t\t .fill \t{}\n'.format(STACK_LBL, STACK_TXT)
    output += '{}\t\t .fill \t{}\n'.format(TABLE_LBL, TABLE_TXT)

    output += '\n\n'

    i = 0
    j = 0

    for parent, generated in tree:
        
        output += ';; i: {}, j: {}, IR: {}\n'.format(i, j, str(parent))
        for instr in generated:
            output += '{} {}'.format(conv_instruction(instr)[0:-1],
                    '\t; {}\n'.format(j))
            j += 1
        i += 1

    output += '\n.end'

    return output