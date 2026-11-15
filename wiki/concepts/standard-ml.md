---
type: concept
title: Standard ML
created: 2026-07-08
tags: [standard-ml, language-implementation, programming-languages]
---

# Standard ML

A statically-typed functional programming language in the ML family, known for
its formally-defined semantics, Hindley-Milner type inference, and module
system. It has several mature implementations and a long line of compiler
research.

## Notes

Standard ML implementations are recurring subjects in compiler research.
Standard ML of New Jersey (SML/NJ) pioneered the heap-allocated first-class
continuation runtime model and the [[continuation-passing-style]] compilation
strategy that [[compiling-with-continuations-and-llvm|Farvardin and Reppy]] carry
to an [[llvm]] backend; their work is implemented in the Parallel ML (PML)
compiler of the Manticore system and is intended to transfer back to SML/NJ.
SML/NJ's closure representation is described in
[[efficient-and-safe-for-space-closure-conversion|Shao and Appel]]: safely linked closures
and callee-save registers on a stackless runtime, satisfying the safe-for-space rule.
Other implementations take different backend strategies — MLton uses
trampolining over LLVM, and SML# also targets LLVM.

## Sources

- [[compiling-with-continuations-and-llvm|Compiling with Continuations and LLVM]]
- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]]
- [[continuation-passing-closure-passing-style|Continuation-Passing, Closure-Passing Style]]
- [[efficient-and-safe-for-space-closure-conversion|Efficient and Safe-for-Space Closure Conversion]]
