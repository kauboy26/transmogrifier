from random import randint, seed
from core.constants import *

class IRMachine1():
    def __init__(self):
        print('Creating IR....')
        self.seed = randint(-1000, 1000)
        seed(self.seed)
        self.memory = [0 for i in range(10000)]
        self.sp = randint(-1000, 1000)
        self.fp = randint(-1000, 1000)
        self.stack_frame = [{} for i in range(randint(0, 10))]
        self.running = True
        self.pc = 0
        self.link = randint(0, 1000) # The link register
        self.cc = randint(-999, 1000)

        self.func_help = None

        # Console IO
        self.buf_ptr = 0
        self.buffer = ''

        print('Finished creating IR.')

    def perform_operation(self, operands, operation, labels, inv_labels):
        
        if operation == SETUP_MAIN:
            self.setup_main()
        elif operation == POP:
            self.pop()
        elif operation == PUSH:
            self.push(operands)
        elif operation == HALT:
            self.halt()
        elif operation == SETUP_FUNC:
            self.setup_func(operands)
        elif operation == CLEAN_MAIN:
            self.clean_main(operands)
        elif operation == JROUTINE:
            self.jump_to_routine(operands, labels)
        elif operation == R_TOCALLER:
            self.return_to_caller()
        elif operation == RETURN:
            self.return_value(operands)
        elif operation == FETCH_RV:
            self.fetch_return_value(operands)
        elif operation == LOAD_CC:
            self.load_cc(operands)
        elif operation == COND_BRANCH:
            self.conditional_branch(operands, labels)
        elif operation == BRANCH:
            self.branch(operands, labels)
        elif operation == MEM_ASSIGN:
            self.mem_assign(operands)
        elif operation == EQUAL:
            self.assign(operands)
        elif operation == MEM:
            self.read_memory(operands)
        elif operation == MEM_ARR_ASSIGN:
            self.mem_arr_assign(operands)
        elif operation == ARR_ASSIGN:
            self.arr_assign(operands)
        elif operation == GETC:
            self.getc()
        elif operation == OUTC:
            self.outc(operands)
        elif operation == PRINT:
            self.puts(operands)

        else:

            # print('doig op"{}"'.format(operation))

            vals = self._get_operand_values(operands)

            # print('operands', operands)

            op0 = vals[0] # These are in the wrong order

            if operation == NOT:
                val = int(not op0)
            elif operation == B_NOT:
                val = int(~op0)

            else:
                op0 = vals[1]
                op1 = vals[0]

                if operation == PLUS:
                    val = op0 + op1
                elif operation == MINUS:
                    val = op0 - op1
                elif operation == MULTI:
                    val = op0 * op1
                elif operation == DIVIS:
                    val = int(op0 / op1)
                elif operation == MODULO:
                    val = op0 % op1
                elif operation == AND:
                    val = int(op0 and op1)
                elif operation == OR:
                    val = int(op0 or op1)
                elif operation == GTHAN:
                    val = int(op0 > op1)
                elif operation == LTHAN:
                    val = int(op0 < op1)
                elif operation == DOUBLE_EQ:
                    val = int(op0 == op1)
                elif operation == LTHANEQ:
                    val = int(op0 <= op1)
                elif operation == GTHANEQ:
                    val = int(op0 >= op1)
                elif operation == B_AND:
                    val = int(op0 & op1)
                elif operation == B_OR:
                    val = int(op0 | op1)

            self.sp += 1

            self.memory[self.sp] = val

            self.pc += 1

    def debug(self, instructions, labels, inv_labels, func_help):

        print('Debug...')
        self.func_help = func_help
        self.pc = 0

        num_executed = 0
        while not input() and self.running:
            num_executed += 1
            operands, instruction = instructions[self.pc]
            print(self.pc, ':', operands, instruction)       
            self.perform_operation(operands, instruction, labels, inv_labels)
            self.print_regs()
            

        print('Finished running. Executed {} instructions.'.format(num_executed))

    def run(self, instructions, labels, inv_labels, func_help):
        """
        Runs a set of instructions given labels and inv_labels. The
        instructions, labels and inv_labels are assumed to be valid, and the
        IRMachine performs no checks.
        """
        print('Running...\n')
        print('Console:')
        print('_________________________________________________________________\n')
        self.func_help = func_help
        self.pc = 0

        num_executed = 0
        while self.running:
            num_executed += 1
            operands, instruction = instructions[self.pc]
            # print(self.pc, ':', operands, instruction)       
            self.perform_operation(operands, instruction, labels, inv_labels)
            # self.print_regs()
        
        print('\n________________________________________________________________')

        print('\n\nFinished running. Executed {} instructions.'.format(num_executed))


    def print_memory(self, low, high):
        print('***************************\nPrinting memory:\n')
        for i in range(low, high):
            print('{:4} : {:6}'.format(i, self.memory[i]))

    def print_regs(self):
        """
        Print the "registers"
        """
        print('***************************\nPrinting regs:')
        print('CC:', self.cc)
        print('SP:', self.sp)
        print('FP:', self.fp)
        print('LINK:', self.link)
        print('# PC:', self.pc)

    def setup_main(self):
        """
        Sets up the frame pointer, stack pointer, and current frame to a clean
        state.
        Increments the PC.
        """

        self.fp = 0
        self.sp = -1
        self.stack_frame = [{}]

        for var in self.func_help[MAIN_FUNC]:
            # Really, this will be implemented with a self.sp += num_vars
            self.sp += 1
            self.stack_frame[-1][var] = self.sp        

        self.pc += 1

    def assign(self, operands):
        """
        Assigns the value to the variable. The variable is assumed to exist.
        Equal will eat things from the stack when necessary. This is meant
        for variables. Writes to memory locations are handled by mem_assign.
        """
        t1, op1 = operands[0]
        t0, var = operands[1]

        if t1 == STACK_TOP:
            self.memory[self.fp + self.stack_frame[-1][var]] = self.memory[self.sp]
            self.sp -= 1 # and POP
        elif t1 == ID:
            self.memory[self.fp + self.stack_frame[-1][var]] =\
                self.memory[self.fp + self.stack_frame[-1][op1]]
        elif t1 == NUMBER:
            self.memory[self.fp + self.stack_frame[-1][var]] = op1

        self.pc += 1

    def mem_assign(self, operands):
        """
        Handles writes to memory locations. In case the location is specified
        by the top of the stack, the top of the stack is eaten.
        """

        t1, op1 = operands[0]
        t0, loc = operands[1]

        location = 0
        pop_count = 0 # How many to pop

        if t0 == STACK_TOP:
            # When location specified by stack top. See note 11.
            if t1 == STACK_TOP:
                location = self.memory[self.sp - 1]
            else:
                location = self.memory[self.sp]
            pop_count = 1
        elif t0 == ID:
            location = self.memory[self.fp + self.stack_frame[-1][loc]]
        elif t0 == NUMBER:
            location = loc

        

        if t1 == STACK_TOP:
            self.memory[location] = self.memory[self.sp]
            pop_count += 1
        elif t1 == ID:
            self.memory[location] =\
                self.memory[self.fp + self.stack_frame[-1][op1]]
        elif t1 == NUMBER:
            self.memory[location] = op1

        # print('Write location:', location, ', value:', self.memory[location])

        self.sp -= pop_count
        self.pc += 1

    def read_memory(self, location):
        """
        Reads the value at the location specified by 'location', and then pushes
        that value on to the stack. In case the location is specified by the
        stack top, the stack size will remain unchanged.
        """

        t, op = location

        value = 0
        loc = 0

        if t == STACK_TOP:
            loc = self.memory[self.sp]
        elif t == ID:
            self.sp += 1
            loc = self.memory[self.fp + self.stack_frame[-1][op]]
        elif t == NUMBER:
            self.sp += 1
            loc = op

        self.memory[self.sp] = self.memory[loc]
        # print('Read location:', loc, ', value:', self.memory[self.sp])
        self.pc += 1

    def mem_arr_assign(self, operands):
        """
        Creates an array on the stack, and puts the pointer to that array
        into the location specified by the memory location.
        """

        t1, op1 = operands[0]
        t0, loc = operands[1]

        length = 0
        location = 0
        pop_count = 0 # How many to pop

        if t0 == STACK_TOP:
            # When location specified by stack top. See note 11.
            if t1 == STACK_TOP:
                location = self.memory[self.sp - 1]
            else:
                location = self.memory[self.sp]
            pop_count = 1
        elif t0 == ID:
            location = self.memory[self.fp + self.stack_frame[-1][loc]]
        elif t0 == NUMBER:
            location = loc
        

        if t1 == STACK_TOP:
            length = self.memory[self.sp]
            pop_count += 1
        elif t1 == ID:
            length = self.memory[self.fp + self.stack_frame[-1][op1]]
        elif t1 == NUMBER:
            length = op1
        elif t1 == STRING:
            length = len(op1) + 1

        # print('Write location:', location, ', value:', self.memory[location])

        self.sp -= pop_count

        # Now we have the length and location.

        # put the length on the stack
        self.sp += 1
        self.memory[self.sp] = length

        # get the pointer to the array
        pointer = self.sp + 1
        self.sp += length

        self.memory[location] = pointer

        # If it's a string, initialize that memory
        if t1 == STRING:
            for i, c in enumerate(op1):
                self.memory[pointer + i] = ord(c)
            self.memory[pointer + length - 1] = 0 # Null terminated

        self.pc += 1

    def arr_assign(self, operands):
        """
        Creates an array on the stack and puts the pointer to that array
        into the specified variable.
        """

        t1, op1 = operands[0]
        t0, var = operands[1]


        if t1 == STACK_TOP:
            # then the length is already in the right place
            length = self.memory[self.sp]
        else:
            if t1 == ID:
                length = self.memory[self.fp + self.stack_frame[-1][op1]]
            elif t1 == NUMBER:
                length = op1
            elif t1 == STRING:
                length = len(op1) + 1
            self.sp += 1
            self.memory[self.sp] = length

        pointer = self.sp + 1
        self.sp += length

        if t1 == STRING:
            for i, c in enumerate(op1):
                self.memory[pointer + i] = ord(c)
            self.memory[pointer + length - 1] = 0

        self.memory[self.fp + self.stack_frame[-1][var]] = pointer

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
        vals = self._get_operand_values(params)

        # print('Pushing vals:')
        # print(vals)

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

        func_name, params = operands

        # make room for RV, RA and old FP
        self.sp += 3

        # store old RA and old fp
        self.memory[self.sp] = self.fp
        self.memory[self.sp - 1] = self.link

        # reset the frame pointer
        self.fp = self.sp + 1

        # Create and add params to stack_frame
        new_frame = {}
        num_params = len(params)

        for i, param in enumerate(params):
            new_frame[param] = - 4 - i

        # Make room for local variables
        self.sp += len(self.func_help[func_name])
        for i, var in enumerate(self.func_help[func_name]):
            new_frame[var] = i

        self.stack_frame.append(new_frame)

        # print('Stack frame: after setting up new stack:')
        # print(self.stack_frame)
        self.pc += 1

    def clean_main(self, operands):
        """
        Cleans up the main method, by reclaiming stack space.
        """

        # print('\n\n*************************************'
        #     '\nCleaning main method:')

        num_to_del = len(operands)

        # Remove from stack frame
        curr_frame = self.stack_frame.pop()
        # for var in operands:
        #     print('{} : {}'.format(var, self.memory[self.fp + curr_frame[var]]))

        # Reset to original position
        self.sp = -1

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

        # print('Returning GARBAGE to caller.')
        self._tear_and_return()


    def return_value(self, operand):
        """
        RETURN has two meanings:
        1) If the operand is $, then pop the value and place it into the RV spot
        2) If the operand is ID, NUMBER, etc, then copy its value to the RV spot.

        Then, do the rest as return_to_caller does
        """
        
        t, op = operand[0]
        val = 0

        ret_val = 0

        if t == STACK_TOP:
            val = self.memory[self.sp]
            self.sp -= 1
            self.memory[self.fp - 3] = val
        elif t == ID:
            self.memory[self.fp - 3] =\
                self.memory[self.fp + self.stack_frame[-1][op]]
        elif t == NUMBER:
            self.memory[self.fp - 3] = op


        ret_val = self.memory[self.fp - 3]
        # print('Returning VALUE: {} to caller.'.format(ret_val))

        self._tear_and_return()

    def getc(self):
        """
        Gets a single character a pushes it on to the stack. Although only
        a single character is retrieved at pushed on to the stack at a time,
        there is a buffer.
        """
        while self.buf_ptr >= len(self.buffer):
            self.buffer = input()
            self.buf_ptr = 0

        c = self.buffer[self.buf_ptr]
        self.buf_ptr += 1

        self.sp += 1
        self.memory[self.sp] = ord(c)

        self.pc += 1

    def outc(self, operand):
        """
        Prints the ascii character corresponding to the operand's value.
        """

        t, op = operand

        c = 0

        if t == ID:
            c = self.memory[self.fp + self.stack_frame[-1][op]]
        elif t == NUMBER:
            c = op
        elif t == STACK_TOP:
            c = self.memory[self.sp]

        print(chr(c), end='')

        self.pc += 1

    def puts(self, operand):
        """
        operand - address of the first letter of the string
        Keeps printing until a null is encountered.
        """

        t, op = operand

        ptr = 0

        if t == ID:
            ptr = self.memory[self.fp + self.stack_frame[-1][op]]
        elif t == NUMBER:
            ptr = op
        elif t == STACK_TOP:
            ptr = self.memory[self.sp]


        # Now print starting from the pointer
        while self.memory[ptr]:
            print(chr(self.memory[ptr]), end='')
            ptr += 1


        self.pc += 1



    def _tear_and_return(self):
        """
        Tears down the stack (on the callee side), and restores the values of
        the RA and old FP.
        Destroys the current stack frame.
        Sets PC to value in link
        """

        # Tear down stack and destroy current stack frame
        curr_frame = self.stack_frame.pop()

        # print('Deleting vars:')
        for var, loc in curr_frame.items():
            # print('{} : {}'.format(var, self.memory[self.fp + loc]))
            pass

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

        # print('CC loaded with {}.'.format(self.cc))

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

    def _get_operand_values(self, operands):
        """
        Returns the values of the operands requested. Also handles reclaiming
        stack space whenever things were popped.
        """
        vals = []

        i = 0

        for t, op in operands:
            if t == STACK_TOP:
                vals.append(self.memory[self.sp - i])
                i += 1
            elif t == ID:
                vals.append(self.memory[self.fp + self.stack_frame[-1][op]])
            elif t == NUMBER:
                vals.append(op)
            elif t == ADDRESS:
                vals.append(self.fp + self.stack_frame[-1][op])


        # Makee stack pointer point to where it should be pointing after popping
        # $ type arguments off the stack.
        self.sp -= i

        return vals
