---
type: entity
status: provisional
title: William D. Clinger
created: 2026-08-05
tags: [programming-languages, language-implementation, scheme, lisp]
---

# William D. Clinger

A computer scientist who designed Twobit — the compiler behind the [[larceny]]
implementation of [[scheme]] — and who argued that an optimizing compiler for a
higher-order language can be simple if it heap-allocates aggressively and then
uses [[lambda-lifting]] to make most of that allocation unnecessary.

## Notes

Clinger's design position is a deliberate contrast with the compilers he inherits
from. Where [[rabbit-a-compiler-for-scheme|RABBIT]] and
[[orbit-an-optimizing-compiler-for-scheme|ORBIT]] set out to advance code quality,
Twobit's stated goals were simplicity, portability, and fast compilation — with
code merely *good enough* to support a high-performance system. He is explicit
that the machine-independent compiler is under 5,000 lines, roughly a tenth of
comparable compilers.

He prefers direct style to [[continuation-passing-style|CPS]] as an intermediate
form, on the grounds that it is more readable and that premature CPS conversion
makes register allocation, targeting, and parallel assignment optimization
harder — while acknowledging that nothing in Twobit's design precludes a later CPS
conversion in the code generator.

A recurring theme in his framing is that compiler optimization is not where the
performance of this class of language is decided: procedure call cost, storage
allocation, and garbage collection matter more, and most standard Scheme benchmarks
measure the collector rather than the compiler.

Beyond the work covered here, the paper's citations show him as co-editor with
Jonathan Rees of the Revised^4 Report on Scheme and co-author of "Macros that
Work," and as the author of the Scheme 311 compiler and of earlier work on
continuation implementation strategies — none of which is itself an ingested source.

## Sources

- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]]
