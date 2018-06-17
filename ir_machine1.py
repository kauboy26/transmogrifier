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
DEF = 'def'
DECLARE = 'declare'
IF = 'if'
ELIF = 'elif'
ELSE = 'else'
WHILE = 'while'
END = 'end'
MAIN = 'main'
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
JUMP = '__jump__'
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
        self.sp = -1
        self.fp = randint(0, 1000)
        self.pc = 0

        pass

    def perform_operation(self, operands, operation):
        
        op0 = operands[1]

        if operation == NOT:
            return int(not op0)

        op1 = operands[0]

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


    def run(self, instructions):

        to_go = []

        while (True):
            operands, operation = instructions[self.pc]
            # Fetch operands:
            if operation == EQUAL:
                t1, op1 = operands[0]
                t0, op0 = operands[1]
                if t1 == NUMBER:
                    self.memory[self.var_loc[op0]] = op1
                elif t1 == ID:
                    self.memory[self.var_loc[op0]] = self.memory[self.var_loc[op1]]
                elif t1 == STACK_TOP:
                     self.memory[self.var_loc[op0]] = self.memory[self.sp]
                self.pc += 1
                continue

            if operation == CREATE:
                t1, op1 = operands[0]
                t0, op0 = operands[1]

                if t1 == STACK_TOP:
                    self.var_loc[op0] = self.sp
                else:
                    self.sp += 1
                    self.var_loc[op0] = self.sp
                    if t1 == NUMBER:
                        self.memory[self.var_loc[op0]] = op1
                    elif t1 == ID:
                        self.memory[self.var_loc[op0]] = self.memory[self.var_loc[op1]]
                self.pc += 1
                continue

            if operation == POP:
                self.sp -= 1
                self.pc += 1
                continue

            if operation == DESTROY_VARS:
                print("\nDestroying vars:")
                for v in operands:
                    print('{} : {}'.format(v, self.memory[self.var_loc[v]]))
                    del self.var_loc[v]
                self.sp -= len(operands)
                self.pc += 1
                continue

            if operation == HALT:
                break

            to_go = []
            for op_type, value in operands:
                if op_type == NUMBER:
                    to_go.append(value)
                elif op_type == ID:
                    to_go.append(self.memory[self.var_loc[value]])
                elif op_type == STACK_TOP:
                    to_go.append(self.memory[self.sp])
                    self.sp -= 1

            self.sp += 1
            self.memory[self.sp] = self.perform_operation(to_go, operation)
            self.pc += 1

        print('Stack: ', self.sp)

