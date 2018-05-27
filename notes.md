# Notes
## Note 1
The 'not' is quickly grabbed and added to the op_stack. This enforces right associativity
and high precendence. I think quickly grabbing it is the only thing needed to enforce the
two, but of course, we still have the problem of misplaced arguments: "a = 5 not;" is treated
the same way as "a = not 5;" although in the first case, the "5" is obviously misplaced.  
The problem of misplaced arguments isn't particular to the 'not' operator, it happens with all
operators. For more information, see [PyEvaluator's Oddities section](https://github.com/kauboy26/PyEvaluator#oddities).
I will try to address this issue if possible in this project.

## Note 2
```
if num_stack:
    num_stack.pop()
    ir_form.append(statement)
statement = []
```  
Before the execution of this code, the num_stack is guaranteed to have 0 or 1 items within it. If it has 0 items, then that means
the statement that was executed was an empty statement, i.e, it was a ";". This is because every operation ("+", "=", "-", function
calls, etc) will all push a value on to num_stack. It is not possible to do anything without a value not being pushed on to the number stack. Therefore, in this code, we empty the num_stack when it is not empty (a single pop() will do), and append the statement generated to the overall form. Regardless, the statement is cleaned out for the next iteration.  
The reasoning behind separating ir_form and statement was to avoid unnecessary pushes to the stack that may occur during the
code generation phase. The last operation in each statement does not require a push to the stack.

## Note 3
The assignment operation and creating variables together are screwing the stack up. A single assignment operation per statement is
now being enforced.

# Other issues

* Tried to execute "a = (1 +;", instead of getting "not enough operands" or "missing paren" message, got the variable "a" is not defined. This is because the stack does not care about the actual positions of operands, and so in the popping process the "a" and "1" are popped to be added, but "a" obviously hasn't been defined yet.
* TODO solve newline problem (newlines are encounterd in func decl.). Right now I expect a linear deterministic format.
* Two assignment operations in one statement, where both assignments require the creation of a variable should be made illegal. I am having problems resolving what the stack should look like then. EDIT: I have done something to somewhat fix that. However, the compiler still lets this go through: "1 * 8 + (b = 10);". This will break it.
* This needs to fail: 'declare a(a); declare b();\ndeclare c(a, b, c);\na = c(b(1), b(1), 0);'. The way I am counting arguments isn't right, need to think of something better. Currently there is a test for it, that passes. However, the test is passing for the wrong reason. TODO IMPORTANT
* I'm not able to trace how the program came up with the ir_form it did for this: "declare a(a); declare b(); i = a(1 + b() + -b() * -b());"