from random import randint
from core.miscell import check

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
MEM_LOC = 9

ADDRESS = 10

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
BLOCK = 'block'
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
PRINT = 'print'
INJECT = 'inject'

# These are different, since they instruct the (IR) machine what to do.
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
MEM_ASSIGN = '__mem_assign__'
MAIN_FUNC = '__main_func__'

HIGHEST_PRECEDENCE = 500
LOWEST_PRECEDENCE = 0

def parse(token_list=[]):
    check(token_list, 'The compiler that one not working guru.', -1)

    # For now just do some crap testing
    # Not too sure of some of these, such as comma vs semicolon. As far as I can
    # see right now, there won't be a time when the two will be compared.
    precedence = {MULTI: 150, DIVIS: 150, MODULO: 150, PLUS: 130, MINUS: 130,
                    NOT: 110, AND: 100, OR: 99, LTHAN: 120, GTHAN:120, LTHANEQ: 120,
                    GTHANEQ: 120, DOUBLE_EQ: 120, EQUAL: 80, COMMA: 70, SEMICOLON: 70,
                    COLON: 70,
                    LPAREN: 0, RPAREN: 1,
                    # functions:
                    MEM: 200, ADDRESS_OF: 200, BLOCK: 200, PRINT: 200, INJECT: 200}


    args_needed = {MULTI: 2, DIVIS: 2, MODULO: 2, PLUS: 2, MINUS: 2, NOT: 1,
                    AND: 2, OR: 2, LTHAN: 2, GTHAN: 2, GTHANEQ: 2, LTHANEQ: 2,
                    DOUBLE_EQ: 2, EQUAL: 2,
                    MEM: 1, ADDRESS_OF: 1,
                    BLOCK: 1, PRINT: 1, INJECT: 1}

    primitive_functions = {MEM: 0, ADDRESS_OF: 0, BLOCK: 0, PRINT: 0,
                            INJECT: 0}

    effect_of = {MULTI: -1, DIVIS: -1, MODULO: -1, PLUS: -1, MINUS: -1, NOT: 0,
                    AND: -1, OR: -1, LTHAN: -1, GTHAN: -1, GTHANEQ: -1, LTHANEQ: -1,
                    DOUBLE_EQ: -1, EQUAL: -1, MEM: 0, ADDRESS_OF: 0,
                    BLOCK: 0, PRINT: 0, INJECT: 0}

    line_number = 1
    labels = {}
    n_lbl = 0
    ln_to_label = {}

    functions = {}
    defined_funcs = {}

    # this is used to figure out how much stack space to allocate
    # initially (counts num vars created).
    func_help = {}
    vars_of_func = {}
    curr_func = None

    # See note 4
    variables = {}
    vars_this_block = []
    curr_scope_type = []

    cond_lbls = [] # A stack to hold the control flow labels (for if, elif, etc)
    proc_cond_header = False

    created_vars = 0 # Counts the number of variables created in a single statement.
    main_found = False
    proc_func = False
    ret_statement = False

    op_stack = []
    num_stack = []
    args_count_stack = []
    effect = [0]

    ir_form = []


    i = 0
    length = len(token_list)
    while i < len(token_list):
        tk_type, value = token_list[i]

        if tk_type == NUMBER:
            num_stack.append((NUMBER, value))
            effect[-1] += 1
            i = i + 1
        elif tk_type == ID:
            if value in functions:
                token_list[i] = (OPERATOR, value)
                continue
            num_stack.append((ID, value))
            effect[-1] += 1
            i = i + 1
        elif tk_type == KEYWORD:
            check(not op_stack and not num_stack,
                'Syntax error. Hint: missing semicolon?', line_number)
            if value == MAIN:
                check(not main_found, 'Main method can be declared only once.', line_number)
                check(not proc_func, 'Bad syntax: the word "main" is reserved.', line_number)
                main_found = True
                proc_func = True
                i, line_number = process_main_header(token_list, i, line_number)
                vars_this_block.append([])
                curr_scope_type.append(MAIN)


                curr_func = MAIN_FUNC
                func_help[curr_func] = []
                vars_of_func = {}

                ir_form.append((None, SETUP_MAIN))
            elif value == DECLARE:
                # Process the entire declare here.
                func_name, args_count, i, line_number\
                    = process_declare(token_list, i, functions, line_number)
                functions[func_name] = args_count
                precedence[func_name] = 200
                args_needed[func_name] = args_count
                effect_of[func_name] = 1 - args_count

                func_help[func_name] = []

            elif value == DEF or value == DEF2:
                check(not proc_func, 'Functions cannot be declared within functions.', line_number)
                proc_func = True
                func_name, param_list, i, line_number\
                    = process_define(token_list, i, functions, defined_funcs,
                        line_number)
                ir_form.append(((func_name, param_list), SETUP_FUNC))

                labels[func_name] = len(ir_form) - 1
                ln_to_label[len(ir_form) - 1] = func_name
                n_lbl += 1

                vars_this_block.append(param_list[:])
                curr_scope_type.append(DEF)

                curr_func = func_name
                vars_of_func = {}

                for param in param_list:
                    variables[param] = 0

            elif value == IF:
                check(not proc_cond_header, 'Syntax error with "if".', line_number)
                proc_cond_header = True
                cond_lbls.append((generate_label(n_lbl, line_number), None))
                n_lbl += 1
                vars_this_block.append([])
                curr_scope_type.append(IF)
                i = i + 1
            elif value == ELIF:
                check(not proc_cond_header, 'Syntax error with "elif".', line_number)
                proc_cond_header = True
                check(curr_scope_type and\
                    (curr_scope_type[-1] == IF or curr_scope_type[-1] == ELIF),
                    'Illegal use of "elif".', line_number)
                
                curr_scope_type.pop()
                curr_scope_type.append(ELIF)

                lbl, end_lbl = cond_lbls.pop()
                end_lbl = end_lbl if end_lbl else 'END_{}'.format(lbl)

                ir_form.append((end_lbl, BRANCH))

                labels[lbl] = len(ir_form)
                ln_to_label[len(ir_form)] = lbl

                n_lbl += 1
                cond_lbls.append((generate_label(n_lbl, line_number), end_lbl))

                vars_to_remove = vars_this_block.pop()
                remove_variables(vars_to_remove, variables)

                vars_this_block.append([])
                i = i + 1

            elif value == ELSE:
                # Eat the ":"
                i = i + 1
                check(i < length, 'End of file reached abruptly.', line_number)
                tk_type, value = token_list[i]
                check(tk_type == OPERATOR and value == COLON, '"else" must be '
                    'followed by a colon (":").', line_number)

                # Check for valid scope
                check(not proc_cond_header, 'Syntax error with "else".', line_number)
                check(curr_scope_type and\
                    (curr_scope_type[-1] == IF or curr_scope_type[-1] == ELIF),
                    'Illegal use of "else".', line_number)

                curr_scope = curr_scope_type.pop()
                curr_scope_type.append(ELSE)

                lbl, end_lbl = cond_lbls.pop()

                if curr_scope == IF:
                    end_lbl = 'END_{}'.format(lbl)

                ir_form.append((end_lbl, BRANCH))

                labels[lbl] = len(ir_form)
                ln_to_label[len(ir_form)] = lbl
                
                cond_lbls.append((lbl, end_lbl))

                vars_to_remove = vars_this_block.pop()
                remove_variables(vars_to_remove, variables)

                vars_this_block.append([])

                i = i + 1
            elif value == WHILE:
                check(not proc_cond_header, 'Syntax error with "while".', line_number)
                proc_cond_header = True

                head_lbl = generate_label(n_lbl, line_number)
                end_lbl = generate_label(n_lbl + 1, line_number)
                n_lbl += 2

                cond_lbls.append((end_lbl, head_lbl))
                
                labels[head_lbl] = len(ir_form)
                ln_to_label[len(ir_form)] = head_lbl

                vars_this_block.append([])
                curr_scope_type.append(WHILE)
                i = i + 1
            elif value == END:
                check(curr_scope_type, 'Mismatched "end" (extra?).', line_number)
                scope_type = curr_scope_type.pop()

                vars_to_remove = vars_this_block.pop()
                remove_variables(vars_to_remove, variables)

                if scope_type == MAIN:

                    if vars_to_remove:
                        ir_form.append((func_help[MAIN_FUNC], DESTROY_VARS))
                        
                    ir_form.append((None, HALT))
                    proc_func = False
                    curr_func = None
                elif scope_type == DEF:
                    ir_form.append((None, R_TOCALLER))
                    proc_func = False
                    curr_func = None
                elif scope_type == IF:
                    lbl, end_lbl = cond_lbls.pop()

                    labels[lbl] = len(ir_form)
                    ln_to_label[len(ir_form)] = lbl

                elif scope_type == ELIF:
                    lbl, end_lbl = cond_lbls.pop()

                    labels[lbl] = len(ir_form) # Note 8
                    labels[end_lbl] = len(ir_form)
                    ln_to_label[len(ir_form)] = end_lbl
                elif scope_type == ELSE:
                    lbl, end_lbl = cond_lbls.pop()

                    labels[end_lbl] = len(ir_form)
                    ln_to_label[len(ir_form)] = end_lbl # TODO POSSIBLE BUG FROM LABEL CLASH (empty else)?
                elif scope_type == WHILE:

                    end_lbl, head_lbl = cond_lbls.pop()

                    ir_form.append((head_lbl, BRANCH))

                    labels[end_lbl] = len(ir_form)
                    ln_to_label[len(ir_form)] = end_lbl

                i = i + 1
            elif value == RETURN:
                check(not ret_statement, 'Illegal use of "return" keyword', line_number)
                ret_statement = True
                i = i + 1

        elif tk_type == OPERATOR:

            check(curr_scope_type, 'Illegal syntax! Hints: Cannot use declare '
                'statements outside of "main" or a "function". Another '
                'possibility is that a keyword has been mispelled.', line_number)

            if value == LPAREN:
                op_stack.append(value)
                effect.append(0)
                i = i + 1
                continue

            if value in functions or value in primitive_functions:
                args_count_stack.append(0)

            if (value == PLUS or value == MINUS) and effect[-1] == 0:
                if value == MINUS:
                    num_stack.append((NUMBER, -1))
                    effect[-1] += 1
                    value = MULTI
                else: # value == PLUS
                    # Skip this iteration. Basically fuck the extra plus sign.
                    i = i + 1
                    continue

            if value == NOT:
                # see note 1.
                op_stack.append(value)
                # effect[-1] += effect_of[NOT] -- Does nothing
                i = i + 1
                continue

            while op_stack and precedence[value] <= precedence[op_stack[-1]]\
                and effect[-1] > 0:

                operation = op_stack.pop()

                check(operation in args_needed, 'Error evaluating statement. '
                    'Hints: Mismatched parens. See "{}".'
                    .format(operation), line_number)


                operands = [num_stack.pop() for i in range(args_needed[operation])]
                # Ensure the required variables exist, or create variables in
                # the case of an assignment statement.
                if operation == EQUAL:
                    check_operands_exist(operands[:-1], variables, line_number)
                    check(not op_stack, 'Illegal statement.', line_number) # See note 3
                    c, v = operands[-1]
                    check(c == ID or c == MEM_LOC, 'Cannot assign value to a literal.', line_number)
                    if c == ID and v not in variables:
                        # Create the variable
                        ir_form.append((operands, EQUAL))
                        vars_this_block[-1].append(v)
                        created_vars = created_vars + 1
                        variables[v] = 0
                        if v not in vars_of_func:
                            func_help[curr_func].append(v)
                            vars_of_func[v] = 0
                    elif c == MEM_LOC:
                        ir_form.append(([operands[0], v], MEM_ASSIGN))
                    else:
                        ir_form.append((operands, operation))
                    continue
                else:
                    check_operands_exist(operands, variables, line_number)

                if operation in functions or operation in primitive_functions:
                    args_found = args_count_stack.pop()
                    args_req = args_needed[operation]
                    check((args_req <= 1 and args_found == 0)\
                        or args_req == args_found + 1, 'Not enough args found '
                        'to function {}. Needed {}, but found {}.'
                        .format(value, args_req, args_found + 1), line_number)

                    if operation in primitive_functions:
                        if operation == MEM:
                            if value == EQUAL:
                                # Simply convert
                                num_stack.append((MEM_LOC, operands[-1]))
                                continue
                            ir_form.append((operands[0], operation))
                            num_stack.append((STACK_TOP, '$'))
                        elif operation == ADDRESS_OF:
                            c, v = operands[0]
                            check(c == ID, 'Cannot find the address of a non-variable.', line_number)
                            num_stack.append((ADDRESS, v))

                        continue

                    ir_form.append((operands, PUSH))
                    ir_form.append((operation, JROUTINE))
                    ir_form.append((operands, FETCH_RV))
                    num_stack.append((STACK_TOP, '$'))
                    continue

                ir_form.append((operands, operation))
                num_stack.append((STACK_TOP, '$'))

            # At this point, either the operand stack is empty, or the top most
            # operand has a precedence lower than the newest operand.
            check(effect[-1] >= 0, 'Syntax error, too few operands?', line_number)
            if value == RPAREN:
                check(op_stack and op_stack[-1] == LPAREN, 'Mismatched parens.',
                    line_number)
                check(effect[-1] == 0 or effect[-1] == 1, #TODO
                    'Bad expr within parens.', line_number)
                op_stack.pop()
                effect[-2] += effect[-1]
                effect.pop()

            elif value == COMMA:
                check(args_count_stack, '"," must appear to separate function'
                    ' arguments.', line_number)
                args_count_stack[-1] = args_count_stack[-1] + 1

                check(effect[-1] == 1, 'Comma-related syntax error.', line_number)
                effect[-2] += 1
                effect[-1] = 0

            elif value == SEMICOLON:
                check(not op_stack, 'Illegal statement.', line_number)
                check(len(num_stack) <= 1 and len(effect) == 1 and effect[-1] <= 1,
                    'Error in statement. Hints: an operation has too many arguments,'
                    ' or semicolon could be missing, possibly from a previous statement.',
                    line_number)
                check(created_vars <= 1, 'Cannot create more than one variable '
                    'in a single statement. Ensure that at most one variable is'
                    ' not defined.', line_number) # note 3
                

                created_vars = 0
                effect[-1] = 0

                # The num_stack has either 0 or 1 items in it. If it has 0 items
                # then that means this was probably (definitely) an empty statement.
                # Otherwise it means things went as usual. See note 2.
                if num_stack:
                    c, v = num_stack.pop()
                    if ret_statement:
                        ir_form.append(([(c, v)], RETURN))
                        ret_statement = False
                    elif c == STACK_TOP:
                        ir_form.append((None, POP)) # See Note 6
                else:
                    check(not ret_statement, '"return" must return something.', line_number)
            elif value == COLON:
                check(proc_cond_header, 'Illegal use of ":".', line_number)
                check(not op_stack, 'Illegal statement, unexpected ":".', line_number)
                check(len(num_stack) == 1\
                    and len(effect) == 1 and effect[-1] == 1, 'Syntax error.', line_number)
                check(created_vars == 0, 'Cannot create variables here.', line_number)

                effect[-1] = 0
                ir_form.append((num_stack.pop(), LOAD_CC))
                ir_form.append((cond_lbls[-1][0], COND_BRANCH))

                proc_cond_header = False
            else:
                op_stack.append(value)
                effect[-1] += effect_of[value]

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
    check(not op_stack and not num_stack, 'Missing semicolon?', line_number)

    return ir_form, labels, ln_to_label, func_help


