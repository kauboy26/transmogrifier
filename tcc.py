"""
Transmogrifier, the Chummy Compiler (haha good one)
"""

import sys

from lexer import tokenize
from parser import parse

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage:\npython3 transmogrifier.py filename')
        exit(0)

    with open(sys.argv[-1], 'r') as filename:
        content = filename.read()
        token_list = tokenize(content)

        for token in token_list:
            print(token)

        ir_form = parse(token_list)

        for statement in ir_form:
            print(statement)