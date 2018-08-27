# About
Transmogrifier is a compiler targeting the LC3 ISA. The project is more or less done, other than some polishing that may be required in a few places. Some cool programs and their sample source files can be found [here](https://github.com/kauboy26/lc3-collection).  


The entire compiler was written in "pure" Python. If you go through the source code of the modules used in the compiling process (look in the `core` folder), you'll see that only the `random` library was used. Since the lexer and parser were hand-written, the syntax-error diagnosing capabilities of the compiler are limited although I've tried to make the error messages as helpful as possible. In the future, **expect the entire compiler to be re-written**, with the help of tools like `flex` and `bison`. The re-written compiler will have wonderful diagnostic messages and optimizing capabilites.

## Intent
LC3 stands for Little Computer 3. The [LC3 has a limited ISA](http://www.cs.unca.edu/~bruce/Spring14/109/Resources/lc3-isa.pdf), and is usually used to teach assembly to beginner computer science students. However, the extremely small ISA of the LC3 sometimes makes us forget that the LC3 still is a computer. For example, the LC3 does not have a `set` or `mov` instruction. There is an `add dr, sr1, imm5` instruction, but this allows us to add values to a register in incremements of 5 bits at a time (`-16` to `15`). If we want to set a register to a large number (say 1000), we would need to generate multiple instructions in order to do so.  

The LC3 ISA doesn't have a multiply, divide or even a subtract instruction. Branching capabilities are also restricted due to a 9 bit PC offset limit. My point is that these constraints give us the impression that not much can be done on the LC3. I'm not saying the LC3 is as powerful as an Intel chip. I'm just saying it's better than we usually think.  

The first purpose of this project is to demonstrate that the LC3 can do a good number of things, but it's hard to do that if we write assembly manually ourselves. We don't write x86 assembly because it is usually unproductive. Likewise, if we don't have to write LC3 assembly we can get a lot more done.  

The second purpose is to show what compiled code looks like. Since the output is unoptimized and pieces of the intermediate representation are left in, it should be somewhat easy to map the generated instructions to the original code.

## Usage
If you have the source code, go to the directory containing `tcc.py`. Then, run:  
```
$ python3 tcc.py filename  
```
where `filename` is the file containing the source code you want to compile to LC3 assembly. Expect to see a `filename.asm` file containing the LC3 assembly in the same directory.  

I recommend creating a one-line shell script that you can call from anywhere to invoke the compiler.  

# About the language
The language has a these features:
* Arithmetic, logical, relational and bitwise operations
* Variables (on the stack)
* Direct memory IO
* Function calls
* Control flow
* An "address of" operator
* Strings and variable length arrays
* Console IO   

Everything is basically a 16 bit signed integer.  

I plan to do these too, but probably when the compiler is re-written:  
* Structs, maybe even objects?
* `malloc`
* Garbage collection

## Arithmetic, logical, relational and bitwise operations
```
a = 10 + (1 * 9 - 2 % 5 / 3);  
b = a & (a | ~a);  
c = a and (b or not a);  
d = c >= b or c < 5 and (1 == a);  
```

## Variables
Variables are automatically created on the stack when they are first mentioned. They are destroyed along with the scope in which they were created. The `end` keyword marks the end of some scope.  
```
var1 = 20;  
if 1:  
    var2 = 30;  
    b = 20;  
end  
```
`var2` and `b` do not exist outside the `if` block, which ends at `end`.

## Direct memory IO
Memory can be read from and written to.  
```
aa = 50;  
mem(aa) = 100;  
mem(aa) = mem(aa) * 2;  
```
The value `100` is written to memory location `50`.

## Functions and function calls
This compiler follows the LC3 calling convention.
```
declare func1(a, b);  
main:  
    a = func1(2, 3);
end  
def func1(j, k):
    if 1:  
        return 20;  
    end  
end
```
Functions must be declared before the `main` method, and defined after. Functions do not have to return a value. The main method isn't a normal function the way it is in some other languages.

## Control flow
There are `if`, `elif`, `else` and `while` keywords (no `for`, `switch`, `break` or `continue`).
```
if a > b:  
elif c > d:  
else d:  
    i = 0;  
    while i < 50:  
        i = i + 1;  
    end  
end  
```

## An "address of" operator
The following increments `a`:  
```
a = 50;  
mem(addrOf(a)) = mem(addrOf(a)) + 1;  
```

## Strings and variable length arrays
Arrays and strings are both created on the stack.  
```
a = 50;
b = array(a);  
c = "hello, world!";  
```
`b` points to the first element of an array with "`a`" elements (here `50`). `c` points to the first character, i.e, it contains the address of "`h`".

In addition, the length of the string or array is stored at index `-1`:  
```
a = array(20);  
length = mem(a - 1);  
```
The length of a string includes the `null` character at the end. So, `"hello"` will give you a length of 6.

## Console IO
You can read input with the `getc()` function, which reads one character at a time. Print using `outc(c)` and `print(s)`. `print(s)` takes a pointer to a character, and keeps printing until a `null` character is reached. `outc(c)` simply prints the ASCII value of `c`.  
```
your_char = getc();  
a = "hello, world!";  
print(a);  
outc('X');  
```
The console output will look like this:  
`hello, world!X`