def check_operands_exist(operands, variables, line_number):
    # I realize that this is a bug source. The line number may not correctly
    # reflect where the variable actually is if the statement spans multiple
    # lines.
    for c, v in operands:
        check(c != ID or v in variables, 'The variable "{}" has not been'
            ' defined'.format(v), line_number)

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

    check(c == ID, 'The name {} is reserved or illegal.'.format(v), line_number)
    check(v not in functions, 'The name {} has been used to declare a function.'
        ' Please use another name.'.format(v), line_number)

    func_name = v
    i = i + 1

    c, v = token_list[i]
    check(v == LPAREN, 'Expected "(" here. Got {}.'.format(v),
        line_number)
    i = i + 1
    
    args_count = 0
    comma_count = 0

    c, v = token_list[i]

    if (v != RPAREN):
        # There is at least one argument.
        while True:
            c, v = token_list[i]
            check(c == ID, 'Malformed function declaration.'.format(c),
                line_number)
            args_count = args_count + 1
            i = i + 1
            c, v = token_list[i]
            if v == COMMA:
                i = i + 1
                comma_count = comma_count + 1
            elif v == RPAREN:
                break
        check(comma_count == args_count - 1, 'Commas must separate arguments.',
            line_number)

    # We have the correct number of arguments, and we should be pointing at
    # a right paren.

    i = i + 1 # pass right paren

    c, v = token_list[i]
    check(v == SEMICOLON, 'Malformed function declaration.', line_number)

    i = i + 1
    return func_name, args_count, i, line_number

