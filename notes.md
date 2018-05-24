## Note 1
The 'not' is quickly grabbed and added to the op_stack. This enforces right associativity
and high precendence. I think quickly grabbing it is the only thing needed to enforce the
two, but of course, we still have the problem of misplaced arguments: "a = 5 not;" is treated
the same way as "a = not 5;" although in the first case, the "5" is obviously misplaced.  
The problem of misplaced arguments isn't particular to the 'not' operator, it happens with all
operators. For more information, see [PyEvaluator's Oddities section](https://github.com/kauboy26/PyEvaluator#oddities).
I will try to address this issue if possible in this project.