---
type: concept
status: reviewed
title: Escape Analysis
created: 2026-08-05
tags: [programming-languages, language-implementation]
---

# Escape Analysis

The compiler analysis that determines whether a dynamically created object — in
the [[scheme]] setting, a closure — outlives the context that created it, and so
whether it must be heap-allocated or may live on the stack or in registers.

## Notes

In ORBIT's formulation a procedure **escapes** when the compiler cannot identify
all the places it is called. A procedure in call position counts as *known* if it
is a lambda-node, a reference to a variable provably bound to a particular
lambda-node, or a variable with early-binding information; anything else is
unknown.

The useful refinement is **downward-only escape**: a procedure whose call sites
are not all known may still avoid the heap if the current continuation provably
will not be invoked before the procedure becomes inaccessible. That condition is
exactly the restriction Pascal's definition places on procedural parameters —
which is why Pascal can pass a procedure as an argument but not return one.

Escape analysis is what makes [[closure-conversion]] pay: without it, every
closure must be heap-allocated defensively, and the cost of first-class
procedures becomes the intrinsic penalty it was long assumed to be.

## Sources

- [[orbit-an-optimizing-compiler-for-scheme|ORBIT: An Optimizing Compiler for Scheme]]
- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]]
- [[lightweight-closure-conversion|Lightweight Closure Conversion]]
- [[optimizing-closures-in-o-0-time|Optimizing Closures in O(0) Time]]
