---
type: entity
status: reviewed
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

His other major line of work is macros. With [[mitchell-wand|Mitchell Wand]] he wrote
the HOPL IV history of [[hygienic-macros|hygienic macro technology]], and he is a
participant in the story it tells: "Macros That Work" (with Jonathan Rees, 1991)
introduced the Strong Hygiene Condition, and the `syntax-rules` appendix to R4RS is
his. That history is also notably self-critical — he records that the strong-hygiene
claim was made without proof and was later broken by Petrofsky extraction and
Kiselyov defilement.

The two sides of him sit oddly together and are worth holding in view at once: the
Twobit paper argues an optimizing compiler need not be complex, while the macro
history is an account of a problem that took twenty years to solve reliably and ten
more to solve well.

A third line of work is control. With Anne Hartheimer and Eric Ost he surveyed and
measured the ways to implement
[[first-class-continuations|first-class continuations]], producing the direct-cost /
indirect-cost framing and the three-scenario method that this wiki now uses to compare
[[larceny]], [[scheme-48|Scheme 48]], and [[chez-scheme|Chez Scheme]]. The
zero-overhead claim Twobit makes for Larceny's stack cache cites that paper.

Across all three lines his method is recognizably the same: define the cost model
before comparing, and distrust a benchmark that does not say which scenario it
represents.

He was also co-editor with Rees of the Revised^4 Report on Scheme and wrote the
Scheme 311 compiler.

## Sources

- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]]
- [[hygienic-macro-technology|Hygienic Macro Technology]]
- [[implementation-strategies-for-first-class-continuations|Implementation Strategies for First-Class Continuations]]
- [[representing-control-in-the-presence-of-first-class-continuations|Representing Control in the Presence of First-Class Continuations]]
