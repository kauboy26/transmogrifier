"""
Checklist:

At the end of all operations, top_reg is set to True. At the
beginning of all operations, top_reg is checked, and things are
pushed down on to the stack if needed, etc.

"instr = " vs "instr += " bug in some places

"""


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
        elif operation == UNARY_MINUS:
            return self.gen_unary_minus(operands)
        elif operation == PLUS:
            return self.gen_plus(operands)
        elif operation == MINUS:
            return self.gen_minus(operands)
        elif operation == MULTI:
            return self.gen_mult(operands)
        elif operation == DIVIS:
            return self.gen_divi(operands)
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
        elif operation == AND:
            return self.gen_and(operands)
        elif operation == OR:
            return self.gen_or(operands)
        elif operation == NOT:
            return self.gen_not(operands)
        elif operation == B_AND:
            return self.gen_b_and(operands)
        elif operation == B_OR:
            return self.gen_b_or(operands)
        elif operation == B_NOT:
            return self.gen_b_not(operands)
        elif operation == LOAD_CC:
            return self.gen_loadcc(operands)
        elif operation == COND_BRANCH:
            return self.gen_condbranch(operands)
        elif operation == BRANCH:
            return self.gen_uncond_branch(operands)


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

        if t0 != STACK_TOP and t1 != STACK_TOP\
            and self.top_reg:

            instr += self.gen_single_push(ACCUM)
            self.top_reg = False
       

        if t0 == NUMBER and t1 == NUMBER:
            instr += self.smart_set(ACCUM, op0 + op1)
            self.top_reg = True
            return instr


        instr += self.fetch_two_operands(operands)

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

        instr += self.fetch_two_operands(operands, commutative=False)

        # Invert the second value
        instr += [ ( LNOT, (OP1, OP1)) ]
        instr += [ (LADDI, (OP1, OP1, 1)) ]

        instr += [ ( LADDR, (ACCUM, OP0, OP1 )) ]

        self.top_reg = True
        return instr

    def gen_lthan(self, operands):
        return self.gen_gthan(operands[::-1])

    def gen_gthan(self, operands):
        # a > b
        # R0 = a - b
        # This will take care of pushing to stack.
        instr = self.gen_minus(operands)

        # if R0 <= 0 set ACCUM = 0
        instr += [ ( LBR, ( 'p', 1 )) ]
        instr += [ ( LADDI, ( ACCUM, ZERO, 0) ) ]

        return instr


    def gen_lthaneq(self, operands):
        return self.gen_gthaneq(operands[::-1])


    def gen_gthaneq(self, operands):
        # a >= b
        # R0 = a - b
        instr = self.gen_minus(operands)

        # if R0 < 0 set ACCUM = 0
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

        Using b as the counter,

        if b <0:
            b = -b
            a = -a

        res = 0

        while b:
            res += a
            b--

        return res

        """

        instr = []
        # TODO optimize by looking at the smaller of the two operands
        # and then looping accordingly

        t0, op0 = operands[1]
        t1, op1 = operands[0]

        if t0 != STACK_TOP and t1 != STACK_TOP and self.top_reg:
            instr += self.gen_single_push(ACCUM)
            self.top_reg = False


        if t0 == NUMBER and t1 == NUMBER:
            instr += self.smart_set(ACCUM, op0 * op1)
            self.top_reg = True
            return instr


        instr += self.fetch_two_operands(operands)
        # At this point, would've loaded the two operands into OP0 and OP1
        # Pick on the second to be the counter variable

        # If it's negative, flip it first

        # if OP1 < 0 then
            # OP1 = - OP1
            # OP0 = - OP0
        instr += [ ( LADDI, (OP1, OP1, 0) )] # reload cc
        instr += [ ( LBR, ( 'zp', 4 ) ) ]
        instr += [ ( LNOT, (OP1, OP1) )] 
        instr += [ ( LADDI, (OP1, OP1, 1) )]
        instr += [ ( LNOT, (OP0, OP0) )] 
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

    def gen_unary_minus(self, operands):
        """
        a
        
        return -a
        """

        t, op = operands[0]
        instr = []

        if t != STACK_TOP and self.top_reg:
            instr += self.gen_single_push(ACCUM)
            self.top_reg = False

        if t == NUMBER:
            instr += self.smart_set(ACCUM, -op)
            self.top_reg = True
            return instr

        instr += self.fetch_one_operand(operands[0])
        instr += [ ( LNOT, (OP0, OP0) )]
        instr += [ ( LADDI, ( OP0, OP0, 1) ) ]

        self.top_reg = True
        return instr


    def gen_divi(self, operands):
        """
        a, b

        if b == 0:
            return a

        if b < 0:
            if a < 0:
                b = -b
                a = -a
            else:
                goto neg_loop
        elif a < 0:
            goto neg_loop

        main_div_loop:
            res = a / b
            goto end

        neg_loop:
            if b > 0:
                b = -b
                a = -a
            res = - (abs(a / b))
            goto end

        end:
            return res

        """

        instr = []

        t0, op0 = operands[1]
        t1, op1 = operands[0]

        if t0 != STACK_TOP and t1 != STACK_TOP and self.top_reg:
            instr += self.gen_single_push(ACCUM)
            self.top_reg = False


        if t0 == NUMBER and t1 == NUMBER:
            instr += self.smart_set(ACCUM, int(op0 // op1))
            self.top_reg = True
            return instr


        instr += self.fetch_two_operands(operands, commutative=False)

        # First ensure the second operand isn't zero
        instr += [ ( LADDI, (OP1, OP1, 0 ))]
        instr += [ ( LBR, ('z', 34) )] # if check fails jump to end

        # Now check whether both are positive
        instr += [ ( LBR, ('n', 3))] # if b is negative, attempt to FLIP a
        
        instr += [ ( LADDI, (OP0, OP0, 0) )]
        instr += [ ( LBR, ('n', 17))] # go to neg_loop, since b > 0 and a < 0

        # a > 0 and b > 0
        instr += [ (LBR, ('nzp', 6))] # jump to main division loop

        # FLIP: (executed when b < 0)
        instr += [ ( LADDI, (OP0, OP0, 0) )]
        instr += [ ( LBR, ('zp', 14))] # if a >= 0, then execute neg_loop

        # since b < 0 and a < 0, flip both of them
        instr += [ ( LNOT, (OP0, OP0))]
        instr += [ ( LADDI, (OP0, OP0, 1) )]
        instr += [ ( LNOT, (OP1, OP1))]
        instr += [ ( LADDI, (OP1, OP1, 1) )]

        # MAIN DIVISION LOOP (not neg_loop):
        # a >= 0 and b > 0
        instr += [ ( LADDI, (TEMP, ZERO, 0 ))] # TEMP = result
        
        instr += [ ( LNOT, (OP1, OP1))]
        instr += [ ( LADDI, (OP1, OP1, 1))] # b = -b

        instr += [ ( LADDI, (OP0, OP0, 0) )] # while a >= 0:
        instr += [ ( LBR, ( 'n', 3 ))]

        instr += [ ( LADDR, (OP0, OP0, OP1 ))] # a = a + (-b)
        instr += [ ( LADDI, (TEMP, TEMP, 1 ))] # res++

        instr += [ ( LBR, ( 'nzp', -5 ))]

        # res will be one more than what it should be
        instr += [ ( LADDI, (ACCUM, TEMP, -1)) ]
        instr += [ ( LBR, ( 'nzp', 14 ))]


        # neg_loop (executed when a < 0 XOR b < 0):
        # make b the negative one
        instr += [ ( LADDI, (OP1, OP1, 0 ) )]
        instr += [ ( LBR, ( 'n', 4) )] # if b < 0, jump to neg_div_loop
        instr += [ ( LNOT, (OP0, OP0))]
        instr += [ ( LADDI, (OP0, OP0, 1) )]
        instr += [ ( LNOT, (OP1, OP1))]
        instr += [ ( LADDI, (OP1, OP1, 1) )]

        instr += [ ( LADDI, (TEMP, ZERO, 0 ))] # TEMP = result

        # neg_div_loop (here a > 0, b < 0):
        instr += [ ( LADDI, (OP0, OP0, 0) )]
        instr += [ ( LBR, ( 'n', 3 ))]

        instr += [ ( LADDR, (OP0, OP0, OP1 ))] # a = a + (-b)
        instr += [ ( LADDI, (TEMP, TEMP, 1 ))] # res++

        instr += [ ( LBR, ( 'nzp', -5 ))]

        # res will be one more than it should be, and opposite sign
        instr += [ ( NOT, (TEMP, TEMP) )]
        instr += [ ( LADDI, (ACCUM, TEMP, 1)) ]
        
        # END

        self.top_reg = True
        return instr

    def gen_modulo(self, operands):
        """
        a, b

        if b == 0:
            return a

        in all other cases, this is guaranteed:
        0 <= res <= abs(b)

        """

        instr = []

        t0, op0 = operands[1]
        t1, op1 = operands[0]

        if t0 != STACK_TOP and t1 != STACK_TOP and self.top_reg:
            instr += self.gen_single_push(ACCUM)
            self.top_reg = False


        if t0 == NUMBER and t1 == NUMBER:
            instr += self.smart_set(ACCUM, int(op0 // op1))
            self.top_reg = True
            return instr


        instr += self.fetch_two_operands(operands)

        # First ensure the second operand isn't zero
        instr += [ ( LADDI, (OP1, OP1, 0 ))]
        instr += [ ( LBR, ('z', 33) )] # if check fails jump to end

        # Now check whether both are positive
        instr += [ ( LBR, ('n', 3))] # if b is negative, attempt to FLIP a
        
        instr += [ ( LADDI, (OP0, OP0, 0) )]
        instr += [ ( LBR, ('n', 17))] # go to neg_loop, since b > 0 and a < 0

        # a > 0 and b > 0
        instr += [ (LBR, ('nzp', 6))] # jump to main division loop

        # FLIP: (executed when b < 0)
        instr += [ ( LADDI, (OP0, OP0, 0) )]
        instr += [ ( LBR, ('zp', 14))] # if a >= 0, then execute neg_loop

        # since b < 0 and a < 0, flip both of them
        instr += [ ( LNOT, (OP0, OP0))]
        instr += [ ( LADDI, (OP0, OP0, 1) )]
        instr += [ ( LNOT, (OP1, OP1))]
        instr += [ ( LADDI, (OP1, OP1, 1) )]

        # MAIN DIVISION LOOP (not neg_loop):
        # a >= 0 and b > 0
        
        instr += [ ( LNOT, (OP1, OP1))]
        instr += [ ( LADDI, (OP1, OP1, 1))] # b = -b

        instr += [ ( LADDI, (OP0, OP0, 0) )] # while a >= 0:
        instr += [ ( LBR, ( 'n', 3 ))]

        instr += [ ( LADDR, (OP0, OP0, OP1 ))] # a = a + (-b)

        instr += [ ( LBR, ( 'nzp', -5 ))]

        instr += [ ( LNOT, (OP1, OP1) )]
        instr += [ ( LADDI, (OP1, OP1, 1) )]
        instr += [ ( LADDR, (ACCUM, OP0, OP1)) ]

        instr += [ ( LBR, ( 'nzp', 13 ))]


        # neg_loop (executed when a < 0 XOR b < 0):
        # make b the negative one
        instr += [ ( LADDI, (OP1, OP1, 0 ) )]
        instr += [ ( LBR, ( 'n', 4) )] # if b < 0, jump to neg_div_loop
        instr += [ ( LNOT, (OP0, OP0))]
        instr += [ ( LADDI, (OP0, OP0, 1) )]
        instr += [ ( LNOT, (OP1, OP1))]
        instr += [ ( LADDI, (OP1, OP1, 1) )]

        # neg_div_loop (here a > 0, b < 0):
        instr += [ ( LADDI, (OP0, OP0, 0) )]
        instr += [ ( LBR, ( 'n', 3 ))]

        instr += [ ( LADDR, (OP0, OP0, OP1 ))] # a = a + (-b)

        instr += [ ( LBR, ( 'nzp', -5 ))]

        # res will be one more than it should be, and opposite sign
        instr += [ ( NOT, (OP0, OP0) )]
        instr += [ ( LADDI, (ACCUM, OP0, 1)) ]
        
        # END

        self.top_reg = True
        return instr

    def gen_and(self, operands):
        """
        a, b

        if a:
            return b
        else:
            return a (which is 0)

        """

        instr = []

        t0, op0 = operands[1]
        t1, op1 = operands[0]

        if t0 != STACK_TOP and t1 != STACK_TOP and self.top_reg:
            instr += self.gen_single_push(ACCUM)
            self.top_reg = False


        if t0 == NUMBER and t1 == NUMBER:
            instr += self.smart_set(ACCUM, int(op0 and op1))
            self.top_reg = True
            return instr

        instr += self.fetch_two_operands(operands)

        instr += [ ( LADDI, (OP0, OP0, 0) )]
        instr += [ ( LBR, ('z', 1) )]

        instr += [ ( LADDI, ( OP0, OP1, 0 )) ]

        self.top_reg = True
        return instr


    def gen_or(self, operands):
        """
        a, b

        if a == 0:
            return b
        else:
            return a (non zero)
        """

        instr = []

        t0, op0 = operands[1]
        t1, op1 = operands[0]

        if t0 != STACK_TOP and t1 != STACK_TOP and self.top_reg:
            instr += self.gen_single_push(ACCUM)
            self.top_reg = False


        if t0 == NUMBER and t1 == NUMBER:
            instr += self.smart_set(ACCUM, int(op0 or op1))
            self.top_reg = True
            return instr

        instr += self.fetch_two_operands(operands)

        instr += [ ( LADDI, (OP0, OP0, 0) )]
        instr += [ ( LBR, ('np', 1) )]

        instr += [ ( LADDI, ( OP0, OP1, 0 )) ]

        self.top_reg = True
        return instr


    def gen_not(self, operands):
        """
        a
        if a:
            return 0
        else:
            return 1
        """

        t, op = operands[0]
        instr = []

        if t != STACK_TOP and self.top_reg:
            instr += self.gen_single_push(ACCUM)
            self.top_reg = False

        if t == NUMBER:
            instr += [ ( LADDI, (OP0, ZERO, int(not op) ))]
            self.top_reg = True
            return instr

        instr += self.fetch_one_operand(operands[0])

        instr += [ ( LADDI, (OP0, OP0, 0) )] # reload CC
        instr += [ ( LBR, ('z', 2 ) )]
        instr += [ ( LADDI, (OP0, ZERO, 0) )]
        instr += [ ( LBR, ('nzp', 1 ) )]
        instr += [ ( LADDI, (OP0, ZERO, 1) )]

        self.top_reg = True
        return instr


    def gen_b_and(self, operands):
        """
        a, b

        return a & b
        """

        instr = []

        t0, op0 = operands[1]
        t1, op1 = operands[0]

        if t0 != STACK_TOP and t1 != STACK_TOP and self.top_reg:
            instr += self.gen_single_push(ACCUM)
            self.top_reg = False


        if t0 == NUMBER and t1 == NUMBER:
            instr += self.smart_set(ACCUM, int(op0 & op1))
            self.top_reg = True
            return instr

        instr += self.fetch_two_operands(operands)
        instr += [ ( LANDR, (OP0, OP0, OP1 ))]

        self.top_reg = True
        return instr

    def gen_b_or(self, operands):
        """
        a, b

        return a | b

        This method uses de Morgan's law. So really, it does
            ~(~a & ~b).
        """

        instr = []

        t0, op0 = operands[1]
        t1, op1 = operands[0]

        if t0 != STACK_TOP and t1 != STACK_TOP and self.top_reg:
            instr += self.gen_single_push(ACCUM)
            self.top_reg = False


        if t0 == NUMBER and t1 == NUMBER:
            instr += self.smart_set(ACCUM, int(op0 | op1))
            self.top_reg = True
            return instr

        instr += self.fetch_two_operands(operands)

        instr += [ ( LNOT, (OP0, OP0 ))]
        instr += [ ( LNOT, (OP1, OP1 ))]
        instr += [ ( LANDR, (OP0, OP0, OP1 ))]
        instr += [ ( LNOT, (OP0, OP0 ))]

        self.top_reg = False
        return instr


    def gen_b_not(self, operands):
        """
        a

        return ~a
        """
        t, op = operands[0]
        instr = []

        if t != STACK_TOP and self.top_reg:
            instr += self.gen_single_push(ACCUM)
            self.top_reg = False

        if t == NUMBER:
            instr += [ ( LADDI, (OP0, ZERO, int(~op) ))]
            self.top_reg = True
            return instr

        instr += self.fetch_one_operand(operands[0])

        instr += [ (LNOT, (OP0, OP0 ))]

        self.top_reg = True
        return instr

    def gen_halt(self):
        return [ (LHALT, None) ]

    def gen_pop(self, num):
        """
        If there is already a value in R0 (head of stack), then
        simply mark R0 as empty.

        After that, pop "n - 1" items from the real, physical stack.

        This method is not be used in cases when top_reg is being 
        turned off manually.
        """
        if self.top_reg:
            self.top_reg = False
            num -= 1

        if num == 0:
            return []

        return self.smart_add(SP, SP, num)

    def gen_physical_pop(self, num):
        """
        Simply reclaims "num" space from the physical stack.
        
        DOES NOT INCLUDE R0!
        DOES NOT LOOK AT TOP_REG!
        """

        if num == 0:
            return []

        return self.smart_add(SP, SP, num)


    def gen_loadcc(self, operand):
        """
        If '$', don't do anything. It is guaranteed to have been
        the last thing put into a register.

        Of course, it will load CC so the order is maintained
        (unlike fetch_one_operand)
        """
        t, op = operand

        if t == STACK_TOP:
            assert(self.top_reg)
            self.top_reg = False
            return [ ( LADDI, ( OP0, OP0, 0) ) ]
        elif t == ID:
            return self.read_var(ACCUM, op)
        elif t == NUMBER:
            return self.smart_set(ACCUM, op)

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
        The condition code is assumed to have been set in
        a prior LOAD_CC.
        If the CC value is NOT 0, then the branch is not taken.

        if CC != 0 do {body} else branch

        """
        lbl = operands

        rt_inst = self.read_table(ACCUM, lbl)

        instr = [ ( LBR, ( 'np', len(rt_inst) + 1) ) ]
        instr += rt_inst
        instr += [ ( LJMP, (ACCUM) )]

        return instr

    def gen_uncond_branch(self, operands):
        """
        Branches to the point specified by the label.
        """
        lbl = operands

        instr = self.read_table(ACCUM, lbl)
        instr += [ ( LJMP, (ACCUM) )]

        return instr


    def smart_add(self, dest_reg, src_reg, number):
        """
        Adds a fixed amount to a number
        """
        
        if -16 <= number <= 15:
            return [(LADDI, (dest_reg, src_reg, number))]

        instr = []

        if number < -16:
            instr += [(LADDI, (dest_reg, src_reg, -16))]
            number += 16
            while number < -16:
                instr += [(LADDI, (dest_reg, dest_reg, -16))]
                number += 16
            instr += [(LADDI, (dest_reg, dest_reg, number))]
        else:
            instr += [(LADDI, (dest_reg, src_reg, 15))]
            number += 15
            while number > 15:
                instr += [(LADDI, (dest_reg, dest_reg, 15))]
                number -= 15
            instr += [(LADDI, (dest_reg, src_reg, number))]

        return instr

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
        Puts the operand into R0. In case of a '$', does nothing, since
        the top of the stack MUST be in R0.

        DOES not guarantee anything about load order. CCs must be reset
        for safety. This is important in cases where the stack is
        manipulated after a function call:
            Return value is fetched, then  the stack is cleaned up. Therefore
        SP is last loaded.
        """
        t, op = operand

        if t == STACK_TOP:
            assert(self.top_reg)
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

        There are NO guarantees made regarding the last register to
        be loaded. There are outcomes when R0 was loaded last, R1 was
        loaded last, and SP was loaded last.
        """

        instr = []

        t0, op0 = operands[1]
        t1, op1 = operands[0]

        assert(not (t0 != STACK_TOP and t1 != STACK_TOP and self.top_reg))

        if t0 == STACK_TOP and t1 == STACK_TOP:
            
            if not commutative:
                instr += [ ( LADDI, (OP1, OP0, 0) ) ]
                instr += [ ( LLDR, ( OP0 ,SP, 0 ) ) ]
            else:
                instr += [ ( LLDR, ( OP1 ,SP, 0 ) ) ]

            instr += [ ( LADDI, (SP, SP, 1) ) ] # Pop

        elif t0 == STACK_TOP or t1 == STACK_TOP:
            tt = t1 if t0 == STACK_TOP else t0
            opt = op1 if t0 == STACK_TOP else op0

            if not commutative and t1 == STACK_TOP:
                instr += [ ( LADDI, (OP1, OP0, 0) )]
                if tt == NUMBER:
                    instr += self.smart_set(OP0, opt)
                elif tt == ID:
                    instr += self.read_var(OP0, opt)

            else:
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