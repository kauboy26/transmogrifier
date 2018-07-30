# About
Transmogrifier is a compiler targeting the LC3 ISA. The project is more or less done, other than some polishing that may be required in a few places. The syntax of the language can be found [here](https://github.com/kauboy26/transmogrifier/blob/master/sample_files/model_program.txt).  

## Intent
LC3 stands for Little Computer 3. The [LC3 has a limited ISA](http://www.cs.unca.edu/~bruce/Spring14/109/Resources/lc3-isa.pdf), and is usually used to teach assembly to beginner computer science students. However, the extremely small ISA of the LC3 sometimes makes us forget that the LC3 still is a computer. For example, the LC3 does not have a ```set``` or ```mov``` instruction. There is an ```add dr, sr1, imm5``` instruction, but this allows us to add values to a register in incremements of 5 bits at a time (```-16``` to ```15```). If we want to set a register to a large number (say 1000), we would need to generate multiple instructions in order to do so.  

The LC3 ISA doesn't have a multiply, divide or even a subtract instruction. Branching capabilities are also restricted due to a 9 bit PC offset limit. My point is that these constraints give us the impression that not much can be done on the LC3. I'm not saying the LC3 is as powerful as an Intel chip. I'm just saying it's better than we usually think.  

The first purpose of this project is to demonstrate that the LC3 can do a good number of things, but it's hard to do that if we write assembly manually ourselves. We don't write x86 assembly because it is usually unproductive. Likewise, if we don't have to write LC3 assembly we can get a lot more done.  

The second purpose is to show what compiled code looks like. Since the output is unoptimized and pieces of the intermediate representation are left in, it should be somewhat easy to map the generated instructions to the original code.

## Usage
If you have the source code, go to the directory containing ```tcc.py```. Then, run:  
```
$ python3 tcc.py filename  
```
where ```filename``` is the file containing the source code you want to compile to LC3 assembly. Expect to see a ```filename.asm``` file containing the LC3 assembly in the same directory.

## Optimizations
This is a toy compiler. I just came up with stuff as I went along, and as a result, there no significant optimizations (you won't see elaborate register allocation schemes, etc.)
