import unittest
from interp import lp

class MyTestCase(unittest.TestCase):
    def test_simp1(self):
        self.assertRaises(SyntaxError, lp, 'a = 1; b = b + 1;')
    def test_simp2(self):
        self.assertRaises(SyntaxError, lp, 'a = 1')
    def test_simp3(self):
        self.assertRaises(SyntaxError, lp, 'd = 9 * 9 -;')
    def test_simp4(self):
        self.assertRaises(SyntaxError, lp, '1 + (a = 1);')
    def test_simp5(self):
        self.assertRaises(SyntaxError, lp, 'b = not not 2 > 5; a = b + 1; c = (a - 1) * not(b - 2);;;;; # Comments buddy\n g = 1; g= 0 * 0 * 0 -- 4;'
        '; c - 4; b = g > > 4;')

    # When there is a malformed function declaration:
    def test_funcdecl1(self):
        self.assertRaises(SyntaxError, lp, 'declare fno_comma(a b);')
    def test_funcdecl2(self):
        self.assertRaises(SyntaxError, lp, 'declare misplaced_semi;()')
    def test_funcdecl3(self):
        self.assertRaises(SyntaxError, lp, 'declare two_commas(a,,b);')
    def test_funcdecl4(self):
        self.assertRaises(SyntaxError, lp, 'declare value_at(a,,b);')
    def test_funcdecl5(self):
        self.assertRaises(SyntaxError, lp, 'declare value_at(a,,b);')
    def test_funcdecl6(self):
        self.assertRaises(SyntaxError, lp, 'declare block(g);')
    def test_funcdecl7(self):
        self.assertRaises(SyntaxError, lp, 'declare hello(g); declare hello(g);')
    def test_funcdecl8(self):
        self.assertRaises(SyntaxError, lp, 'declare hello(g,);')


if __name__ == '__main__':
    assert(lp('a = -1;') == [([(0, 1), (0, -1)], '*'), ((3, 'a'), '__create__'), ([(8, '$'), (3, 'a')], '='), (None, '__pop__')])
    assert(lp('a = 9; b = 20;declare f(a); declare g();') == [((3, 'a'), '__create__'), ([(0, 9), (3, 'a')], '='), (None, '__pop__'), ((3, 'b'), '__create__'), ([(0, 20), (3, 'b')], '='), (None, '__pop__')])
    assert(lp('a = -0;') == [([(0, 0), (0, -1)], '*'), ((3, 'a'), '__create__'), ([(8, '$'), (3, 'a')], '='), (None, '__pop__')])
    assert(lp('a = - (8 * 9);') == [([(0, 9), (0, 8)], '*'), ([(8, '$'), (0, -1)], '*'), ((3, 'a'), '__create__'), ([(8, '$'), (3, 'a')], '='), (None, '__pop__')])
    assert(lp('a = - (9);') == [([(0, 9), (0, -1)], '*'), ((3, 'a'), '__create__'), ([(8, '$'), (3, 'a')], '='), (None, '__pop__')])
    assert(lp(';d = -(1 * 1);') == [([(0, 1), (0, 1)], '*'), ([(8, '$'), (0, -1)], '*'), ((3, 'd'), '__create__'), ([(8, '$'), (3, 'd')], '='), (None, '__pop__')])
    assert(lp('a = 1;d = -(1 * 1);') == [((3, 'a'), '__create__'), ([(0, 1), (3, 'a')], '='), (None, '__pop__'), ([(0, 1), (0, 1)], '*'), ([(8, '$'), (0, -1)], '*'), ((3, 'd'), '__create__'), ([(8, '$'), (3, 'd')], '='), (None, '__pop__')])
    assert(lp('a = 1; b= a + 234;; d = -(1 * 1);') == [((3, 'a'), '__create__'), ([(0, 1), (3, 'a')], '='), (None, '__pop__'), ([(0, 234), (3, 'a')], '+'), ((3, 'b'), '__create__'), ([(8, '$'), (3, 'b')], '='), (None, '__pop__'), ([(0, 1), (0, 1)], '*'), ([(8, '$'), (0, -1)], '*'), ((3, 'd'), '__create__'), ([(8, '$'), (3, 'd')], '='), (None, '__pop__')])
    assert(lp('a = 1; b= a + 234;; d = -(a * b);') == [((3, 'a'), '__create__'), ([(0, 1), (3, 'a')], '='), (None, '__pop__'), ([(0, 234), (3, 'a')], '+'), ((3, 'b'), '__create__'), ([(8, '$'), (3, 'b')], '='), (None, '__pop__'), ([(3, 'b'), (3, 'a')], '*'), ([(8, '$'), (0, -1)], '*'), ((3, 'd'), '__create__'), ([(8, '$'), (3, 'd')], '='), (None, '__pop__')])
    assert(lp('a = 1; b = a + 234; c = 0; 9 + 8; 45 + c; d = -(a * b);') == [((3, 'a'), '__create__'), ([(0, 1), (3, 'a')], '='), (None, '__pop__'), ([(0, 234), (3, 'a')], '+'), ((3, 'b'), '__create__'), ([(8, '$'), (3, 'b')], '='), (None, '__pop__'), ((3, 'c'), '__create__'), ([(0, 0), (3, 'c')], '='), (None, '__pop__'), ([(0, 8), (0, 9)], '+'), (None, '__pop__'), ([(3, 'c'), (0, 45)], '+'), (None, '__pop__'), ([(3, 'b'), (3, 'a')], '*'), ([(8, '$'), (0, -1)], '*'), ((3, 'd'), '__create__'), ([(8, '$'), (3, 'd')], '='), (None, '__pop__')])

    print('Some function declaration crap:')
    assert(lp('declare fuc(a, b);') == [])
    assert(lp('declare fuc(a);') == [])
    assert(lp('declare fuc();') == [])

    unittest.main()

    print("\n********************************\nAll tests passed!")