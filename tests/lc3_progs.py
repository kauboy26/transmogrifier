lsamp_th = '''

declare eval(str, vars, evars);
declare is_alpha(c);
declare index(a, b);
declare prec(c);
declare  do_op(n1, n2, op);
declare print_num(a);



macro NUM_VARS  199;
macro ID    0;
macro NUMBER 1;
macro OPER  2;



main:
    # The string to evaluate
    # Make sure it is valid, has only '+' and '*',
    # and it ends with a semicolon.

    init_msg = "Not Python 3.5.2 (default, Jul 31 2018, 12:52:01)\\n[tranny 5.4.0 20160609] on lc3\\n";
    prompt = "\\n>>> ";
    
    print(init_msg);
    
    buffer = array(100);
    vars = array(NUM_VARS);
    evars = array(NUM_VARS);

    done = 0;

    i = 0;
    while i < NUM_VARS:
        mem(vars + i) = 0;
        mem(evars + i) = 0;
        i = i + 1;
    end
    
    while not done:
        print(prompt);
        i = 0;

        c = getc();
        outc(c);

        while not (c == '\\n' or c == ';') and i < 95:
            mem(buffer + i) = c;
            i = i + 1;
            c = getc();
            outc(c);
        end

        outc('\\n');

        if not c == ';':
            mem(buffer + i) = ';';
            mem(buffer + i + 1) = 0;

            eval(buffer, vars, evars);

        else:
            done = 1;
        end
    end
end

def index(str, l):
    # Finds where a variable should sit by finding the Rabin Karp hash
    # and then modding it.

    hash = 0;
    i = 0;

    while i < l:
        c = mem(str + i);
        hash = hash * 17 + c;
        i = i + 1;
    end

    return hash % 199;

end


def eval(str, vars, evars):
    # Create two stacks, one for operands and one for operation
    num_stack = array(20);
    type_stack = array(20);
    op_stack = array(20);

    # pointers to the top of the stack
    ntop = -1;
    otop = -1;

    # to store all the parsed elements
    sl = -1;
    tokens = array(100);
    token_types = array(100);

    i = 0;

    c = mem(str + i);

    while c:
        if c >= '0' and c <= '9':
            # found a number, capture the whole thing.
            num = c - '0';

            i = i + 1;
            c = mem(str + i);
            while c >= '0' and c <= '9':
                num = num * 10 + (c - '0');
                i = i + 1;
                c = mem(str + i);
            end

            # "i" should now be pointing to a non-numeric character
            # the number is loaded into "num"

            sl = sl + 1;
            mem(tokens + sl) = num;
            mem(token_types + sl) = NUMBER;

        elif prec(c) < 0:

            a = "pdd called!";
            print_num(prec(c));
            print(a);
            outc(c);
            print(a);

            sl = sl + 1;
            mem(tokens + sl) = c;
            mem(token_types + sl) = prec(c);
            i = i + 1;

        elif (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):

            a = "other thing called";
            print(a);

            start = i;

            while is_alpha(c):
                i = i + 1;
                c = mem(str + i);
            end

            sl = sl + 1;
            mem(tokens + sl) = 0;
            mem(token_types + sl) = ID;

        

        else:
            # eat up other characters
            i = i + 1;
        end

        c = mem(str + i);
    end


    # at this point, all tokens loaded

    i = 0;

    while i <= sl:
        curr = mem(tokens + i);
        type = mem(token_types + i);

        if type == NUMBER:
            ntop = ntop + 1;
            mem(num_stack + ntop) = curr;
            mem(type_stack + ntop) = NUMBER;
        elif type < 0:
            # An operator
            while otop >= 0 and prec(curr) <= prec(mem(op_stack + otop)):

                operation = mem(op_stack + otop);
                otop = otop - 1;

                num2 = mem(num_stack + ntop);
                num1 = mem(num_stack + ntop - 1);

                ntop = ntop - 1;

                temp = 0;

                if operation == '=':
                else:
                    temp = do_op(num1, num2, operation);
                end

                mem(num_stack + ntop) = temp;
                mem(type_stack + ntop) = NUMBER;

            end

            otop = otop + 1;
            mem(op_stack + otop) = curr;
        end

        i = i + 1;
    end


    result = mem(num_stack + ntop);
    print_num(result);

end

def prec(a):
    if a == '*' or a == '/' or a == '%':
        return -10;
    elif a == '+' or a == '-':
        return -20;
    elif a == ')' or a == ';':
        return -50;
    elif a == '(':
        return -1;
    end

    return 99;
end

def is_alpha(n):
    return n >= 'a' and n <= 'z' or n >= 'A' and n <= 'Z' or n >= '0' and n <= '9'; 
end

def do_op(n1, n2, op):
    if op == '*':
        return n1 * n2;
    elif op == '/':
        return n1 / n2;
    elif op == '%':
        return n1 % n2;
    elif op == '+':
        return n1 + n2;
    elif op == '-':
        return n1 - n2;
    end
end

def print_num(n):
    a = 10000;
    dig = 0;

    if n < 0:
        outc('-');
        n = -n;
    end

    

    while a:
        dig = n / a;
        n = n % a;
        a = a / 10;
        outc(dig + '0');
    end
end

'''