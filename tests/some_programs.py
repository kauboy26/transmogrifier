samp1 = '''
main:
    a = 1;
    b = a * -a - 89;
    b = -b - b;

    # Assert these:
    mem(50) = a;
    mem(51) = b;
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
    mem(50) = a;
    mem(51) = b;
    mem(52) = c;
    mem(53) = d;
    mem(54) = equal;

end
'''




samp4 = '''

declare sum(n);
declare fact(n);

main:
    a = fact(12);

    # Assert
    mem(100) = sum(20);
    mem(101) = a;
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

samp5 = '''

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
    # basically does mem(50) = 50;
    mem(a + b + 9 * 2 - 1 + mem(102 + mem(21) * 0) * (0) + 0) = 50; 
end
'''





samp3 = '''
declare func1(a, b, c);
declare f(fa);
declare func2(a, b);

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
end

def is_prime(num):

    prime = 1;

    i = 2;
    while i * i < num:
        if num %% i == 0:
            prime = 0;
            i = num; # to exit the loop
        end

        i = i + 1
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
    if n > 0:
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
    fibo(20);
end

def fibo(n):
    if n > 2:
        return fibo(n - 1) + fibo(n - 2) + fibo(n - 3);
    elif n == 2:
        return 1;
    else:
        return 0;
    end
end    
'''







samp10 = '''

declare tribo(n);

main:
    a = tribo(20);
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
    mem(22) = 666;
    mem(23) = 666;
end

'''

samp12 = '''

main:
    mem(10) = 5;
    mem(mem(10)) = 666;
    mem(mem(mem(10))) = 1000;
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
end

'''

samp15 = '''

# Bubble sort

main:
    start = 10;
    length = 200;

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