samp1 = '''
main:
    a = -5 / -5;
    b = a * -a - 89;
    b = -b - b;

    c = not a * b;

    d = 1 * 9 - 9 or 0 and not 1 * 5 < 6 or not not not not a;

    mem(50) = a;
    mem(51) = b;
    mem(52) = c;
    mem(53) = d;

    # assert
    # mem(50) == 1
    # mem(51) == 180
    # mem(52) == 0
    # mem(53) == 1
end
'''

samp2 = '''
main:
    a = 9 - 9 * 11;
    a + 1;
    c = 80;
    b = (a + c ) * (a - c);
    d = a * a - c * c;
    equal = b == d;

    # Assert
    mem(50) = a; # -90
    mem(51) = b; # -1700
    mem(52) = c; # 80
    mem(53) = d; # -1700
    mem(54) = equal; # 1

end
'''




samp3 = '''

declare sum(n);
declare fact(n);
declare thing();

main:
    a = fact(thing() + 2 * -thing() + 3 * thing());

    # Assert
    mem(100) = sum(20); # 210
    mem(101) = a;       # 40320
end

def thing():
    return 4;
end

def sum(n):

    if n > 1:
        return n + sum(n - 1);
    end

    return 1;
end

def fact(n):
    if n > 1:
        return n * fact(n - 1);
    end

    return 1;
end
'''

samp4 = '''

declare f(a, b);

main:
    a = 1 + 1 + 1;
    a = 1;
    a = 1 + 1;
    e = 2;
    e = a + 999;

    a = 1 + 1 + 1;
    b = 30;

    f(a, b);

    if mem(50) == 50:
        i = 1;
    end

    # Assert mem(50) = 50
end

def f(a, b):
    waht = 90 * a * b;
    # basically does mem(50) = 50;
    mem(a + b + 9 * 2 - 1 + mem(102 + mem(21) * 0) * (0) + 0) = 50; 
end
'''


samp5 = '''
declare func1(a, b, c);
declare f(fa);
# declare func2(a, b);

declare is_prime(n);

main:
    # b = f(5);
    # a = func1(1, 2, f(func2(1, b))) * func2(2, 3);
    c = 1;
    c = 2 + 2;
    c = 1;

    mem(38) = 101;

    # assert mem(50) == 1 (101 is prime)
    mem(50) = is_prime(mem(38));
    mem(51) = is_prime(mem(50) * 128); # 0
end

def is_prime(num):

    prime = 1;

    i = 2;

    while i * i < num:

        if num % i == 0:
            prime = 0;
            i = num; # to exit the loop
        end

        i = i + 1;
    end

    return prime;
end

def func1(hello, mr, sky):
    a = hello * mr * sky;
    b = -a;
    c = hello + 1;
    c = c + 1;
    return c;
end

def f(parum):
    parum = parum * 0;
end
'''



samp6 = '''
main:
    mem(10) = 20;
    mem(20) = 10;
    mem(mem(mem(10))) = mem(10) * mem(10);

    # assert mem(10) == 400
end
'''


samp7 = '''
declare f(a, b);
declare fact(n);
declare trial(a, b, c);

main:
    f(1, 2);
end

def f(a, b):
    if a > b:
        if b > 20:
            c = 1;
            return c - a * b;
        end

        return a;
    end

    return b;
end

def fact(n):
    if n > 0:
        return n * fact(n - 1);
    elif n == 0:
        return -1;
    elif n < 0:
        return 1000;
    else:
        return 100000;
    end

    return 1;
end

def trial(a, b, c):
    if a > b:
        if a > c:
            return a * a;
        elif c > a:
            return c * c;
        end
    elif a < b:
        return 1;
    end
end
'''

samp8 = '''
declare fact(n);

main:
    a = 9;
    mem(a) = fact(a - 1) / fact(a - 2) - 8 / 1;

    # Assert mem(9) == 0
end

def fact(n):

    i = n;

    if n > 0:
        i = i + 1;
        return n * fact(n - 1);
    else:
        return 1;
    end

    return 5;
end
'''

samp9 = '''
declare fibo(n);

main:
    a = fibo(9) + fibo(8);
    b = fibo(10);

    if a == b:
        mem(100) = 1;
    else:
        mem(100) = 0;
    end

    # Assert mem(100) == 1
end

def fibo(n):
    g = mem(9);
    k = mem(10);
    l = mem(n + 100);

    if n > 1:
        a = 10;
        return fibo(n - 1) + fibo(n - 2);
    end

    return 1;
end    
'''







