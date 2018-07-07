"""
These functions help with lexical analysis. I've tried to do as much work
as possible over here before stuff is passed over to the parser. The
"tokenize" method will tokenize a string, for consumption by the parser.
"""

from core.miscell import check

keywords = {'def': 0, 'if': 0, 'elif': 0,
        'else': 0, 'while': 0, 'end': 0,
        'main': 0, 'return': 0, 'declare': 0,
        'define': 0}

multichar_ops = {'mem': 0, 'addrOf': 0, 'array': 0,
                'inject': 0, 'print': 0, 'and': 0, 'or': 0, 'not': 0}

NUMBER = 0
KEYWORD = 1
OPERATOR = 2
ID = 3
STRING = 4
NEWLINE = 5
COMMENT = 6

def is_numeric(c):
    return c >= '0' and c <= '9'

def is_alpha(c):
    # I'm including underscore as a letter
    return (c >= 'A' and c <= 'Z') or\
        (c >= 'a' and c <= 'z') or\
        c == '_'

def is_alphanumeric(c):
    return (c >= 'A' and c <= 'Z') or\
        (c >= 'a' and c <= 'z') or\
        (c >= '0' and c <= '9') or\
        c == '_'

def is_special(c):
    # Maybe I should use a hashmap or something, but whatever.
    return c == '*' or c == '/' or\
        c == '+' or c == '-' or\
        c == '(' or c == ')' or\
        c == '=' or c == ',' or\
        c == '&' or c == '|' or\
        c == '~' or c == '%' or\
        c == ';' or c == ':' or\
        c == '[' or c == ']' or\
        c == '<' or c == '>' or\
        c == '"' or c == '\'' or\
        c == '#'

def tokenize(in_str):
    """
    Tokenize the given string, with some checks. The returned token list will be of
    the format [(TYPE, VALUE), ...].
    """

    token_list = []
    line_number = 1

    if not in_str:
        return token_list

    length = len(in_str)

    i = 0
    while i < length:
        if is_numeric(in_str[i]):
            # It is a number, grab the entire number. NO floats allowed.
            num = 0
            while i < length and is_numeric(in_str[i]):
                num = num * 10 + int(in_str[i])
                i = i + 1

            token_list.append((NUMBER, num))
        
        elif is_alpha(in_str[i]):
            # Requires variables to start with a letter or underscore.
            start_index = i
            while i < length and is_alphanumeric(in_str[i]):
                i = i + 1
            
            val = in_str[start_index:i]
            if val in keywords:
                token_list.append((KEYWORD, val))
            elif val in multichar_ops:
                token_list.append((OPERATOR, val))
            else:
                token_list.append((ID, val))

        elif is_special(in_str[i]):

            start_index = i
            if in_str[i] == '"':
                # Capture the entire string
                i = i + 1
                while i < length and in_str[i] != '"' and in_str[i] != '\n':
                    # Screw escape characters
                    i = i + 1
                check(i < length and in_str != '\n', 'Incomplete string: "{}"'
                    .format(in_str[start_index:i]), line_number)
                token_list.append((STRING, in_str[start_index + 1:i]))
                i = i + 1
            elif in_str[i] == '\'':
                i = i + 1
                check(i < length and in_str[i] != '\n', 'Bad character formatting', line_number)
                i = i + 1
                check(i < length and in_str[i] == '\'', 'Lone " \' "', line_number)
                token_list.append((NUMBER, ord(in_str[i - 1])))
                i = i + 1  
            elif in_str[i] == '#':
                # capture the entire comment, which ends at the new line character.
                i = i + 1
                start_index = i
                while i < length and in_str[i] != '\n':
                    i = i + 1
                # Now pointing at either a newline or we've gone past.
                if start_index != length:
                    token_list.append((COMMENT, in_str[start_index:i]))
                    # The thing will be left pointing to a newline char, which will be picked up later.         
            else:
                c = in_str[i]
                if (c == '<' or c == '>' or c == '=')\
                    and i + 1 < length and in_str[i + 1] == '=':
                    token_list.append((OPERATOR, in_str[i:i + 2]))
                    i = i + 1
                else:
                    token_list.append((OPERATOR, c))
                i = i + 1
        else:
            if in_str[i] == '\n':
                token_list.append((NEWLINE, None))
                line_number = line_number + 1
            i = i + 1

    return token_list