---
type: concept
title: Continuation-Passing Style
created: 2026-07-08
tags: [continuations, language-implementation, programming-languages]
---

# Continuation-Passing Style

A compilation and program-representation technique (CPS) in which control flow is
made explicit by passing each computation its **continuation** — a function
representing "the rest of the program" — as an argument, so that no call ever
returns in the ordinary sense; every call is a tail call.

## Notes

CPS is a workhorse of functional-language compilers. In the heap-allocated
first-class continuation runtime model (traceable to Appel's *Compiling with
Continuations* and the SML/NJ system), continuation closures are immutable and
allocated on the heap rather than on a call stack. This yields two payoffs:
constant-time `callcc` and very lightweight multithreading, plus a simple garbage
collector interface — with no stack to scan, the collector needs no knowledge of
the code generator.

The cost is a demand for **guaranteed tail-call optimization**: because loops and
returns are expressed as tail calls, they must not grow the stack. This is what
makes [[llvm]] awkward as a CPS backend and motivates the Jump-With-Arguments
convention in [[compiling-with-continuations-and-llvm|Farvardin and Reppy]]. The
Manticore/PML and [[standard-ml|SML/NJ]] compilers both use this model; GHC
instead makes the stack explicit via a whole-program CPS transformation.

## Sources

- [[compiling-with-continuations-and-llvm|Compiling with Continuations and LLVM]]
