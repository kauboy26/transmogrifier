from core.constants import *
from core.lc3_consts import *

class LC3Converter():

    def __init__(self, instructions, labels, inv_labels, func_help):

        self.top_reg = False
        self.lc3_instructions = []
        self.stack_frame = [{}]

        self.instructions = instructions
        self.labels = labels
        self.inv_labels = inv_labels
        self.func_help = func_help

        self.table = {}
        self.table_print = []

        self.init_table()

    def convert(self):

        tree = []
        total_len = 0

        for n, i in enumerate(self.instructions):
            if n in self.inv_labels:
                lbl = self.inv_labels[n]
                table_index = self.table[lbl]
                self.table_print[table_index] = (lbl, total_len)

            block = self.convert_operation(i)
            total_len += len(block)
            tree.append((i, block))

        return tree, self.table_print

    def convert_operation(self, instruction):
        """
        Returns a list of lc3 operations for the given operation.
        """
        operands, operation = instruction

        if operation == SETUP_MAIN:
            return self.gen_setup_main(operands)
        elif operation == POP:
            return self.gen_pop(1)
        elif operation == HALT:
            return self.gen_halt()
        elif operation == CLEAN_MAIN:
            return self.gen_clean_main(operands)
        elif operation == EQUAL:
            return self.gen_assign(operands)
        elif operation == PLUS:
            return self.gen_plus(operands)
        elif operation == MINUS:
            return self.gen_minus(operands)
        elif operation == MULTI:
            return self.gen_mult(operands)
        elif operation == LTHAN:
            return self.gen_lthan(operands)
        elif operation == GTHAN:
            return self.gen_gthan(operands)
        elif operation == LTHANEQ:
            return self.gen_lthaneq(operands)
        elif operation == GTHANEQ:
            return self.gen_gthaneq(operands)
        elif operation == DOUBLE_EQ:
            return self.gen_doubeq(operands)
        elif operation == LOAD_CC:
            return self.gen_loadcc(operands)
        elif operation == COND_BRANCH:
            return self.gen_condbranch(operands)


    def gen_setup_main(self, operands):
        """
        Generates instructions to set up the frame pointer and stack pointer, the zero
        register and the TABLE register, and also makes
        space for the local variables in main.
        """

        instr = []
        # Set up SP and FP
        instr.append((LLD, (SP, STACK_LBL)))
        instr.append((LADDI, (FP, SP, -1)))
        
        # Set up the zero reg
        instr.append((LANDI, (ZERO, ZERO, 0)))

        # set up the TABLE reg
        instr.append((LLD, (TABLE, TABLE_LBL)))

        # Make space for local vars

        # Remember stack points downwards!
        i = 0
        for var in self.func_help[MAIN_FUNC]:
            self.stack_frame[-1][var] = i
            i -= 1
        
        instr = instr + self.smart_add(SP, SP, i)

        return instr

    def gen_clean_main(self, operands):
        instr = [ ( LADDI, (SP, FP, 1 )) ]
        return instr

    def gen_assign(self, operands):
        """
        Assigns the value to the variable. The variable is assumed to exist.
        Will eat things from the stack when necessary. This is meant
        for variables. Writes to memory locations are handled by mem_assign.
        """

        instr = []

        t1, op1 = operands[0]
        t0, var = operands[1]

        if t1 == STACK_TOP:
            # Eat from stack
            self.top_reg = False

            # The value is already in R0
            val_reg = OP0
            loc_reg = OP1

            # Find the location of the variable, and load into OP1
            instr += self.smart_add(loc_reg, FP, self.stack_frame[-1][var])

            # Store the value into location of variable
            instr += [( LSTR, ( val_reg, loc_reg, 0 )) ]

            return instr

        # Otherwise figure out the location of the variable
        loc_reg = OP0
        val_reg = OP1

        instr += self.smart_add(loc_reg, FP, self.stack_frame[-1][var])

        if t1 == ID:
            instr += self.read_var(val_reg, op1)
        elif t1 == NUMBER:
            instr += self.smart_set(val_reg, op1)

        

        # Now actually store the value
        instr += [( LSTR, ( val_reg, loc_reg, 0 )) ]

        return instr

    def gen_plus(self, operands):
        """
        Generates instructions to add two numbers
        """

        instr = []

        t0, op0 = operands[1]
        t1, op1 = operands[0]

        if t0 != STACK_TOP and t1 != STACK_TOP:
            if self.top_reg:
                instr += self.gen_single_push(ACCUM)
                self.top_reg = False
       

        if t0 == NUMBER and t1 == NUMBER:
            instr += self.smart_set(ACCUM, op0 + op1)
            self.top_reg = True
            return instr


        instr = self.fetch_two_operands(operands)

        instr += [ ( LADDR, (ACCUM, OP0, OP1 )) ]

        self.top_reg = True
        return instr

    def gen_minus(self, operands):
        """
        Generates instructions to subtract two numbers
        """

        instr = []

        t0, op0 = operands[1]
        t1, op1 = operands[0]

        if t0 != STACK_TOP and t1 != STACK_TOP:
            if self.top_reg:
                instr += self.gen_single_push(ACCUM)
                self.top_reg = False
        

        if t0 == NUMBER and t1 == NUMBER:
            instr += self.smart_set(ACCUM, op0 - op1)
            self.top_reg = True
            return instr

        instr = self.fetch_two_operands(operands, commutative=False)

        # Invert the second value
        instr += [ ( NOT, (OP1, OP1)) ]
        instr += [ (LADDI, (OP1, OP1, 1)) ]

        instr += [ ( LADDR, (ACCUM, OP0, OP1 )) ]

        self.top_reg = True
        return instr

    def gen_lthan(self, operands):
        return self.gen_gthan(operands[::-1])

    def gen_gthan(self, operands):
        # a > b
        # res = a - b
        # This will take care of pushing to stack.
        instr = self.gen_minus(operands)

        # if res <= 0 set ACCUM = 0
        instr += [ ( LBR, ( 'p', 1 )) ]
        instr += [ ( LADDI, ( ACCUM, ZERO, 0) ) ]

        return instr


    def gen_lthaneq(self, operands):
        return self.gen_gthaneq(oerands[::-1])


    def gen_gthaneq(self, operands):
        # a >= b
        # res = a - b
        instr = self.gen_minus(operands)

        # if res < 0 set ACCUM = 0
        instr += [ ( LBR, ( 'zp', 2 )) ]
        instr += [ ( LADDI, ( ACCUM, ZERO, 0) ) ]
        instr += [ ( LBR, ( 'nzp', 1) ) ]

        # else set ACCUM = 1
        instr += [ ( LADDI, (ACCUM, ZERO, 1)) ]

        return instr

    def gen_doubeq(self, operands):
        instr = self.gen_minus(operands)

        # res = a - b

        # if res == 0  then ACCUM = 1
        instr += [ ( LBR, ( 'np', 2) ) ]
        instr += [ ( LADDI, (ACCUM, ZERO, 1)) ]
        instr += [ (LBR, ('nzp', 1)) ]

        # else ACCUM = 0
        instr += [ ( LADDI, (ACCUM, ZERO, 0)) ]

        return instr


    def gen_mult(self, operands):
        """

        a, b

        a_isneg, b_isneg

        if a < 0 and b < 0:
            a = -a
            b = -b
            op0 = a
            op1 = b


        elif a < 0:
            op0 = a
            op1 = b
        elif b < 0:
            op0 = b
            op1 = a

        """

        instr = []
        # TODO optimize by looking at the smaller of the two operands
        # and then looping accordingly

        t0, op0 = operands[1]
        t1, op1 = operands[0]


        if t0 != STACK_TOP and t1 != STACK_TOP:
            if self.top_reg:
                instr += self.gen_single_push(ACCUM)
                self.top_reg = False


        if t0 == NUMBER and t1 == NUMBER:
            self.top_reg = True
            return self.smart_set(ACCUM, op0 * op1)


        instr = self.fetch_two_operands(operands)
        # At this point, would've loaded the two operands into OP0 and OP1
        # Pick on the second to be the counter variable

        # If it's negative, flip it first
        # The second was always loaded last

        # if OP1 < 0 then
            # OP1 = - OP1
            # OP0 = - OP0
        instr += [ ( LBR, ( 'zp', 4 ) ) ]
        instr += [ ( NOT, (OP1, OP1) )] 
        instr += [ ( LADDI, (OP1, OP1, 1) )]
        instr += [ ( NOT, (OP0, OP0) )] 
        instr += [ ( LADDI, (OP0, OP0, 1) )]


        # Now we have the counter ready, use TEMP to store mult result
        instr += [ ( LANDI, (TEMP, ZERO, 0)) ]

        # To reload CC with counter
        instr += [ ( LADDI, (OP1, OP1, 0)) ]
        instr += [ ( LBR, ('nz', 3) )]

        instr += [ ( LADDR, (TEMP, TEMP, OP0 ))]

        instr += [ ( LADDI, (OP1, OP1, -1))]
        instr += [ ( LBR, ('nzp', -5 ))]

        # put the result into accumulator
        instr += [ (LADDI, (ACCUM, TEMP, 0)) ]

        self.top_reg = True
        return instr


    def gen_divi(self, operands):
        return None

    def gen_modulo(self, operands):
        return None

    def gen_halt(self):
        return [ (LHALT, None) ]

    def gen_pop(self, num):
        """
        """
        if self.top_reg:
            self.top_reg = False
            num -= 1

        if num == 0:
            return []

        return self.smart_add(SP, SP, num)

    def gen_loadcc(self, operand):
        """
        If '$', don't do anything. It is guaranteed to have been
        the last thing put into a register.
        """
        return self.fetch_one_operand(operand)

    def gen_single_push(self, register):
        """
        Pushes the value in the register on to the stack (updates
        stack pointer as well)
        """
        instr =  [ ( LADDI, ( SP, SP, -1 )) ]
        instr += [ ( LSTR, ( register, SP, 0 ))]
        return instr


    def gen_condbranch(self, operands):
        """
        """
        lbl = operands

        rt_inst = self.read_table(ACCUM, lbl)

        instr = [ ( LBR, ( 'np', len(rt_inst) + 1) ) ]
        instr += rt_inst
        instr += [ ( LJMP, (ACCUM) )]

        return instr

    def smart_add(self, dest_reg, src_reg, number):
        """
        Adds a fixed amount to a number
        """
        return [(LADDI, (dest_reg, src_reg, number))]

    def smart_set(self, target_reg, value):
        """
        Puts a number into a register.
        """
        instr = []

        if -16 <= value <= 15:
            instr += [ ( LADDI, (target_reg, ZERO, value))]
            return instr

        # For now just let it loop, I'll write a better version later
        if value < -16:
            instr += [ ( LADDI, (target_reg, ZERO, -16))]
            value += 16
            while value < -16:
                instr += [ ( LADDI, (target_reg, target_reg, -16))]
                value += 16
            instr += [ ( LADDI, (target_reg, target_reg, value ))]
        else:
            instr += [ ( LADDI, (target_reg, ZERO, 15))]
            value -= 15
            while value > 15:
                instr += [ ( LADDI, (target_reg, target_reg, 15))]
                value -=15
            instr += [ ( LADDI, (target_reg, target_reg, value ))]

        return instr

    def fetch_one_operand(self, operand):
        """
        Puts the operand into R0. In case of a '$', does nothing.
        """
        t, op = operand

        if t == STACK_TOP:
            self.top_reg = False
            return []
        elif t == ID:
            return self.read_var(ACCUM, op)
        elif t == NUMBER:
            return self.smart_set(ACCUM, op)


    def fetch_two_operands(self, operands, commutative=True):
        """
        Puts the two operands into R0 and R1.
        If the commutative flag is True, then the first operand
        is put into R0 and the second operand into R1.

        Precondition: R0 is free to use
        """
        assert(not self.top_reg)

        instr = []

        if t0 == STACK_TOP and t1 == STACK_TOP:
            
            if commutative:
                instr += [ ( LADDI, (OP1, OP0, 0) ) ]
                instr += [ ( LLDR, ( OP0 ,SP, 0 ) ) ]
            else:
                instr += [ ( LLDR, ( OP1 ,SP, 0 ) ) ]

            instr += self.gen_pop(1)

        elif t0 == STACK_TOP or t1 == STACK_TOP:
            tt = t1 if t0 == STACK_TOP else t0
            op = op1 if t0 == STACK_TOP else op0

            if tt == NUMBER:
                instr += self.smart_set(OP1, opt)
            elif tt == ID:
                instr += self.read_var(OP1, opt)
        else:

            if t0 == ID:
                instr += self.read_var(OP0, op0)
            elif t0 == NUMBER:
                instr += self.smart_set(OP0, op0)

            if t1 == ID:
                instr += self.read_var(OP1, op1)
            elif t1 == NUMBER:
                instr += self.smart_set(OP1, op1)

        return instr


    def read_var(self, target_reg, var):
        """
        Reads a variable into the specified register.
        """

        dist_to_var = self.stack_frame[-1][var]

        instr = self.smart_add(target_reg, FP, dist_to_var)
        instr += [ ( LLDR, ( target_reg, target_reg, 0) )]

        return instr

    def read_table(self, target_reg, lbl):
        """
        Puts the value at that label into the target register
        """
        dist_to_entry = self.table[self.resolve_lbl(lbl)]
        instr = self.smart_add(target_reg, TABLE, dist_to_entry)
        instr += [ ( LLDR, ( target_reg, target_reg, 0) )]
        return instr

    def resolve_lbl(self, lbl):
        """
        Resolves multiple labels that point to the same thing.
        """
        return self.inv_labels[self.labels[lbl]]


    def init_table(self):
        """
        """
        self.table = {}
        self.table_print = []

        i = 0
        for lbl, ln in self.labels.items():
            rlbl = self.resolve_lbl(lbl)
            if rlbl not in self.table:
                self.table[rlbl] = i
                self.table_print.append((rlbl, 0))
                i += 1
