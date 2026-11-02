---
type: summary
title: "Clasp: Common Lisp Using LLVM and C++ for Molecular Metaprogramming"
created: 2026-10-31
source: https://www.youtube.com/watch?v=8X69_42Mj-g
raw: raw/2026-10-31-clasp-common-lisp-using-llvm-and-c-for-molecular-metaprogramming.md
tags: [language-implementation, llvm, lisp, programming-languages]
---

# Clasp: Common Lisp Using LLVM and C++ for Molecular Metaprogramming

## Summary

A 2015 Google Tech Talk in which [[christian-schafmeister|Christian Schafmeister]], a Temple University chemist, presents [[clasp|Clasp]], a new Common Lisp that compiles through [[llvm|LLVM]] and interoperates with C++. It also covers CANDO, the molecular-design tool built on it. The first third is the chemistry: "molecular Lego" (spiroligomers) are rigid, modular molecules his lab can synthesize at sizes too complex to design by hand. He wants a programming language for exploratory, large-scale computational design (Monte Carlo search across hundreds of thousands of CPUs), plus generated code for the derivatives of force-field energy functions.

He had tied his C++ chemistry library to [[python|Python]] with Boost.Python and found the interface work (memory models, exceptions, wrappers) took over the project. A small Lisp interpreter of his own ran well on a 40,000-CPU machine but was too slow, so he moved to Common Lisp for its macros, which are written in the language itself, and for a compiler he could tune down to native code. He calls C++ hostile to other languages: name mangling, overloading, virtual functions and exceptions leave most Lisps to reach it only through C foreign function interfaces. Clasp skips the FFI. Its clbind library, adapted from Lua's Luabind (itself modeled on Boost.Python), uses C++ templates to generate wrappers at compile time from a Lisp name and a function pointer. That extends to classes, constructors, methods and pointer-ownership rules, which is how he exposes LLVM's C++ API and much of Clang.

At the time, Clasp was about 150,000 lines of C++ beneath Common Lisp code taken from ECL (Embeddable Common Lisp), with a new compiler written by him. A slow interpreter bootstraps a simple compiler that goes straight from s-expressions to LLVM IR, which then loads Robert Strandh's Cleavir compiler from the SICL project. Cleavir lowers through an AST and a flow-graph IR with inlining, type inference and [[escape-analysis|escape analysis]], deciding what lives on the stack and what needs a heap closure. Clasp does JIT and ahead-of-time compilation in memory, emits DWARF so GDB and LLDB see interleaved Lisp and C++ frames, and profiles both together. Using Clang's AST matchers from Lisp, a static analyzer parses Clasp's own C++ source and generates about 20,000 lines of glue so the Memory Pool System compacting collector can move around 300 C++ classes and update every pointer. Boehm GC is used for bootstrapping. Generated code then ran about 100x slower than SBCL, because generic arithmetic called out to C++; the fix he proposes is Cleavir's inlining and type inference.

## Why this matters

This matters because it may help with ways of calling external code in Emit.
