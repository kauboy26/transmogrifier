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
                    LPAREN: 0, RPAREN: 1,
                    # functions:
                    VALUE_AT: 200, ADDRESS_OF: 200, BLOCK: 200, PRINT: 200, INJECT: 200}


    args_needed = {MULTI: 2, DIVIS: 2, MODULO: 2, PLUS: 2, MINUS: 2, NOT: 1,
                    AND: 2, OR: 2, LTHAN: 2, GTHAN: 2, GTHANEQ: 2, LTHANEQ: 2,
                    DOUBLE_EQ: 2, EQUAL: 2,
                    VALUE_AT: 1, ADDRESS_OF: 1,
                    BLOCK: 1, PRINT: 1, INJECT: 1}

    primitive_functions = {VALUE_AT: 0, ADDRESS_OF: 0, BLOCK: 0, PRINT: 0,
                            INJECT: 0}

    line_number = 1

    functions = {}
    variables = {}
    created_vars = 0 # Counts the number of variables created in a single statement.

    op_stack = []
    num_stack = []
    args_count_stack = []

    ir_form = []

    op_stack_length = 0
    num_stack_length = 0

    i = 0
    length = len(token_list)
    while i < len(token_list):
        tk_type, value = token_list[i]

        if tk_type == NUMBER:
            num_stack.append((NUMBER, value))
            num_stack_length = num_stack_length + 1
            i = i + 1
        elif tk_type == ID:
            if value in functions:
                token_list[i] = (OPERATOR, value)
                continue
            num_stack.append((ID, value))
            num_stack_length = num_stack_length + 1
            i = i + 1
        elif tk_type == KEYWORD:
            if value == MAIN:
                pass
            elif value == DECLARE:
                # Process the entire declare here.
                func_name, args_count, i, line_number\
                    = process_declare(token_list, i, functions, line_number)
                functions[func_name] = args_count
                precedence[func_name] = 200
                args_needed[func_name] = args_count
            elif value == DEF:
                pass
            elif value == IF:
                pass
            elif value == ELIF:
                pass
            elif value == ELSE:
                pass
            elif value == WHILE:
                pass
            elif value == END:
                pass
        elif tk_type == OPERATOR:

            if value == LPAREN:
                op_stack.append(value)
                op_stack_length = 0
                num_stack_length = 0
                i = i + 1
                continue

            if value in functions:
                args_count_stack.append(0)

            if (value == PLUS or value == MINUS) and (op_stack_length == num_stack_length):
                print('called')
                if value == MINUS:
                    num_stack.append((NUMBER, -1))
                    num_stack_length = num_stack_length + 1
                    value = '*'
                else: # value == PLUS
                    # Skip this iteration. Basically fuck the extra plus sign.
                    i = i + 1
                    continue

            if value == NOT:
                # Does this solve the double NOT problem? Maybe it'll come back
                # to bite me, see note 1.
                op_stack.append(value)
                op_stack_length = op_stack_length + 1
                i = i + 1
                continue

            while op_stack and precedence[value] <= precedence[op_stack[-1]]:
                operation = op_stack.pop()
                op_stack_length = op_stack_length - 1

                check(operation in args_needed, 'Error evaluating statement. '
                    'Hints: Mismatched parens. See "{}". Line number: {}'
                    .format(operation, line_number))
                check(len(num_stack) >= args_needed[operation], 'Incorrect args'
                    ' to operation (or function) "{}". Needed {}, but found {}.'
                    ' Line number: {}'
                    .format(operation, args_needed[operation],
                        num_stack_length, line_number))
                if value in functions:
                    args_found = args_count_stack.pop()
                    args_req = args_needed[value]
                    check((args_req <= 1 and args_found == 0)\
                        or args_req == args_found + 1, 'Not enough args found '
                        'to function {}. Needed {}, but found {}. Line number: '
                        '{}'
                        .format(value, args_req, args_found + 1, line_number))

                operands = [num_stack.pop() for i in range(args_needed[operation])]
                num_stack_length = num_stack_length - args_needed[operation]

                # Ensure the required variables exist, or create variables in
                # the case of an assignment statement.
                if operation == EQUAL:
                    check_operands_exist(operands[:-1], variables, line_number)
                    check(not op_stack, 'Illegal statement. Line number: {}'
                        .format(line_number)) # See note 3
                    c, v = operands[-1]
                    check(c == ID, 'Cannot assign value to a literal. Line'
                        ' number: {}'.format(line_number))
                    if v not in variables:
                        # Create the variable
                        ir_form.append(([operands[-1]], CREATE))
                        created_vars = created_vars + 1
                        variables[v] = 0
                else:
                    check_operands_exist(operands, variables, line_number)

                ir_form.append((operands, operation))
                print(ir_form)

                num_stack.append((STACK_TOP, '$'))
                num_stack_length = num_stack_length + 1

            # At this point, either the operand stack is empty, or the top most
            # operand has a precedence lower than the newest operand.
            if value == RPAREN:
                check(op_stack and op_stack[-1] == LPAREN, 'Mismatched parens.'
                    ' Line number: {}'.format(line_number))
                op_stack.pop()

            elif value == COMMA:
                check(args_count_stack, '"," must appear to separate function'
                    ' arguments. Line number: {}'.format(line_number))
                args_count_stack[-1] = args_count_stack[-1] + 1
                op_stack_length = 0
                num_stack_length = 0
            elif value == SEMICOLON:
                check(len(num_stack) <= 1, 'Error in statement. Hints: an oper'
                    'ation has too many arguments, or semicolon could be '
                    'missing. Line number: {}'.format(line_number))
                check(created_vars <= 1, 'Cannot create more than one variable '
                    'in a single statement. Ensure that at most one variable is'
                    ' not defined. Line number: {}'.format(line_number)) # note 3
                check(not op_stack, 'Illegal statement. Line number: {}'
                    .format(line_number))
                created_vars = 0
                num_stack_length = 0 # Cause of so much grief! TODO PUT THIS IN COLON too
                op_stack_length = 0
                # The num_stack has either 0 or 1 items in it. If it has 0 items
                # then that means this was probably (must) an empty statement.
                # Otherwise it means things went as usual. See note 2.
                if num_stack:
                    c, v = num_stack.pop()
                    if c == STACK_TOP:
                        # Therefore something was pushed on to the stack as a
                        # result of an operation. Otherwise a statement like
                        # "4;" was encountered, and nothing needs to be done.
                        ir_form.append((None, POP))
            else:
                op_stack.append(value)
                op_stack_length = op_stack_length + 1

            i = i + 1
        elif tk_type == COMMENT:
            # TODO need to put this into the ir so that comments are printed on
            # to the generated code.
            # print(value)
            i = i + 1
        elif tk_type == NEWLINE:
            line_number = line_number + 1
            i = i + 1

    # I think this may cause the user a lot of grief. A missing semicolon on one
    # line may not get detected until much much later. Perhaps this message needs
    # to be broadcast elsewhere.
    check(not num_stack, 'Missing semicolon? Line number: {}'
        .format(line_number))

    return ir_form


