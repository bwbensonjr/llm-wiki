---
type: concept
title: Safe for Space
created: 2026-08-05
tags: [programming-languages, language-implementation]
---

# Safe for Space

The property that a compiler transformation does not increase a garbage-collected
program's memory use by more than a constant factor. A transformation is **safe for space**
when nothing it introduces keeps data reachable that the source program would have let the
collector reclaim; the parallel property for running time is **safe for time**.

## Notes

The property exists because [[closure-conversion|closure conversion]] can quietly violate
it. A closure holding variables with different future lifetimes — one of them pointing at a
large structure — prevents the collector from reclaiming any of them until the whole
closure becomes unreachable. The resulting inflation is **not bounded by any constant
factor**, which is what makes this a correctness-shaped concern rather than a tuning
question: a program's asymptotic space behavior can change under compilation.

The failure mode is specifically **environment sharing**. A **flat** closure copies each
free variable it needs and holds nothing else, so it is safe for space by construction. A
**linked** closure reaches shared structure by pointer, which is cheaper to create and can
be smaller, but it retains whatever else that structure holds.
[[continuation-passing-closure-passing-style|Appel and Jim]] noted the trade-off in 1988 —
linked closures "can take up more space than flat closures because they hold on to closures
which might otherwise be reclaimed" — and the concern is live rather than historical:
JavaScript's V8 engine shares environments in a way that is not safe for space, per
[[closure-conversion-is-safe-for-space|Paraskevopoulou and Appel]].

The rule as SML/NJ states it, in
[[efficient-and-safe-for-space-closure-conversion|Shao and Appel]], is that *any local
variable binding must be unreachable after its last use within its scope*. They report
real programs whose live data was 2 to 80 times larger than necessary before SML/NJ obeyed
it, and argue that stack frames violate it too: a function binding a series of large
intermediate results keeps all of them live until it returns. Their safely linked closures
show that sharing and space safety are compatible, as long as shared records group only
variables with the same lifetime.

Where the property bites is in deciding how far to optimize closures.
[[optimizing-closures-in-o-0-time|Chez Scheme's]] optimization suite treats it as a hard
constraint: every transformation must preserve space safety and must never add allocation
or memory operations relative to naive flat closures, so flat-closure performance is a
floor a programmer can rely on. That constraint is also part of why Chez declines
[[efficient-and-safe-for-space-closure-conversion|Shao and Appel's]] nested representation
and optimizes the flat model instead — and why
[[the-development-of-chez-scheme|Chez's]] original choice of flat closures is a space
decision as much as an access-cost one.

Being asymptotic, the property does not say a safe-for-space representation is *faster*.
Flat closures cost more to create (proportional to the free-variable count) and less to
access (a single indirect), so "safe for space" and "optimal" are separate claims. That is
why a compiler can honor the property and still have real work left to do on closure
representation.

The property was folklore rigor for decades before
[[closure-conversion-is-safe-for-space|Paraskevopoulou and Appel]] proved it, mechanized in
Coq, for flat closure conversion on CPS lambda calculus — the first formal proof of space
safety for such a transformation, and one whose cost model includes the collector rather
than idealizing it away. That proof matters because a compiler that does not preserve
resource consumption makes source-level cost analysis meaningless, whatever its
extensional correctness guarantees.

## Sources

- [[continuation-passing-closure-passing-style|Continuation-Passing, Closure-Passing Style]]
- [[optimizing-closures-in-o-0-time|Optimizing Closures in O(0) Time]]
- [[closure-conversion-is-safe-for-space|Closure Conversion Is Safe for Space]]
- [[efficient-and-safe-for-space-closure-conversion|Efficient and Safe-for-Space Closure Conversion]]
