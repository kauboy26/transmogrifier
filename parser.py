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

HIGHEST_PRECEDENCE = 500
LOWEST_PRECEDENCE = 0

def parse(token_list=[]):
    check(token_list, 'The compiler that one not working guru')

    # For now just do some crap testing
    # Not too sure of some of these, such as comma vs semicolon. As far as I can
    # see right now, there won't be a time when the two will be compared.
    precedence = {MULTI: 150, DIVIS: 150, MODULO: 150, PLUS: 130, MINUS: 130,
                    NOT: 110, AND: 100, OR: 99, LTHAN: 120, GTHAN:120, LTHANEQ: 120,
                    GTHANEQ: 120, DOUBLE_EQ: 120, EQUAL: 80, COMMA: 70, SEMICOLON: 70,
                    LPAREN: 0, RPAREN: 1}

    args_needed = {MULTI: 2, DIVIS: 2, MODULO: 2, PLUS: 2, MINUS: 2, NOT: 1,
                    AND: 2, OR: 2, LTHAN: 2, GTHAN: 2, GTHANEQ: 2, LTHANEQ: 2,
                    DOUBLE_EQ: 2, EQUAL: 2}

    line_number = 1

    i = 0
    length = len(token_list)

    variables = {}

    op_stack = []
    num_stack = []
    args_count_stack = []

    ir_form = []

    op_stack_length = 0
    num_stack_length = 0

    while i < len(token_list):
        tk_type, value = token_list[i]

        if tk_type == NUMBER:
            num_stack.append((NUMBER, value))
            num_stack_length = num_stack_length + 1
            i = i + 1
        elif tk_type == ID:
            num_stack.append((ID, value))
            num_stack_length = num_stack_length + 1
            i = i + 1
        elif tk_type == OPERATOR:

            if value == LPAREN:
                op_stack.append(value)
                op_stack_length = 0
                num_stack_length = 0
                i = i + 1
                continue

            if (value == PLUS or value == MINUS) and (op_stack_length == num_stack_length):
                if value == MINUS:
                    num_stack.append((NUMBER, -1))
                    num_stack_length = num_stack_length + 1
                    value = '*'
                else: # value == PLUS
                    # Skip this iteration. Basically fuck the extra plus sign.
                    i = i + 1
                    continue

            if value == NOT:
                # Does this solve the double NOT problem? Maybe it'll come back to bite me.
                op_stack.append(value)
                op_stack_length = op_stack_length + 1
                i = i + 1
                continue

            while op_stack and precedence[value] <= precedence[op_stack[-1]]:
                operation = op_stack.pop()
                op_stack_length = op_stack_length - 1

                check(len(num_stack) >= args_needed[operation], 'Not enough args to operation {}. Needed '
                    '{}, but found {}'.format(operation, args_needed[operation], num_stack_length))

                operands = [num_stack.pop() for i in range(args_needed[operation])]
                num_stack_length = num_stack_length - args_needed[operation]
                ir_form.append((operands, operation))

                # TODO: variable existence
                num_stack.append((ID, '$'))
                num_stack_length = num_stack_length + 1

            # At this point, either the operand stack is empty, or the top most
            # operand has a precedence lower than the newest operand.
            if value == RPAREN:
                check(op_stack and op_stack[-1] == LPAREN, 'Mismatched parens')
                op_stack.pop()

            elif value == COMMA:
                check(args_count_stack, '"," must appear to separate function arguments.')
                args_count_stack[-1] = args_count_stack[-1] + 1
                op_stack_length = 0
                num_stack_length = 0
            elif value == SEMICOLON:
                check(len(num_stack) == 1, 'Problem in statement')
                num_stack.pop()
            else:
                op_stack.append(value)
                op_stack_length = op_stack_length + 1
            i = i + 1

        elif tk_type == NEWLINE:
            line_number = line_number + 1
            i = i + 1

    check(not num_stack, 'Missing semicolon?')
    return ir_form