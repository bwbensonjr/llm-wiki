---
type: summary
status: provisional
title: Flow-Directed Lightweight Closure Conversion
created: 2026-10-31
source: https://engineering.purdue.edu/~qobi/papers/fdlcc.pdf
raw: raw/2026-10-31-fdlcc.md
tags: [scheme, language-implementation, programming-languages]
---

# Flow-Directed Lightweight Closure Conversion

## Summary

Jeffrey Mark Siskind's paper (NEC Research Institute) on the [[closure-conversion]] method in Stalin, an aggressively optimizing whole-program compiler for [[scheme|Scheme]]. Stalin is deliberately **batch-mode**: no read-eval-print loop, no `eval`, no loading new code into a running program. It compiles the whole source program, via C, into a single executable whose behavior equals loading the program into a fresh interactive Scheme and letting it terminate, so it targets application delivery and production runs rather than development. That closed world is what licenses its analyses: polyvariant interprocedural flow and reachability analysis, supporting points-to, [[escape-analysis|escape]] and lifetime analyses, lightweight closure and CPS conversion, automatic inlining, region-based storage, unboxing, and program-point-specific representation selection.

The paper contrasts three implementations on a linked-closure model. A *baseline* gives every procedure a closure with a slot per bound variable and a parent pointer, passes and spills parents and variables, and references variables through the closure pointer. A *conventional* one applies only optimizations visible from the syntax of one top-level procedure. The *lightweight* method uses the whole-program results to eliminate closures, variable and parent slots, closure pointers, parent parameters and passing, and spilling; to compress the slots that remain; to "globalize" variables that can live in globals; and to "hide" others. Siskind notes the method is not tied to linked closures and applies to display and flat representations too, and that its results are incomparable to [[lightweight-closure-conversion|Steckler and Wand's]]: each performs optimizations the other does not.

On twenty benchmarks, the lightweight method eliminates far more variables, closures and indirections than either alternative, removing all slotted variables and every closure in half the benchmarks, and its code runs substantially faster. Against Scheme->C, Gambit-C, Bigloo and Chez, Stalin wins on all but three, often by several times and sometimes by one or two orders of magnitude. Siskind points out that the other compilers were often run with flags that violate R4RS semantics (assuming standard bindings, fixnum-only arithmetic), which "manually gives these compilers information that can only be determined by whole-program interprocedural flow analysis", information Stalin derives soundly on its own.

## Why this matters

Stalin is the far end of the trade the [[separate-compilation]] question is about. By giving up `eval`, the REPL and separate compilation entirely, it gets a closed world in which flow analysis can prove what other Scheme compilers can only be told by unsafe flags, and it emits exactly the standalone executable that dynamic Lisps find hard to produce. The paper quantifies what the closed world buys, which is the benchmark against which any open-world compromise, such as per-library compilation with cross-library inlining or sealing, has to be measured.
