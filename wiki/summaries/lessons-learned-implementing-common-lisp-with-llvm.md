---
type: summary
status: reviewed
title: Lessons Learned Implementing Common Lisp with LLVM
created: 2026-10-31
source: https://www.youtube.com/watch?v=mbdXeRBbgDM
raw: raw/2026-10-31-2018-llvm-developers-meeting-c-schafmeister-lessons-learned-implementing-common-lisp-with-llvm.md
tags: [language-implementation, llvm, lisp, programming-languages]
---

# Lessons Learned Implementing Common Lisp with LLVM

## Summary

A 26-minute talk by [[christian-schafmeister|Christian Schafmeister]] at the 2018 LLVM Developers' Meeting, on six years of building [[clasp|Clasp]], a Common Lisp implementation that uses [[llvm|LLVM]] as its back end and interoperates directly with C++. The motivation is chemistry: his lab builds large, stiff "molecular Lego" molecules (catalysts, filters, sensors) and wants to design them computationally, by evolutionary search run as massively parallel arithmetic on GPUs. Clasp sits inside CANDO, his environment for that design work. He chose Common Lisp over [[python|Python]] because it is dynamic but built to compile to efficient native code, and above all for its macros, which he calls the language's killer feature.

The path there: a large C++ chemistry library first exposed to Python with Boost.Python, then to a homegrown Lisp interpreter through a C++ template library that generates wrappers automatically. The same mechanism later exposed about 100 LLVM classes and roughly 420 functions to Lisp, so the whole compiler could be written in Common Lisp against LLVM's C++ API, one Lisp function per C++ method with the same layout. His first compiler went straight from s-expressions to LLVM IR. It was complete but very slow, especially on closures. He then adopted Robert Strandh's Cleavir, a compiler written in pure Common Lisp that lowers through an AST and a graph-based intermediate representation before reaching LLVM IR. Bootstrapping from Clang to the full system takes about half an hour: an interpreter builds the bootstrap compiler (bclasp), which builds the final one (cclasp). Code generation methods are generic functions that also dispatch on an ABI argument, which he plans to use to retarget a Common Lisp subset at GPU kernels, combined with symbolic differentiation of molecular force fields.

Runtime features: a compacting garbage collector, made workable in C++ by a static analyzer (written in Lisp on Clang's AST matchers) that finds every pointer in every managed class. Also expression-level debug info, so LLDB and GDB step through interleaved C++ and Lisp frames; link-time optimization across both languages' bitcode; the ORC JIT; pthreads; and C++-compatible exception handling, so the stack unwinds cleanly through mixed frames. DTrace flame graphs profile both languages together. Reported results: a Fibonacci microbenchmark within about 4x of C++, and about 97.8% of the ANSI Common Lisp test suite passing. His main lesson is that LLVM can be learned from the outside, from public documentation and the community, at the cost of keeping up with its constantly changing C++ API. He closes by asking for help writing custom calling conventions.

## Why this matters

This matters because my Emit Scheme system is an LLVM-backed [[lisp|Lisp]] implementation and I want the ability to compare.
