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
    b = 12;
    c = a / b;
    c = a / -b;
end

'''