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
    a = (12 + 12) + (1 + 1 - 1 - 1) + 1;
end

'''