samp10 = '''

declare tribo(n);

main:
    a = tribo(20);
    b = tribo(20 - 1) + tribo(20 - 2) + tribo(400 / 20 - 3 + tribo(5) * tribo(6) * tribo(7) * 0);
    b = b + a - a;

    if b - a:
        mem(100) = 999;
    elif 1:
        mem(100) = 0;
    else:
        mem(100) = 8;
    end

    # assert mem(100) == 0
end

def tribo(n):

    if n < 2:
        return 0;
    elif n == 2:
        return 1;
    end

    # Otherwise calculate them through a loop
    a0 = 0;
    a1 = 0;
    a2 = 1;

    ans = 0;

    n = n - 2;

    while n:
        ans = a2 + a1 + a0;

        a0 = a1;
        a1 = a2;
        a2 = ans;

        n = n - 1;
    end

    return ans;

end
'''

samp11 = '''

main:
    i = 5;

    while i < 500:
        mem(i) = 0;
        i = i + 1;
    end

    # Assert mem[5:500] == 0
end

'''

samp12 = '''

main:
    
    i = 5;
    while i < 100:
        mem(i) = i;
        i = i + 1;
    end

    # Assert mem[5:100] are consecutive ints
end

'''


samp13 = '''

main:
    mem(10) = mem(20);

    mem(1 + 1) = 1 + 1;

    i = 0;
    while i < 40:
        mem(i + 20) = 0;
    end
end

'''

samp14 = '''

main:
    a = 100;
    mem(a) = 5;
    while mem(100) < 5 + 20:
        mem(mem(a)) = 0;
        mem(a) = mem(100) + 1;
    end

    # Assert mem[5:25] is 0
end

'''

samp15 = '''

# Bubble sort
declare bsort(start, length);

main:
    start = 20;
    length = 80;

    bsort(start, length);

    # Assert mem[20:100] is sorted
end

def bsort(start, length):
    j = 0;
    i = 0;
    temp = 0;

    while j < length - 1:

        i = 0;
        while i < length - j - 1:
            if mem(start + i) > mem(start + i + 1):
                temp = mem(start + i);
                mem(start + i) = mem(start + i + 1);
                mem(start + i + 1) = temp;
            end

            i = i + 1;
        end

        j = j + 1;
    end
end
'''
11


samp16 = '''

declare swap(a, b);

main:
    a = -1;
    b = 100;

    swap(addrOf(a), addrOf(b));

    mem(50) = a; # 100
    mem(51) = b; # -1
end

define swap(addr1, addr2):
    temp = mem(addr1);
    mem(addr1) = mem(addr2);
    mem(addr2) = temp;
end
'''






samp17 = '''

declare mem_fact(addr_op, addr_val);

main:
    a = 8;
    fact_a = 1;

    mem_fact(addrOf(a), addrOf(fact_a));

    mem(100) = fact_a; # assert 40320
end

def mem_fact(addr_op, addr_val):
    if mem(addr_op) > 1:
        val = mem(addr_val);
        val = val * mem(addr_op);
        mem(addr_val) = val;
        mem(addr_op) = mem(addr_op) - 1;

        mem_fact(addr_op, addr_val);
    end
end

'''

samp18 = '''
declare increment(a);

main:
    a = 1;
    increment(addrOf(a));
end

def increment(a):
    mem(a) = mem(a) + 1;
end
'''


samp19 = '''
declare h(a, b);

main:
    a = 1;
    b = 2;
end

def h(a, b):
    if a > b:
        c = 1;
    end

    c = 2;
end
'''

samp20 = '''

declare len(a);
declare asce(a);

main:
    a = array(10);
    asce(a);
    b = array(len(a) * 2);
    asce(b);

    # Assert that a has consecutive ints within it
    mem(100) = a;

end

def len(a):
    return mem(a - 1);
end

def asce(a):
    i = 0;

    k = array(len(a) * 3);

    while i < len(a):
        mem(a + i) = i;
        i = i + 1;
    end
end

'''

samp21 = '''

declare rando();

main:
    n = 10;

    orig = array(n);

    first_half = array(n / 2);
    sec_half = array(n  - n / 2);
end

def rando():
    cool = array(20);

    i = 0;
    while i < 20:
        mem(cool + i) = array(10);
    end
end

'''

samp22 = '''

declare ms(a);
declare len(a);

main:
    arr = array(100);

    ms(arr);

    mem(150) = arr;

end

def ms(a):

    length = len(a);

    if length < 2:
        return;
    end

    fh = array(length / 2);
    sh = array(length - length / 2);

    i = 0;
    j = 0;


    # there's a lot of unneccessary function calling
    # to ensure that the language works.

    while i < len(fh):
        mem(fh + i) = mem(a + i);
        i = i + 1;
    end

    while j < len(sh):
        mem(sh + j) = mem(a + i + j);
        j = j + 1;
    end 

    ms(fh);
    ms(sh);

    # Now merge them together

    i = 0;
    j = 0;


    while i < len(fh) and j < len(sh):
        if mem(fh + i) <= mem(sh + j):
            mem(a + i + j) = mem(fh + i);
            i = i + 1;
        else:
            mem(a + i + j) = mem(sh + j);
            j = j + 1;
        end
    end

    while i < len(fh):
        mem(a + i + j) = mem(fh + i);
        i = i + 1;
    end

    while j < len(sh):
        mem(a + i + j) = mem(sh + j);
        j = j + 1;
    end

end

def len(a):
    return mem(a - 1);
end

'''

