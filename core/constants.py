NUMBER = 0
KEYWORD = 1
OPERATOR = 2
ID = 3
STRING = 4
NEWLINE = 5
COMMENT = 6

STACK_TOP = 8
MEM_LOC = 9

ADDRESS = 10
ARR_TYPE = 11

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

MEM = 'mem'
ADDRESS_OF = 'addrOf'
ARRAY = 'array'
DEF = 'def'
DEF2 = 'define'
DECLARE = 'declare'
IF = 'if'
ELIF = 'elif'
ELSE = 'else'
WHILE = 'while'
END = 'end'
MAIN = 'main'
RETURN = 'return'
GETC = 'getc'
OUTC = 'outc'
PRINT = 'print'
INJECT = 'inject'

# These are different, since they instruct the (IR) machine what to do.
POP = '__pop__'
PUSH = '__push__'
HALT = '__halt__'
SETUP_FUNC = '__setup_func__'
CLEAN_MAIN = '__clean_main__'
JROUTINE = '__jump_to_routine___'
R_TOCALLER = '__return_to_caller__'
FETCH_RV = '__fetch_return_value__'
LOAD_CC = '__load_cc__'
COND_BRANCH = '__cond_branch__'
BRANCH = '__branch__'
SETUP_MAIN = '__setup_main__'
MEM_ASSIGN = '__mem_assign__'
MAIN_FUNC = '__main_func__'
ARR_ASSIGN = '__array_assign__'
MEM_ARR_ASSIGN = '__mem_array_assign__'

HIGHEST_PRECEDENCE = 500
LOWEST_PRECEDENCE = 0