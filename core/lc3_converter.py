from core.constants import *
from core.lc3_consts import *

class LC3Converter():

    def __init__(self, instructions, labels, inv_labels, func_help):

        self.topreg = False
        self.lc3_instructions = []
        self.stack_frame = [{}]

        self.instructions = instructions
        self.labels = labels
        self.inv_labels = inv_labels
        self.func_help = func_help

    def convert(self):

        tree = []
        for i in self.instructions:
            tree.append((i, self.convert_operation(i)))

        return tree

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
        instr = [ ( LADDI, (SP, FP, -1 )) ]
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

        if t0 == NUMBER and t1 == NUMBER:
            instr += self.smart_set(op0 * op1)
            return instr


        if t0 == STACK_TOP and t1 == STACK_TOP:
            # Fetch second value from stack top and pop
            instr += [ ( LLDR, ( OP1, SP, 0 ) ) ]
            instr += self.gen_pop(1)

            # add them together and store in accumulator
            instr += [ ( LADDR, (ACCUM, OP0, OP1) ) ]

            return instr



        if t0 == STACK_TOP or t1 == STACK_TOP:

            # Find out which isn't the stack top
            tt = t1 if t0 == STACK_TOP else t0
            opt = op1 if t0 == STACK_TOP else op0

            # Fetch the second value
            if tt == ID:
                instr += self.read_var(OP1, opt)
            elif tt == NUMBER:
                instr += self.smart_set(OP1, opt)

            # Add them together and put in accumulator
            instr += [ ( LADDR, ( ACCUM, OP0, OP1 ) ) ]

            return instr


        if t0 == ID:
            instr += self.read_var(OP0, op0)
        elif t0 == NUMBER:
            instr += self.smart_set(OP0, op0)

        if t1 == ID:
            instr += self.read_var(OP1, op1)
        elif t1 == NUMBER:
            instr += self.smart_set(OP1, op1)


        instr += [ ( LADDR, (ACCUM, OP0, OP1 )) ]

        return instr

    def gen_minus(self, operands):
        """
        Generates instructions to subtract two numbers
        """

        instr = []

        t0, op0 = operands[1]
        t1, op1 = operands[0]

        if t0 == NUMBER and t1 == NUMBER:
            instr += self.smart_set(op0 - op1)
            return instr


        if t0 == STACK_TOP and t1 == STACK_TOP:
            # Fetch second value from stack top and pop
            instr += [ ( LLDR, ( OP1, SP, 0 ) ) ]
            instr += self.gen_pop(1)

            # Invert the second value
            instr += [ ( NOT, (OP1, OP1)) ]
            instr += [ (LADDI, (OP1, OP1, 1)) ]

            # add them together and store in accumulator
            instr += [ ( LADDR, (ACCUM, OP0, OP1) ) ]

            return instr


        if t0 == STACK_TOP or t1 == STACK_TOP:

            # Find out which isn't the stack top
            tt = t1 if t0 == STACK_TOP else t0
            opt = op1 if t0 == STACK_TOP else op0

            # Fetch the second value
            if tt == ID:
                instr += self.read_var(OP1, opt)
            elif tt == NUMBER:
                instr += self.smart_set(OP1, number)

            # Invert the second value
            instr += [ ( NOT, (OP1, OP1)) ]
            instr += [ (LADDI, (OP1, OP1, 1)) ]

            # Add them together and put in accumulator
            instr += [ ( LADDR, ( ACCUM, OP0, OP1 ) ) ]

            return instr


        if t0 == ID:
            instr += self.read_var(OP0, op0)
        elif t0 == NUMBER:
            instr += self.smart_set(OP0, op0)

        if t1 == ID:
            instr += self.read_var(OP1, op1)
        elif t1 == NUMBER:
            instr += self.smart_set(OP1, op1)

        # Invert the second value
        instr += [ ( NOT, (OP1, OP1)) ]
        instr += [ (LADDI, (OP1, OP1, 1)) ]

        instr += [ ( LADDR, (ACCUM, OP0, OP1 )) ]

        return instr

    def gen_lthan(self, operands):
        return self.gen_gthan(operands[::-1])

    def gen_gthan(self, operands):
        # a > b
        # res = a - b
        instr = self.gen_minus(operands)

        # if res <= 0 set ACCUM = 0
        instr += [ ( LBR, ( 'p', 1 )) ]
        instr += [ ( LADDI, ( ACCUM, ZERO, 0) ) ]


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


    def gen_doubeq(self, operands):
        instr = self.gen_mins(operands)

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

        if t0 == NUMBER and t1 == NUMBER:
            return self.smart_set(ACCUM, op0 * op1)

        if t0 == STACK_TOP and t1 == STACK_TOP:
            # Fetch second value from stack top and pop
            instr += [ ( LLDR, ( OP1, SP, 0 ) ) ]
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


        # At this point, would've loaded the two operands into OP0 and OP1
        # Pick on the second to be the counter variable

        # If it's negative, flip it first
        # The second was always loaded last

        # if OP1 < 0 then OP1 = - OP1
        # instr += [ ( LBR, ( 'zp', 2 ) ) ]
        # instr += [ ( NOT, (OP1, OP1) )]
        # instr += [ ( LADDI, (OP1, OP1, 1) )]


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

        return instr


    def gen_divi(self, operands):
        return None

    def gen_modulo(self, operands):
        return None

    def gen_halt(self):
        return [ (LHALT, None) ]


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

        if value == 0:
            instr += [ ( LADDI, (target_reg, ZERO, 0))]
            return instr

        if value >= -16 and value < 15:
            instr += [ ( LADDI, (target_reg, ZERO, value))]
            return instr

        # Otherwise do smart thing

    def read_var(self, target_reg, var):
        """
        Reads a variable into the specified register.
        """

        dist_to_var = self.stack_frame[-1][var]

        instr = self.smart_add(target_reg, FP, dist_to_var)
        instr += [ ( LLDR, ( target_reg, target_reg, 0) )]

        return instr