samp23 = '''

declare is_palin(a);


main:
    a = "abcdefghijklmnop";
    mal = "malayalam";
    b = is_palin(a);
    c = is_palin(mal);

    # assert
    mem(20) = b; # 0
    mem(21) = c; # 1
end

def is_palin(a):

    length = mem(a - 1) - 1;
    i = 0;
    j = length - 1;

    while i < j and mem(a + i) == mem(a + j):
        i = i + 1;
        j = j - 1;
    end

    if i < j:
        return 0;
    end

    return 1;

end

'''

samp24 = '''

main:
    b = array(51);

    i = 0;
    while i < 50:
        mem(b + i) = getc();
        i = i + 1;
    end

    mem(b + 50) = 0;

    a = "you have entered: ";
    print(a);
    print(b);
end
'''

samp25 = '''
macro  xx 25;
macro zz 40;

declare xx(a);

main:
    a = xx + zz;
end
'''

samp26 = '''


main:
    arr = 0;
    mem(addrOf(arr)) = array(20);


    i = 0;
    b = 100;

    # mem(100) = arr;
    mem(b * 2 / 2) = arr;

    while i < mem(arr - 1):
        mem(arr + i) = i;
        i = i + 1;
    end
end

'''

samp27 = '''

main:
    # 14 characters long including NULL
    a = "hello, world!";
    b = "goooood!";
end

'''

tooheavy = '''
# Bootstrapping my friend

declare eval(str);

main:
    # The string to evaluate
    # Make sure it is valid, has only '+' and '*',
    # and it ends with a semicolon.

    msg = "Type in an expression with only '+' and '*'.\\nMake sure it is valid\\n";
    prompt = "\\n>>\\t";
    output = "\\nThe result is: ";
    
    print(msg);
    

    str = array(92);
    done = 0;

    
    while not done:
        print(prompt);
        i = 0;

        c = getc();
        while not (c == ';' or c == 'q') and i < 90:
            mem(str + i) = c;
            i = i + 1;
            c = getc();
        end

        if not c == 'q':
            mem(str + i) = ';';
            mem(str + i + 1) = 0;

            a = eval(str);

            # Now to display that.
            print(output);

            i = 10000;
            div = 0;

            while i:
                div = a / i;
                outc(div + '0');
                a = a - div * i;
                i = i / 10;
            end
        else:
            done = 1;
        end
    
    end
end


def eval(str):
    # Create two stacks, one for operands and one for operation
    num_stack = array(10);
    op_stack = array(10);

    # pointers to the top of the stack
    ntop = -1;
    otop = -1;

    # to store all the parsed elements
    sl = -1;
    tokens = array(15);

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
        elif c == '+':
            sl = sl + 1;
            mem(tokens + sl) = -2;
            i = i + 1;
        elif c == '*':
            sl = sl + 1;
            mem(tokens + sl) = -1;
            i = i + 1;
        elif c == ';':
            sl = sl + 1;
            mem(tokens + sl) = -3;
            i = i + 1;
        else:
            # eat up other characters
            i = i + 1;
        end

        c = mem(str + i);
    end


    # at this point, all tokens loaded

    i = 0;
    res = 0;

    while i <= sl:
        curr = mem(tokens + i);

        if curr >= 0:
            # it's a number
            ntop = ntop + 1;
            mem(num_stack + ntop) = curr;
        else:

            while otop >= 0 and curr <= mem(op_stack + otop):

                operation = mem(op_stack + otop);
                otop = otop - 1;

                num1 = mem(num_stack + ntop);
                num2 = mem(num_stack + ntop - 1);

                ntop = ntop - 1;

                if operation == -1:
                    mem(num_stack + ntop) = num1 * num2;
                else:
                    mem(num_stack + ntop) = num1 + num2;
                end
            end

            otop = otop + 1;
            mem(op_stack + otop) = curr;
        end

        i = i + 1;
    end


    return mem(num_stack + ntop);

end
'''

samps = [   samp1, samp2, samp3, samp4, samp5, samp6,\
            samp7, samp8, samp9, samp10, samp11, samp12,\
            samp13, samp14, samp15]