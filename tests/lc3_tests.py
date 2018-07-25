"""
I'll enter some real tests in here later, after the compiler reaches an acceptable stage.
For now, I'm screwing around, so the other basic_tests file in the parent directory is in
use.
"""
import sys
# What a ridiculous way of importing things
sys.path.insert(0, '..')


from core.parser import parse
from core.lexer import tokenize
from core.lc3_converter import LC3Converter

from machines.lc3_machine import LC3Machine as Machine

from tests import some_programs as sp


import unittest

SP = 6

def flatten(tree):

    pure = []

    for parent, generated in tree:
        pure += generated

    return pure


class BasicArithmeticMainMemUnittests(unittest.TestCase):
    """
    Tests that don't have any function calls. Just some basic
    arithmetic stuff and memory operations to tests the same.
    """

    def test_basicMath(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp1))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)

        machine = Machine()

        machine.run(pure, table)

        self.assertEqual(machine.memory[50], 1)
        self.assertEqual(machine.memory[51], 180)
        self.assertEqual(machine.memory[52], 0)
        self.assertEqual(machine.memory[53], 1)

        self.assertEqual(machine.registers[SP], 0xF000)

    def test_basicMath2(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp2))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)

        machine = Machine()

        machine.run(pure, table)

        self.assertEqual(machine.memory[50], -90)
        self.assertEqual(machine.memory[51], 1700)
        self.assertEqual(machine.memory[52], 80)
        self.assertEqual(machine.memory[53], 1700)
        self.assertEqual(machine.memory[54], 1)

        self.assertEqual(machine.registers[SP], 0xF000)


    def test_nestedMemCalls(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp6))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)

        machine = Machine()

        machine.run(pure, table)

        self.assertEqual(machine.memory[10], 400)

        self.assertEqual(machine.registers[SP], 0xF000)

class EasyFunctionCallsUnittests(unittest.TestCase):

    def test_noAssignmentInFunctionsRecursive(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp3))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)

        machine = Machine()

        machine.run(pure, table)

        self.assertEqual(machine.memory[100], 210)
        self.assertEqual(machine.memory[101], 40320)

        self.assertEqual(machine.registers[SP], 0xF000)

    def test_assignmentSingleFunctionCallNestedMem(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp4))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)

        machine = Machine()
        machine.run(pure, table)

        self.assertEqual(machine.memory[50], 50)

        self.assertEqual(machine.registers[SP], 0xF000)


class ConditionInOtherFunctionUnittests(unittest.TestCase):

    def test_bullshitFunctionCallsIsPrime(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp5))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table)

        self.assertEqual(machine.memory[50], 1)
        self.assertEqual(machine.memory[51], 0)

        self.assertEqual(machine.registers[SP], 0xF000)


    def test_moreRecursiveFunctions(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp8))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table)

        self.assertEqual(machine.memory[9], 0)

        self.assertEqual(machine.registers[SP], 0xF000)


    def test_moreRecursiveFunctionsWithFiller(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp9))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table)

        self.assertEqual(machine.memory[100], 1)

        self.assertEqual(machine.registers[SP], 0xF000)


    def test_moreCondsInFunctions(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp10))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table)

        self.assertEqual(machine.memory[100], 0)

        self.assertEqual(machine.registers[SP], 0xF000)

class MassMemoryOpsUnittests(unittest.TestCase):

    def test_wipeMemory(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp11))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table)

        for i in range(5, 500):
            self.assertEqual(machine.memory[i], 0)

        self.assertEqual(machine.registers[SP], 0xF000)

    def test_incrementedMemory(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp12))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table)

        for i in range(5, 100):
            self.assertEqual(machine.memory[i], i)

        self.assertEqual(machine.registers[SP], 0xF000)

    def tests_memoryAccessWithVariable(self):
        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp14))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table)

        for i in range(5, 25):
            self.assertEqual(machine.memory[i], 0, i)

        self.assertEqual(machine.registers[SP], 0xF000)

    def tests_memorySorted(self):
        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp15))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table)

        for i in range(20, 99):
            self.assertTrue(machine.memory[i] <= machine.memory[i + 1], 'Mem loc: {}'.format(i))

        self.assertEqual(machine.registers[SP], 0xF000)


class AddressOfSimpleUnittests(unittest.TestCase):


    def test_incrementVariable(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp18))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table)


        self.assertEqual(machine.memory[machine.registers[SP] - 1], 2)
        self.assertEqual(machine.registers[SP], 0xF000)

    def test_swap(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp16))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table)

        self.assertEqual(machine.memory[50], 100)
        self.assertEqual(machine.memory[51], -1)

        self.assertEqual(machine.registers[SP], 0xF000)

    def test_memFactorial(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp17))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table)

        self.assertEqual(machine.memory[100], 40320)

        self.assertEqual(machine.registers[SP], 0xF000)

class ArraySimpleTests(unittest.TestCase):

    def test_makeAscending(self):
        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp20))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table)

        ptr_a = machine.memory[100]

        self.assertEqual(machine.memory[ptr_a - 1], 10)

        for i in range(10):
            self.assertEqual(machine.memory[ptr_a + i], i)

    def test_mergeSort(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp22))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table)

        arr = machine.memory[150]

        # machine.print_memory(0, 120)
        self.assertEqual(machine.memory[arr - 1], 100)

        for i in range(0, 99):
            self.assertTrue(machine.memory[arr + i] <= machine.memory[arr + i + 1],
                'Mem loc: {}, seed: {}'.format(arr + i, machine.seed))

        self.assertEqual(machine.registers[SP], 0xF000)

    def test_memArrAssign(self):
        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp26))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table)

        arr = machine.memory[100]

        # machine.print_memory(0, 120)
        self.assertEqual(machine.memory[arr - 1], 20)

        for i in range(0, 20):
            self.assertTrue(machine.memory[arr + i] == i, i)


    def test_palinString(self):

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp23))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table, str_table)

        self.assertEqual(machine.memory[20], 0)
        self.assertEqual(machine.memory[21], 1)

    def test_memString2D(self):
        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp28))
        lc3_conv = LC3Converter(instructions, labels, inv_lbl, func_help)

        tree, table, str_table = lc3_conv.convert()
        pure = flatten(tree)
        
        machine = Machine()
        machine.run(pure, table, str_table)

        for i in range(5):
            if i % 2 == 0:
                for j in range(5):
                    self.assertEqual(machine.memory[5 + i * 5 + j], ord('a'))
            else:
                for j in range(5):
                    self.assertEqual(machine.memory[5 + i * 5 + j], ord('t'))




if __name__ == '__main__':
    unittest.main()