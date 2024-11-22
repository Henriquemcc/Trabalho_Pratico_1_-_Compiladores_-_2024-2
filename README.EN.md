[Versão em Português](README.md)

# Practical Work 1 - Compilers - 2024-2

Practical work of the subject Compilers of the Computer Science course at Pontifical Catholic University of Minas Gerais.

## Statement

### **Control Flow Graph (CFG)**

Optimizers and humans do not view a computer program in the same way. Humans are more interested in the source code. However, source code is extremely different
from machine code. Furthermore, from an engineering point of view, it is appropriate that there is a common way of representing programs that is relevant to various languages and architectures.
In this sense, the optimizer needs to work with an intermediate representation of the program.

Usually, compilers represent programs as [_Control Flow Graphs_.](https://en.wikipedia.org/wiki/Control-flow_graph)

A CFG is a direct graph in which the nodes are _basic blocks_. There is an edge that goes from basic block B1 to basic block B2 if the execution of the program can flow from B1 to B2.

See for example the code below, which calculates the factorial of a number, and its respective CFG.

```
int fact ( int n) {
    int ans = 1 ;
    while (n > 1 ) {
        ans *= n ;
        n--;
    }
    return ans ;
}
```

In the practical work of this discipline, we will work with a compilation framework called LLVM (Low Level Virtual Machine). Despite its name, LLVM is much more than a low-level virtual machine: it is a compiler and an optimizer for C and C++ programs. It has an ecosystem and an active community of compiler engineers who work to create new passes and optimizations to make object code more efficient.

In Figure 2 we see the LLVM pipeline. The front-end ([_clang_](https://clang.llvm.org/)) transforms C code into bytecode (intermediate representation). The optimizer ([_opt_](https://llvm.org/docs/CommandGuide/opt.html)) works on the intermediate representation, performing passes, or optimizations, such as Constant Propagation, Dead Code Elimination, among others. Note that the optimizer performs several optimizations in an arbitrary order, since it is NP-Hard to determine the optimal sequence of optimizations. Note also that, for this reason, the optimizer's output is always in the same format as the input, since the code can pass through it an infinite number of times. Opt has 3 levels of aggressiveness, with level O3 being the one with the most aggressive passes and transformations, which can drastically modify the semantics of your program.

Unfortunately, it is not so trivial to identify which passes are performed in clang levels O1, O2 and O3. [_In this file_](https://github.com/llvm-mirror/llvm/blob/master/lib/Transforms/IPO/PassManagerBuilder.cpp) you can see that several transformations are added to the pipeline depending on the **OptLevel** variable.

Finally, after applying the optimizations, the static compiler (llc) transforms the bytecode into machine code for different architectures, in addition to performing machine-dependent optimizations (Register Allocation, for example).

#### **Work Requirements.**

You must write a script in **bash** or **python** that receives as input a C source code (source.c) and produces, in the output, images in PNG format (**main.png**, **foo.png**, ...) that represent the Control Flow Graphs for the functions contained in the source file.

In the **cfg.zip** file you will find a **src** folder containing some programs. You must generate CFGs for each of the programs contained in the folder.

In addition, you must also generate different versions of the CFG for each clang optimization level. Therefore, for each source code, you must generate 4 CFG versions: one CFG for optimization level O1, another CFG for level O2, and another CFG for level O3. Remember that there can be more than one CFG per file, since the graphs are per function and not per module.

Finally, you must observe the generated graphs and explain at least 2 transformations that occurred at different optimization levels.

#### What must be submitted:

You must submit a .zip file containing:

1. A **gen_cfg.sh** or **gen_cfg.py** script that receives as its first argument a program written in C and generates, as output, PNG images representing the control flow graph of this program at three different optimization levels (O1, O2 and O3). [10 pts].
2. The CFG images for all programs contained in the **src/singlesource/** folder, at the three different optimization levels. [1 pt].
3. The _.digraph_ files of all CFGs of the programs contained in the **src/** folder, at the three different optimization levels [1 pt]
4. A PDF describing **two or more** transformations that are possible to notice when analyzing the CFG of the same program after different optimization levels. [3 pts].

#### **Final Thoughts && Tips**

1. Once you have clang installed, you can generate a readable intermediate representation file with the **-emit-llvm** flag.
2. There is a pass that compiles the intermediate representation to **.dot** format. Can you find this pass? Try using the **opt --help** command to list all possible passes.
3. The [graphviz](https://graphviz.org/) tool is the ideal software for handling **.dot** files.
4. See the examples that already have CFGs formed **infinity.c** & **fact.c**.
5. **Attention!** If the intermediate representation has the **optnone** flag, the opt tool will ignore any attempts to run any pass, including those for generating .dot files.
6. If any of the programs does not compile, explain in the submitted PDF what problem occurred in its compilation.
7. **Attention!** There is more than one .c file in the **singlesource/** folder

#### **References**

[1] Control Flow Graphs: https://en.wikipedia.org/wiki/Control-flow_graph

[2] clang: https://clang.llvm.org/

[3] opt: https://llvm.org/docs/CommandGuide/opt.html

[4] Graphviz: https://graphviz.org/

Good work!

## Source code

The source code of the developed program, in the Python programming language, is available at [gen_cfg.py](gen_cfg.py).

## PNG files

The PNG files generated from the developed program are located at [imagens_cfg](docs/imagens_cfg).

## Digraph Files

The generated Digraph files are in [arquivos_.digraph](docs/arquivos_.digraph).

## Report

The developed report (in Portuguese) is available at [Relatorio.pdf](docs/relatorio/Relatorio.pdf).