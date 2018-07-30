"""
Transmogrifier, the Chummy Compiler (haha good one)
"""

import sys

from core.lexer import tokenize
from core.parser import parse
from core.lc3_converter import LC3Converter
from core.lc3_printer import gen_asm

import os.path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage:\npython3 transmogrifier.py filename')
        exit(0)

    content = ''
    
    with open(sys.argv[-1], 'r') as filename:
        content = filename.read()

    basename, ext = os.path.splitext(sys.argv[-1])

    tokens = tokenize(content)
    ir_form, labels, ln_to_label, func_help = parse(tokens)

    lc3_converter = LC3Converter(ir_form, labels, ln_to_label, func_help)
    tree, table, str_table = lc3_converter.convert()

    output = gen_asm(tree, table, str_table)

    asm_file = basename + '.asm'


    with open(asm_file, 'w+') as af:
        af.write(output)