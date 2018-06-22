from random import randint

NUMBER = 0
KEYWORD = 1
OPERATOR = 2
ID = 3
STRING = 4
NEWLINE = 5
COMMENT = 6

STACK_TOP = 8

AND = 'and'
OR = 'or'
NOT = 'not'
B_AND = '&' # bitwise and, or and not
B_OR = '|'
B_NOT = '~'
MULTI = '*'
DIVIS = '/'
MODULO = '%'
PLUS = '+'
MINUS = '-'
EQUAL = '='
COMMA = ','
SEMICOLON = ';'
COLON = ':'
LPAREN = '('
RPAREN = ')'
LBRACKET = '['
RBRACKET = ']'
LTHAN = '<'
GTHAN = '>'
LTHANEQ = '<='
GTHANEQ = '>='
DOUBLE_EQ = '=='

VALUE_AT = 'value_at'
ADDRESS_OF = 'address_of'
BLOCK = 'block'

RETURN = 'return'
PRINT = 'print'
INJECT = 'inject'

# These are different, since they instruct the (IR) machine what to do.
CREATE = '__create__'
POP = '__pop__'
PUSH = '__push__'
HALT = '__halt__'
SETUP_FUNC = '__setup_func__'
DESTROY_VARS = '__destroy_vars__'
JROUTINE = '__jump_to_routine___'
R_TOCALLER = '__return_to_caller__'
FETCH_RV = '__fetch_return_value__'
LOAD_CC = '__load_cc__'
COND_BRANCH = '__cond_branch__'
BRANCH = '__branch__'
SETUP_MAIN = '__setup_main__'