def process_main_header(token_list, i, line_number):
    """
    i should be pointing at the token, "MAIN"
    """

    i = i + 1
    length = len(token_list)
    while i < length:
        tk_type, value = token_list[i]
        if tk_type == NEWLINE:
            line_number += 1
            i = i + 1
        elif tk_type == COMMENT:
            i = i + 1
        elif tk_type == OPERATOR and value == COLON:
            i = i + 1
            break
        else:
            check(False, 'Invalid "main" method header syntax: {} : {}'
                .format(tk_type, value),
                line_number)

    # "i" now points at the next token (actual stuff within the main method)
    return i, line_number

def remove_variables(variables_to_remove, variables):
    for variable in variables_to_remove:
        del variables[variable]

def process_define(token_list, i, functions, defined_funcs, line_number):
    """
    i points to the keyword "def" when this is called.
    functions are all the declared functions
    defined_funcs are all the functions that have been defined
    """

    i = i + 1
    length = len(token_list)

    while i < length:
        tk_type, value = token_list[i]
        if tk_type == NEWLINE:
            i = i + 1
            line_number = line_number + 1
        elif tk_type == COMMENT:
            i = i + 1
        else:
            break

    # We should now be pointing to the name of the function.
    tk_type, value = token_list[i]
    check(tk_type == ID, 'Syntax error. Expected function name, but was {}.'
        .format(value), line_number)

    check(value in functions, 'The function "{}" has not been declared.'
        .format(value), line_number)
    check(value not in defined_funcs, 'The function "{}" has already been defined.'
        .format(value), line_number)

    func_name = value

    defined_funcs[func_name] = 0

    i = i + 1
    tk_type, value = token_list[i]
    check(tk_type == OPERATOR and value == LPAREN, 'Syntax error processing'
        ' function header to function "{}"'.format(func_name), line_number)

    args_count = 0
    i = i + 1
    tk_type, value = token_list[i]

    params = {}
    param_list = [] # Doing list(params) will give me the thing out of order.

    if (tk_type == OPERATOR and value == RPAREN):
        args_count = 0
    else:
        check(tk_type == ID, 'Invalid syntax in func header.', line_number)
        check(value not in functions, 'Bad param name.', line_number)
        params[value] = 0
        param_list.append(value)
        args_count = 1

        i = i + 1
        tk_type, value = token_list[i] # Please excuse the million times I call this line.


        while not (tk_type == OPERATOR and value == RPAREN):
            tk_type, value = token_list[i]
            check(tk_type == OPERATOR and value == COMMA,
                'Expected comma, but was "{}"'.format(value), line_number)

            i = i + 1
            tk_type, value = token_list[i]
            check(tk_type == ID, 'Invalid syntax in func header.', line_number)
            check(value not in functions and value not in params,
                'Bad / duplicate param name.', line_number)
            args_count += 1
            params[value] = 0
            param_list.append(value)

            i = i + 1
            tk_type, value = token_list[i]

    check(args_count == functions[func_name],
        'Argument count mismatch. Expected {} arguments (from declaration), but found {}.'
        .format(functions[func_name], args_count), line_number)

    # Should be pointing at the right paren. Now we move to ":"
    i = i + 1
    tk_type, value = token_list[i]
    check(tk_type == OPERATOR and value == COLON,
        'Invalid syntax in func header. Expected ":" but was "{}".'
        .format(value), line_number)

    i = i + 1

    return func_name, param_list, i, line_number

def generate_label(n, line_number):
    return 'COND_{}_{}_ln_{}'.format(randint(0, 1000), n, line_number)