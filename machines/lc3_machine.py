"""
The LC3
"""
from core.lc3_consts import *
from random import randint, seed

def convert_nzp(nzp):
    cc = 0
    if 'n' in nzp:
        cc = cc | (1 << 2)
    if 'z' in nzp:
        cc = cc | (1 << 1)
    if 'p' in nzp:
        cc = cc | 1

    return cc

def value_to_cc(value):
    cc = 0

    if value < 0:
        cc = 1 << 2
    elif value == 0:
        cc = 1 << 1
    elif value > 0:
        cc = 1

    return cc

class LC3Machine():

    def __init__(self):

        self.orig = 0x3000
        self.memsize = 0xFFFF
        self.pc = 0
        self.is_running = False

        self.seed = randint(0, 10000)
        print('LC3 Seed:', self.seed)

        seed(self.seed)
        self.memory = [0 for i in range(0, self.memsize)]

        self.registers = [ 0 for i in range(0, 8)]

        self.labels = {}


    def run(self, instructions, table, labels):
        """
        """
        self.labels = {STACK_LBL: -1, TABLE_LBL: -2}
        self.memory[self.orig - 1] = 0xF000
        self.memory[self.orig - 2] = 0x2000

        self.write_table(table)

        self.pc = 0
        self.is_running = True

        

        instr_len = len(instructions)
        executed = 0

        while self.is_running:
            assert(0 <= self.pc < instr_len)

            instruction, operands = instructions[self.pc]
            self.pc += 1

            print(self.pc - 1, ':', instruction, operands, '........')
            self.perform_operation(instruction, operands)
            executed += 1
            self.print_regs()

        print('Executed', executed, 'instructions.')


    def write_table(self, table):
        """
        Writes the label table at x2000. Adds x3000 to all the entries.
        """
        i = 0x2000

        for lbl, val in table:
            self.memory[i] = val
            i += 1

    def print_memory(self, low, high):
        for i in range(low, high):
            print(format(i, '04x'), ':', '{:8}   : '.format(self.memory[i]), format(self.memory[i], '04x'))

    def print_regs(self):
        print('Printing regs...')
        for i in range(8):
            print('R{}'.format(i), ': {:8}'.format(self.registers[i]), '  :   ', format(self.registers[i], '04x'))

        print('CC :', self.CC)
        print('PC :', self.pc)

    def perform_operation(self, instruction, operands):
        if instruction == LADDI:
            self.addi(operands)
        elif instruction == LADDR:
            self.addr(operands)  
        elif instruction == LANDI:
            self.andi(operands)
        elif instruction == LANDR:
            self.andr(operands)
        elif instruction == LNOT:
            self.lnot(operands)
        elif instruction == LLDR:
            self.ldr(operands)
        elif instruction == LSTR:
            self.str(operands)
        elif instruction == LLD:
            self.ld(operands)
        elif instruction == LST:
            self.st(operands)
        elif instruction == LBR:
            self.br(operands)
        elif instruction == LJMP:
            self.jmp(operands)
        elif instruction == LHALT:
            self.halt()


    def addi(self, operands):
        dest, src, imm = operands
        assert(-16 <= imm <= 15)
        self.registers[dest] = self.registers[src] + imm

        self.CC = value_to_cc(self.registers[dest])

    def addr(self, operands):
        dest, sr1, sr2 = operands
        self.registers[dest] = self.registers[sr1] + self.registers[sr2]

        self.CC = value_to_cc(self.registers[dest])

    def andi(self, operands):
        dest, src, imm = operands
        assert(-16 <= imm <= 15)
        self.registers[dest] = self.registers[src] & imm

        self.CC = value_to_cc(self.registers[dest])

    def andr(self, operands):
        dest, sr1, sr2 = operands
        self.registers[dest] = self.registers[sr1] & self.registers[sr2]

        self.CC = value_to_cc(self.registers[dest])

    def lnot(self, operands):
        dest, src = operands
        self.registers[dest] = ~ self.registers[src]

        self.CC = value_to_cc(self.registers[dest])


    def ldr(self, operands):
        dest, base, offset = operands
        assert(-32 <= offset <= 31)
        self.registers[dest] = self.memory[self.registers[base] + offset]
        
        self.CC = value_to_cc(self.registers[dest])

    def str(self, operands):
        src, base, offset = operands
        assert(-32 <= offset <= 31)
        self.memory[self.registers[base] + offset] = self.registers[src] 


    def ld(self, operands):
        dest, lbl = operands
        offset = self.labels[lbl] - self.pc

        assert(-2**8 <= offset <= 2**8 - 1)
        self.registers[dest] = self.memory[self.pc + offset + self.orig]
        
        self.CC = value_to_cc(self.registers[dest])


    def st(self, operands):
        src, lbl = operands
        offset = self.labels[lbl] - self.pc

        assert(-2**8 <= offset <= 2**8 - 1)
        self.memory[self.pc + offset + self.orig] = self.registers[src]

    def ldi(self, operands):
        dest, lbl = operands
        offset = self.labels[lbl] - self.pc

        assert(-2**8 <= offset <= 2**8 - 1)
        self.registers[dest] = self.memory[self.memory[self.pc + offset + self.orig]]

    def sti(self, operands):
        src, lbl = operands
        offset = self.labels[lbl] - self.pc

        assert(-2**8 <= offset <= 2**8 - 1)
        self.memory[self.memory[self.pc + offset + orig]] = self.registers[src]


    def lea(self, operands):
        dest, lbl = operands
        offset = self.labels[lbl] - self.pc

        assert(-2**8 <= offset <= 2**8 - 1)
        self.registers[dest] = self.pc + offset + self.orig



    def br(self, operands):
        nzp, offset = operands
        assert(-2**8 <= offset <= 2**8 - 1)

        test_cc = convert_nzp(nzp)

        if test_cc & self.CC:
            # Condition met
            self.pc += offset

    def jsr(self, operands):
        lbl = operands
        offset = self.labels[lbl] - self.pc

        assert(-2**10 <= offset <= 2**10 - 1)
        self.registers[LINK] = self.pc
        self.pc += offset

    def jsrr(self, operands):
        base = operands
        self.registers[LINK] = self.pc
        self.pc = base


    def jmp(self, operands):
        base = operands
        self.pc = self.registers[base]


    def ret(self, operands):
        self.pc = self.registers[LINK]


    def halt(self):

        self.is_running = False

    def trap(self, operands):
        vector = operands
        self.pc = self.memory[vector]