class IRMachine1():
    def __init__(self):
        self.var_loc = {}
        self.memory = [randint(0, 2 ** 16) for i in range(1000)]
        self.sp = randint(0, 1000)
        self.fp = randint(0, 1000)
        self.stack_frame = [{} for i in randint(0, 10)]
        self.running = True
        self.pc = 0
        self.link = randint(0, 1000) # The link register

        self.cc = randint(-999, 1000)

        pass

    def perform_operation(self, operands, operation, labels, inv_labels):
        
        if operation == SETUP_MAIN:
            self.setup_main()
        elif operation == CREATE:
            self.create_var(operands)
        elif operation == POP:
            self.pop()
        elif operation == PUSH:
            self.push(operands)
        elif operation == HALT:
            self.halt()
        elif operation == SETUP_FUNC:
            self.setup_func(operands)
        elif operation == DESTROY_VARS:
            self.destroy_vars(operands)
        elif operation == JROUTINE:
            self.jump_to_routine(operands, labels)
        elif operation == R_TOCALLER:
            self.return_to_caller()
        elif operation == RETURN:
            self.return_value()
        elif operation == FETCH_RV:
            self.fetch_return_value(operands)
        elif operation == LOAD_CC:
            self.load_cc(operands)
        elif operation == COND_BRANCH:
            self.conditional_branch(operands, labels)
        elif operation == BRANCH:
            self.branch()


        if operation == NOT:
            return int(not op0)

        if operation == PLUS:
            return op0 + op1
        elif operation == MINUS:
            return op0 - op1
        elif operation == MULTI:
            return op0 * op1
        elif operation == DIVIS:
            return op0 / op1
        elif operation == MODULO:
            return op0 % op1
        elif operation == AND:
            return int(op0 and op1)
        elif operation == OR:
            return int(op0 and op1)
        elif operation == GTHAN:
            return int(op0 > op1)
        elif operation == LTHAN:
            return int(op0 < op1)
        elif operation == DOUBLE_EQ:
            return int(op0 == op1)


    def run(self, instructions, labels, inv_labels):

        self.pc = 0

        while (self.running):
            operands, instruction = instructions[i]

            self.perform_operation(operands, instruction, labels, inv_labels)

    def setup_main(self):
        """
        Sets up the frame pointer, stack pointer, and current frame to a clean
        state.
        Increments the PC.
        """

        self.fp = 0
        self.sp = -1
        self.stack_frame = [{}]

        self.pc += 1

    def create_var(self, operands):
        """
        The CREATE instruction has two meanings, as described in notes. These
        meanings will change as the IRMachine evolves, and starts storing
        variables on the stack.
        1) a = $
            Mark the top-most position of the stack as belonging to the variable
            "a".
        2) a = <const or other var>
            Claim space on the stack first and then put the constant or variable
            within there.
        In both cases, the location of the variable will be recorded within
        self.stack_frame
        """

        t1, op1 = operands[0]
        t0, var = operands[1]

        if t1 == NUMBER:
            self.sp += 1
            self.memory[self.sp] = op1
        elif t1 == ID:
            self.sp += 1
            self.memory[self.sp] = self.memory[self.fp + self.stack_frame[-1][op1]]

        # Store the location of the newly created variable.
        self.stack_frame[-1][var] = self.sp - self.fp

        self.pc += 1

    def pop(self):
        """
        Pops the stack (doesn't clean up garbage, stack will remain dirty)
        """
        self.sp -= 1
        self.pc += 1

    def push(self, params):
        """
        Pushes params on to the stack, usually to be consumed by some function.
        """

        # For now, screw the intelligence crap. That's the code generator's
        # responsibility.

        # Stores the actual values of the params
        vals = []

        i = 0

        for t, op in params:
            if t == STACK_TOP:
                vals.append(self.memory[self.sp - i])
                i += 1
            elif t == ID:
                vals.append(self.memory[self.fp + self.stack_frame[-1][op]])
            elif t == NUMBER:
                vals.append(op)


        # Makee stack pointer point to where it should be pointing after popping
        # $ type arguments off the stack.
        self.sp -= i

        # Claim space for the new values
        self.sp += len(vals)

        # Copy the values on to the stack
        i = 0
        for v in vals:
            self.memory[self.sp - len(vals) + 1 + i] = v
            i += 1

        self.pc += 1


    def halt(self):
        """
        Halts the IRMachine
        """
        self.running = False

    def setup_func(self, operands):
        """
        Makes room for the return value, return address and old frame pointer.
        Stores return address and old frame pointer.
        Resets the frame pointer.
        Creates and adds params to stack_frame.
        """

        # make room for RV, RA and old FP
        self.sp += 3

        # store old RA and old fp
        self.memory[self.sp] = self.fp
        self.memory[self.sp - 1] = self.link

        # reset the frame pointer
        self.fp = self.sp + 1

        # Create and add params to stack_frame
        new_frame = {}
        num_params = len(operands)

        for i, param in enumerate(operands):
            new_frame[param] = self.fp - 3 - i

        self.stack_frame.append(new_frame)

        self.pc += 1

    def destroy_vars(self, operands):
        """
        Destroys all the variables created within some scope:
        - Removes them from the stack frame
        - Reclaims the area occupied by them on the stack.
        """

        print('Deleting variables:')

        num_to_del = len(operands)

        # REmove from stack frame
        curr_frame = self.stack_frame[-1]
        for var in operands:
            print('{} : {}'.format(var, self.memory[self.fp + curr_frame[var]]))
            del curr_frame[var]

        # reclaim stack space
        self.sp -= num_to_del

        self.pc += 1


    def jump_to_routine(self, function, labels):
        """
        Stores the incremented value of the PC in the link register.
        Sets PC to the location of the subroutine.
        """

        self.link = self.pc + 1

        self.pc = labels[function]


    def return_to_caller(self):
        """
        Cleans up the stack, and doesn't insert a value to RV position.
        """

        print('Returning GARBAGE to caller.')
        self._tear_and_return()


    def return_value(self, operand):
        """
        RETURN has two meanings:
        1) If the operand is $, then pop the value and place it into the RV spot
        2) If the operand is ID, NUM, etc, then copy its value to the RV spot.

        Then, do the rest as return_to_caller does
        """
        
        t, op = operand
        val = 0

        ret_val = 0

        if t == STACK_TOP:
            val = self.memory[self.sp]
            self.sp -= 1
            self.memory[self.fp - 3] = val
        elif t == ID:
            self.memory[self.fp - 3] =\
                self.memory[self.fp + self.stack_frame[-1][op]]
        elif t == NUM:
            self.memory[self.fp - 3] = op


        ret_val = self.memory[self.fp - 3]
        print('Returning VALUE: {} to caller.'.format(ret_val))

        self._tear_and_return()

    def _tear_and_return(self):
        """
        Tears down the stack (on the callee side), and restores the values of
        the RA and old FP.
        Destroys the current stack frame.
        Sets PC to value in link
        """

        # Tear down stack and destroy current stack frame
        curr_frame = self.stack_frame.pop()

        print('Deleting vars:')
        for var, loc in curr_frame.items():
            print('{} : {}'.format(var, self.memory[self.fp + loc]))

        self.sp = self.fp - 1

        # Restore old RA and FP
        self.link = self.memory[self.fp - 2]
        self.fp = self.memory[self.fp - 1]

        # Make sp point to return value
        self.sp -= 2

        # Go back to caller
        self.pc = self.link

    def fetch_return_value(self, params):
        """
        Fetches the value that the stack pointer is pointing at, reclaims the
        space occupied by params pushed earlier. See note 9 for more details.
        """

        num_params = len(params)

        self.memory[self.sp - num_params] = self.memory[self.sp]
        self.sp -= num_params

        self.pc += 1


    def load_cc(self, operand):
        """
        LOAD_CC has two meanings:
        1) if the operand type is $, pop the value and load CC with it
        2) else simply load CC
        """

        t, op = operand

        if t == STACK_TOP:
            self.cc = self.memory[self.sp]
            self.sp -= 1
        elif t == ID:
            self.cc = self.memory[self.fp + self.stack_frame[-1][op]]
        elif t == NUMBER:
            self.cc = op

        self.pc += 1

    def conditional_branch(self, lbl, labels):
        """
        Looks at the CC and if it IS ZERO, it branches to the point specified
        by the label. Otherwise does nothing.
        """

        if self.cc == 0:
            self.pc = labels[lbl]
        else:
            self.pc += 1

    def branch(self, lbl, labels):
        """
        Unconditionally branch to the label.
        """
        self.pc = labels[lbl]