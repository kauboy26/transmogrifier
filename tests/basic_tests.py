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

from machines.ir_machine1 import IRMachine1

from tests import some_programs as sp


import unittest


class BasicArithmeticMainMemUnittests(unittest.TestCase):
    """
    Tests that don't have any function calls. Just some basic
    arithmetic stuff and memory operations to tests the same.
    """

    def test_basicMath(self):

        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp1))
        machine.run(instructions, labels, inv_lbl, func_help)

        self.assertEqual(machine.memory[50], 1)
        self.assertEqual(machine.memory[51], 180)
        self.assertEqual(machine.memory[52], 0)
        self.assertEqual(machine.memory[53], 1)

        self.assertEqual(machine.sp, -1)

    def test_basicMath2(self):

        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp2))
        machine.run(instructions, labels, inv_lbl, func_help)

        self.assertEqual(machine.memory[50], -90)
        self.assertEqual(machine.memory[51], 1700)
        self.assertEqual(machine.memory[52], 80)
        self.assertEqual(machine.memory[53], 1700)
        self.assertEqual(machine.memory[54], 1)

        self.assertEqual(machine.sp, -1)


    def test_nestedMemCalls(self):
        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp6))
        machine.run(instructions, labels, inv_lbl, func_help)

        self.assertEqual(machine.memory[10], 400)

        self.assertEqual(machine.sp, -1)

class EasyFunctionCallsUnittests(unittest.TestCase):

    def test_noAssignmentInFunctionsRecursive(self):

        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp3))
        machine.run(instructions, labels, inv_lbl, func_help)

        self.assertEqual(machine.memory[100], 210)
        self.assertEqual(machine.memory[101], 40320)

        self.assertEqual(machine.sp, -1)

    def test_assignmentSingleFunctionCallNestedMem(self):

        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp4))
        machine.run(instructions, labels, inv_lbl, func_help)

        self.assertEqual(machine.memory[50], 50)

        self.assertEqual(machine.sp, -1)


class ConditionInOtherFunctionUnittests(unittest.TestCase):

    def test_bullshitFunctionCallsIsPrime(self):

        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp5))
        machine.run(instructions, labels, inv_lbl, func_help)

        self.assertEqual(machine.memory[50], 1)
        self.assertEqual(machine.memory[51], 0)

        self.assertEqual(machine.sp, -1)


    def test_moreRecursiveFunctions(self):

        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp8))
        machine.run(instructions, labels, inv_lbl, func_help)

        self.assertEqual(machine.memory[9], 0)

        self.assertEqual(machine.sp, -1)


    def test_moreRecursiveFunctionsWithFiller(self):

        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp9))
        machine.run(instructions, labels, inv_lbl, func_help)

        self.assertEqual(machine.memory[100], 1)

        self.assertEqual(machine.sp, -1)


    def test_moreCondsInFunctions(self):

        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp10))
        machine.run(instructions, labels, inv_lbl, func_help)

        self.assertEqual(machine.memory[100], 0)

        self.assertEqual(machine.sp, -1)

class MassMemoryOpsUnittests(unittest.TestCase):

    def test_wipeMemory(self):

        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp11))
        machine.run(instructions, labels, inv_lbl, func_help)

        for i in range(5, 500):
            self.assertEqual(machine.memory[i], 0)

        self.assertEqual(machine.sp, -1)

    def test_incrementedMemory(self):

        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp12))
        machine.run(instructions, labels, inv_lbl, func_help)

        for i in range(5, 100):
            self.assertEqual(machine.memory[i], i)

        self.assertEqual(machine.sp, -1)

    def tests_memoryAccessWithVariable(self):
        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp14))
        machine.run(instructions, labels, inv_lbl, func_help)

        for i in range(5, 25):
            self.assertEqual(machine.memory[i], 0)

        self.assertEqual(machine.sp, -1)

    def tests_memorySorted(self):
        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp15))
        machine.run(instructions, labels, inv_lbl, func_help)

        for i in range(20, 99):
            self.assertTrue(machine.memory[i] < machine.memory[i + 1], 'Mem loc: {}'.format(i))

        self.assertEqual(machine.sp, -1)


class AddressOfSimpleUnittests(unittest.TestCase):


    def test_incrementVariable(self):

        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp18))
        machine.run(instructions, labels, inv_lbl, func_help)

        self.assertEqual(machine.memory[0], 2)

    def test_swap(self):

        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp16))
        machine.run(instructions, labels, inv_lbl, func_help)

        self.assertEqual(machine.memory[50], 100)
        self.assertEqual(machine.memory[51], -1)

    def test_memFactorial(self):

        machine = IRMachine1()

        instructions, labels, inv_lbl, func_help = parse(tokenize(sp.samp17))
        machine.run(instructions, labels, inv_lbl, func_help)

        self.assertEqual(machine.memory[100], 40320)

if __name__ == '__main__':
    unittest.main()