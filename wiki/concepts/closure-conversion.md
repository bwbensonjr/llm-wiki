---
type: concept
status: reviewed
title: Closure Conversion
created: 2026-08-05
tags: [programming-languages, language-implementation, continuations]
---

# Closure Conversion

The compiler pass that turns a nested, lexically-scoped function into an explicit
pair of code and captured environment — together with the *closure analysis* that
decides which functions need a run-time closure at all, and what may live in
registers instead of the heap.

## Notes

Closure analysis is where the payoff of lexical scoping is collected. Because the
compiler sees every reference to a variable, it can choose any representation for
an environment. RABBIT sorts each `LAMBDA`-expression into three cases: **fully
closed**, when the function escapes as data and needs a standard closure;
**partially closed**, when it is only ever called by name but from inside other
closures, so its environment must be built without a code pointer; and **not
closed**, when the environment is always recoverable at the point of call.

The pass is naturally entangled with the rest of compilation — determining which
functions to close requires knowing which variables are referenced from within
closed functions below each node, so both are computed in a single pass — and it
typically runs after conversion to [[continuation-passing-style]]. Aggressive
analysis can eliminate closures entirely for programs that never treat functions
as data.

[[orbit-an-optimizing-compiler-for-scheme|ORBIT]] supplies the algorithms RABBIT
left open, splitting the work into *strategy analysis* (heap, stack, or registers)
and *representation analysis* (the closure's actual run-time structure), and adding
closure hoisting and packing so several procedures can share one environment
without indirection. [[escape-analysis]] is what decides the strategy.

[[an-incremental-approach-to-compiler-construction|Ghuloum]] shows the pass at its
smallest: free-variable analysis annotates each `lambda` with what it references but
does not bind, then `lambda` forms become `closure` forms with the code lifted to the
top — a code label in the closure's first cell, captured values in the rest.

The name is contested, and Clinger and Hansen
([[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Twobit]])
are explicit about the tangle. What Twobit calls
[[lambda-lifting]] is what SML/NJ's compiler calls closure conversion — the same
transformation, differing in how global the flow equation is. Meanwhile Wand and
Steckler use "closure conversion" for a source-level transformation that replaces a
procedure with a representation of it, which is orthogonal to lifting. Twobit also
supplies a cheap version of the analysis: *single assignment analysis*, a first-order
closure analysis that identifies parameters assigned once to a `lambda` and called as
often as referenced, which are therefore known local procedures needing no closure.

## Sources

- [[rabbit-a-compiler-for-scheme|RABBIT: A Compiler for Scheme]]
- [[orbit-an-optimizing-compiler-for-scheme|ORBIT: An Optimizing Compiler for Scheme]]
- [[an-incremental-approach-to-compiler-construction|An Incremental Approach to Compiler Construction]]
- [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Lambda, the Ultimate Label: A Simple Optimizing Compiler for Scheme]]
- [[the-development-of-chez-scheme|The Development of Chez Scheme]]
- [[a-nanopass-framework-for-commercial-compiler-development|A Nanopass Framework for Commercial Compiler Development]]
