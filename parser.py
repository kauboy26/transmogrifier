from miscell import check

# I will use these constants to save myself some trouble in
# typing. Sublime's autocompletion feature my friend.
NUMBER = 0
KEYWORD = 1
OPERATOR = 2
ID = 3
STRING = 4
NEWLINE = 5
COMMENT = 6

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
IF = 'if'
ELIF = 'elif'
ELSE = 'else'
WHILE = 'while'
END = 'end'
MAIN = 'main'
RETURN = 'return'
PRINT = 'print'
INJECT = 'inject'

def parse(token_list=[]):
    