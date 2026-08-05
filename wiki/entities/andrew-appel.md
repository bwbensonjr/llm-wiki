---
type: entity
status: provisional
title: Andrew W. Appel
created: 2026-08-05
tags: [programming-languages, language-implementation, standard-ml, continuations]
---

# Andrew W. Appel

A Princeton computer scientist and a principal architect of
[[standard-ml|Standard ML of New Jersey]], whose CPS-based back end he described with
Trevor Jim in
[[continuation-passing-closure-passing-style|Continuation-Passing, Closure-Passing Style]].
He is the source of the position that a compiler for a higher-order language needs no
stack at all.

## Notes

Two commitments run through his work on compiling higher-order languages, and both are
argued rather than assumed.

The first is that **cheap garbage collection changes the calling convention**: if
collection costs little, call frames and continuations can live in the heap, which removes
the analysis deciding what may be stack-allocated, simplifies the runtime, and makes
first-class control cheap. He quantifies the concession — stack-allocating every closure
record would have saved 6–10% — and notes the stackless compiler used about 20% less
memory, since a stack retains objects past their last use. That argument is met head-on by
[[representing-control-in-the-presence-of-first-class-continuations|Hieb, Dybvig, and Bruggeman]],
who accept the accounting and reject the premise on locality grounds, and it
sits opposite the strategies catalogued in
[[implementation-strategies-for-first-class-continuations|Clinger, Hartheimer, and Ost]].

The second is that a compiler back end should be **many small phases with well-defined
interfaces** rather than one analysis. He states it as a criticism of
[[orbit-an-optimizing-compiler-for-scheme|ORBIT]]'s single tangled back end, which is the
same case [[nanopass]] makes later with measurements.

His [[closure-conversion|closure-conversion]] work also raises the space question that
became the safe-for-space rule: linked closures can retain data that flat closures would
let the collector reclaim.

## Sources

- [[continuation-passing-closure-passing-style|Continuation-Passing, Closure-Passing Style]]
- [[optimizing-closures-in-o-0-time|Optimizing Closures in O(0) Time]]
