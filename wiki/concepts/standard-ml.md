---
type: concept
status: reviewed
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
Other implementations take different backend strategies — MLton uses
trampolining over LLVM, and SML# also targets LLVM.

## Sources

- [[compiling-with-continuations-and-llvm|Compiling with Continuations and LLVM]]
