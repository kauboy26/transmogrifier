from interp import lp

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


print("\n********************************\nAll tests passed!")