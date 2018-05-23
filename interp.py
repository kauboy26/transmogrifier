from parser import parse
from lexer import tokenize

def lp(stri):
    return parse(tokenize(stri))