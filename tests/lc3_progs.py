lsamp1 = '''

main:
    a = 0;
    b = 5;
    i = 0;
    
    while a < b:
        temp = a + 1;
        i = i + temp * temp;
        a = temp;
    end

end
'''

lsamp2 = '''

main:
    i = 10;
    if i * 2 == 10 * 2:
        i = 3;
        i = i + 1;
    elif i == 3:
        i = 2;
    end

    if 8 * 8 <= 64:
        if 1 >= 8:
            i = 30;
        elif i > 2:
            i = (12 + 12) + (1 + 1 - 1 - 1) + 1;
        end
    end

    # i should be 25;
    # Also pay close attention to how much of the stack was occupied.
    # When there are no functions being called, if there are "n" variables,
    # the stack size should be at most n + 1 (max stack size possible).
    # Look at garbage left in the stack to ensure this.
end

'''

lsamp3 = '''

main:
    b = 12;
    a = (12 + 12) + (b + b - b - b) + 1;

    # a should be 25
    # b should be 12
end

'''

lsamp5 = '''

main:
    a = 10;
    b = 20;
    c = 7;
    d = 8;
    e = c & d;
    f = c | d;

    if a + b > b + b and not not b + 20 or (b - b) or not 28:
        b = 30;
    end

end

'''

lsamp4 = '''

main:
    c = 7;
    d = 8;
    e = c & d;
    f = c | d;
    g = (~f) + 1;

end

'''

lsamp6 = '''

main:
    c = 0;
    a = 49;
    b = -7;
    c = a / b;
    d = a / -b;
    e = (a + b) / (a - b);
    f = (a + b) * (a - b);
    # g = a % b;
end

'''

lsamp7 = '''

main:
    a = 10;
    b = 7;
    g = a % b;

    if (a + b) * (a - b) % (a + b - 4) == 13 - 1:
        g = -666;
    end
end

'''

lsamp8 = '''

# declare fib(n);
declare fib2(n);

main:
    a = fib2(10);
end


# def fib(n):
#     if n < 2:
#         return 1;
#     end

#     return fib(n - 1) + fib(n - 2);
# end

def fib2(n):
    if n < 2:
        return 1;
    end

    a0 = 1;
    a1 = 1;
    ans = 0;

    n = n - 1;

    while n:
        ans = a0 + a1;
        a0 = a1;
        a1 = ans;
        n = n - 1;
    end

    return ans;
end
'''

lsamp9 = '''

declare f(a, b, c, d, e);

main:
    a = 1;
    b = 2;
    c = 3;
    d = 4;
    e = 5;

    g = f(a, b, c, d, e);
    h = f(a, a + a, a + b, d, b + c);
    i = f(1, 2, a + a + a, a + a + a + a, 5 - 1 + 1);
end

def f(a, b, c, d, e):
    return 1 * a + 2 * b + 3 * c + 4 * d + 5 * e;
end
'''

lsamp10 = '''

declare is_prime(n);

main:
    a = is_prime(100 + 99 - 100);
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
'''