def check_operands_exist(operands, variables, line_number):
    # I realize that this is a bug source. The line number may not correctly
    # reflect where the variable actually is if the statement spans multiple
    # lines.
    for c, v in operands:
        check(c != ID or v in variables, 'The variable "{}" has not been'
            ' defined. Line number: {}'.format(v, line_number))


def process_declare(token_list, i, functions, line_number):
    """
    Process the entire declare, until the ":".
    token_list is the same token_list being used,
    i is the current position of the counter (should point to the DECLARE)
    """
    # At any point, if we hit the end of the token_list stream, the compiler
    # will crash. But there is little that can be done about that.

    i = i + 1 # Pass the DECLARE

    c, v = token_list[i]

    check(c == ID, 'The name {} is reserved or illegal. Line number: {}.'
        .format(v, line_number))
    check(v not in functions, 'The name {} has been used to declare a function.'
        ' Please use another name. Line number: {}'.format(v, line_number))

    func_name = v
    i = i + 1

    c, v = token_list[i]
    check(v == LPAREN, 'Expected "(" here. Got {}. Line number: {}'.format(v, line_number))
    i = i + 1
    
    args_count = 0
    comma_count = 0

    c, v = token_list[i]

    if (v != RPAREN):
        # There is at least one argument.
        while True:
            c, v = token_list[i]
            check(c == ID, 'Malformed function declaration. Line number: {}'.format(c, line_number))
            args_count = args_count + 1
            i = i + 1
            c, v = token_list[i]
            if v == COMMA:
                i = i + 1
                comma_count = comma_count + 1
            elif v == RPAREN:
                break
        check(comma_count == args_count - 1, 'Commas must separate arguments.'
            'Line number: {}'.format(line_number))

    # We have the correct number of arguments, and we should be pointing at
    # a right paren.

    i = i + 1 # pass right paren

    c, v = token_list[i]
    check(v == SEMICOLON, 'Malformed function declaration. Line number: {}'.format(line_number))

    i = i + 1
    return func_name, args_count, i, line_number