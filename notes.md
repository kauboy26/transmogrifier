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

## Note 4
When processing "if" statement bodies, variables may be created for that block, and may be destroyed later as we leave that block. In order to keep track of which variables were created and need to be destroyed in a certain block, the vars_this_block stack will be used. As each "end" is encountered, variables that were last created will be destroyed.  
The curr_scope_type is to keep track of the innermost scope we're in (are we in "if", "while", "def", "main", etc?). This is used to resolve what the keyword "end" needs to do, since its meaning changes depending on the scope type. For example, an "end" encountered when the scope type is an "if" statement means we need to delete some variables, but an "end" encountered when the scope type is "def" means we need to generate code to clean-up the stack and return to the caller.

## Note 5 -- OUTDATED
The meaning of CREATE:  
CREATE, to the IRMachine, means if the second operand is not the stack top ($): claim space for the new variable, and set the value to whavever it should be. If the second oeprand is the top of the stack: claim space (by eating up the top of the stack) and mark this assign this space to the new variable.  
Also EQUAL will EAT THINGS from the stack!

## Note 6
If stacktop, then something was pushed on to the stack as a result of an operation. Otherwise a statement like "4;" was encountered, and nothing needs to be done.

## Note 7
The RETURN keyword does two different things depending on the second operand; if the second operand is the stack top ($), then the IRMachine must pop, place the popped value where the return value is expected, and then return to the caller. If the second operand is anything else, there is no need to pop: just copy the value over to the return value spot and then return to the caller.  

LOAD_CC also has two meanings, very similar to RETURN.

## Note 8
More than one label can map to an instruction. This was to solve the "last elif" problem. The two labels will be replaced with a single label in a later stage of processing.

## Note 9
The FETCH_RV instruction has a list of operands. This is simply the list of params, so the IRMachine knows how many params to pop off the stack. The actual contents of the list DO NOT MATTER!

## Note 10
The instruction MEM_ASSIGN is the memory counterpart of assign (equal operator). It will eat the stack, if the location to be assigned to is determined by a value previously pushed on to the stack.  

The MEM instruction, though it looks like a function if you look at the syntax, isn't really a function. It is actually just another operation like addition or subtraction. Therefore, it doesn't require arguments to be pushed on to the stack, arguments to be popped off the stack, return values to be fetched, return addresses to be saved, etc.

## Note 11
Depending on whether the value to be assigned to is of type STACK TOP, the location to be looked at will change. If we are trying to accomplish something like ```mem(1 + 1) = 1 + 1;```, in the end we are trying to do ```mem($1) = $2;```. Here, $1 will be found below $2 on the stack.

## Note 12
The purpose of adding variables to the dictionary (in the parser) and so on is just a syntax check. It DOES NOT affect the way the IRMachine executes.

## Note 13
The number of variables to be created for a method is known at compilation. Therefore, on method set up, all the variables can be created (i.e. space for them can be allocated on the stack). This helps with variable-sized arrays because now the size of an array does not affect the location of a variable that is created (initialized) later, since all variables are created in the very beginning.

## Note 14
The length of an array is stored in the memory location right before the first element. See the "len" method that has been written in a couple of the test cases.

# LC3 Notes

## Note 1
The less-than and less-than-eq operators had an issue with commutativity. Since they were reusing the gthan and gthaneq operators by simply flipping the arguments, when the arguments were both of type "$", ```lthan($, $) --> gthan($, $)```, so effectively a gthan operation was being called.

## Note 2
The strings are stored consecutively starting at 0x2800 in memory. When a string is to be created on the stack, the string is copied over from here. Since the location of the strings are known at compilation time, a hardcoded ```set``` is called to get the pointer.

## Note 3
PUTS and OUTC are defined in the language as "vanishing" functions. Basically, removing them will not alter the flow of the program in any way or change the state of the machine it is running on (i.e. the registers and memory must not be modified).  
Since on PUTS and OUTC calls, R0 must be loaded with an address (in the case of PUTS) or an ASCII value (for OUT), the current value in R0 is moved to TEMP, and later moved back to R0. We are free to use TEMP, since in this compiler there are no guarantees provided (between methods) on whether TEMP will be used or not.

# Other issues

* Tried to execute "a = (1 +;", instead of getting "not enough operands" or "missing paren" message, got the variable "a" is not defined. This is because the stack does not care about the actual positions of operands, and so in the popping process the "a" and "1" are popped to be added, but "a" obviously hasn't been defined yet.
* TODO solve newline problem (newlines are encounterd in func decl.). Right now I expect a linear deterministic format.
* Two assignment operations in one statement, where both assignments require the creation of a variable should be made illegal. I am having problems resolving what the stack should look like then. EDIT: I have done something to somewhat fix that. However, the compiler still lets this go through: "1 * 8 + (b = 10);". This will break it.
* This needs to fail: 'declare a(a); declare b();\ndeclare c(a, b, c);\na = c(b(1), b(1), 0);'. The way I am counting arguments isn't right, need to think of something better. Currently there is a test for it, that passes. However, the test is passing for the wrong reason. TODO IMPORTANT
* I'm not able to trace how the program came up with the ir_form it did for this: "declare a(a); declare b(); i = a(1 + b() + -b() * -b());" -- SOLVED?
* "```a = b and b not 8 - 8 * - (0);```": The "b not 8" is definitely illegal, but the compiler lets it go through. I see why it's happening, should a check on the effect be introduced at some place? It's an odd case when the "-" and "not" are both there. I hope there aren't cases where the two could get together and screw up a valid statement.