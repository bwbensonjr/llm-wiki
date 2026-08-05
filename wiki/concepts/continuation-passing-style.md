---
type: concept
status: reviewed
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

CPS as a *compiler intermediate representation* originates with
[[rabbit-a-compiler-for-scheme|Steele's RABBIT compiler]], where its defining
property is that the IR is itself a subset of the source language — so the same
optimizer runs at both levels — and where its imperative reading (no control
stack, no function ever returns) is what makes transcription to machine code
straightforward. [[closure-conversion|Closure analysis]] conventionally follows
CPS conversion.

[[orbit-an-optimizing-compiler-for-scheme|ORBIT]] carries the model into a
production compiler and names the payoffs precisely: continuation-bound variables
are the compiler's temporaries with no special status, the single-return-value
restriction disappears, and tail calls become syntactically evident. Its CPS output
is valid Scheme over a node tree of just four node kinds — lambda, call, reference,
constant.

## Sources

- [[compiling-with-continuations-and-llvm|Compiling with Continuations and LLVM]]
- [[rabbit-a-compiler-for-scheme|RABBIT: A Compiler for Scheme]]
- [[orbit-an-optimizing-compiler-for-scheme|ORBIT: An Optimizing Compiler for Scheme]]
- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]]
- [[a-tractable-native-code-scheme-system|A Tractable Native-Code Scheme System]]
- [[the-development-of-chez-scheme|The Development of Chez Scheme]]
- [[implementation-strategies-for-first-class-continuations|Implementation Strategies for First-Class Continuations]]
- [[lightweight-closure-conversion|Lightweight Closure Conversion]]
