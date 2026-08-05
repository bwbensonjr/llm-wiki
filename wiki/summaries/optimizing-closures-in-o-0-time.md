---
type: summary
status: provisional
title: Optimizing Closures in O(0) Time
created: 2026-08-05
source: https://andykeep.com/pubs/scheme-12a.pdf
raw: raw/2026-08-05-scheme-12a.md
tags: [programming-languages, language-implementation, scheme, chez-scheme]
---

# Optimizing Closures in O(0) Time

## Summary

Andrew W. Keep, Alex Hearn, and [[r-kent-dybvig|R. Kent Dybvig]]'s Scheme Workshop 2012
paper describing the [[closure-conversion|closure]] optimizations in
[[chez-scheme|Chez Scheme]], with an algorithm that implements them. The facetious title
refers to the compile-time cost: the pass adds work during closure conversion but emits
less code, so later passes more than repay it.

**The baseline is the flat closure**, which Chez adopted with assignment conversion
boxing the locations of *assigned* variables only (Dybvig, 1987) so values are never
duplicated. Its virtues are stated plainly: every free variable is reachable in a single
indirect, with no nested environment to traverse; creation cost is proportional to the
free-variable count, which is usually small and is repaid whenever a variable is
referenced more than once; and it is **[[safe-for-space|safe for space]]**, holding nothing
the procedure might not need, so the collector can reclaim values that are merely visible in the
environment. The paper's constraint is that its optimizations must *never do harm* —
never add allocation or memory operations relative to naive flat closures, and never lose
space safety — so a programmer can rely on flat-closure performance as a floor.

**Avoiding closures entirely** turns on whether a procedure is *well known*: known at
every call site, so its value is never used except where its λ-expression is provably the
one being invoked, meaning the code pointer is dead because each call can jump to a
direct-call label. The representation then depends on the free-variable count — none, and
the closure disappears; one, and the closure is *replaced by that variable*; two, and it
becomes a pair (two words against a closure's three); three or more, and it becomes a
vector, chosen over a closure because a small length is slightly cheaper to store than a
full-word code pointer and because vectors help with sharing. A not-well-known procedure
must keep a real closure, since some call site can only jump indirectly through its code
pointer.

**Eliminating free variables** covers six cases: unreferenced variables, globals,
variables bound to constants (which lets a closure be allocated statically and treated as
a constant, in cooperation with the linker), aliases removed by copy propagation,
**self-references** — a procedure's own name never needs to be in its own free-variable
list, since a link at a known offset always pointing back to itself is useless — and
**unnecessary mutual references**, where mutually recursive procedures hold each other
only to supply each other's closures. The paper is careful about when the mutual case does
*not* apply: if `even?` also closes over an outer variable `z`, it genuinely needs its own
closure, and `odd?` genuinely needs to reach it.

**Sharing closures** merges closures with the same lifetime and a single code pointer, or
the same free variables and none, so a pointer between them becomes a self-reference and
vanishes. The obstacle named is representational — Chez's closure format has no room for
multiple code pointers, and fixing that needs storage-manager support — so a shared
closure admits at most one not-well-known member.

**Results.** Over 67 R6RS benchmarks the pass statically eliminated **56.94%** of closures
and **44.89%** of free variables, and dynamically **58.25%** of closure allocation and
**58.58%** of the memory references attributable to closure access.

**On lambda lifting, the paper takes a position.** Replacing a well-known one-free-variable
closure with that variable is called "a degenerate form of
[[lambda-lifting|lambda lifting]]," and the authors say why they stop there: converting
free variables into separate arguments increases stack traffic for non-tail-recursive routines and raises
register pressure whenever two or more variables become live in place of one package.
Restricting the move to the single-variable case is what keeps the never-do-harm
guarantee, "as we are replacing a single package of values with just one value." They
apply the same judgment to
[[lightweight-closure-conversion|Steckler and Wand's lightweight closures]], describing
them as "a limited form of lambda lifting" that, like full lifting, "can sometimes do harm
relative to the straight flat-closure model."

The related work also credits Serrano's control-flow-analysis-based elimination of a
well-known closure's code part, [[david-kranz|Kranz's]]
[[orbit-an-optimizing-compiler-for-scheme|ORBIT]] for stack- and register-allocated
closures (judged orthogonal to this work), Shao and Appel's nested representation for
closures sharing some free variables — which the authors decline in favor of optimizing
the flat model, partly because much of its reported saving came from global variables they
omit entirely — and Appel's own elimination of self-references and multi-code-pointer
sharing for strongly connected `letrec` sets. They note that Chez has performed a few of
these since 1992 without publishing them.

## Why this matters

This supplies the mechanism behind a claim
[[a-nanopass-framework-for-commercial-compiler-development|the nanopass paper]] makes and
does not explain: that the rewritten back end "improved closure optimization." Here that
improvement is enumerated, bounded by a never-do-harm rule, and measured — better than
half of closure allocation and closure-related memory traffic removed.

More pointedly, it is Chez's answer in a long-running argument this corpus has been
assembling from both sides. [[lambda-the-ultimate-label-a-simple-optimizing-compiler-for-scheme|Twobit]]
lifts aggressively, stopping only when a body already requires a closure;
[[continuation-passing-closure-passing-style|SML/NJ]] adds free variables as extra
arguments for every known function; [[lightweight-closure-conversion|Steckler and Wand]]
lift selectively and prove it sound. Keep, Hearn, and Dybvig accept the mechanism and
reject the enthusiasm, on a cost basis the others do not price: extra arguments mean stack
traffic and register pressure, so lifting *can lose*, and they therefore lift only where
one value replaces one package. Three compilers, three policies, one transformation — and
this is the paper that states the case against doing it freely.

It also closes the loop on space safety. Appel and Jim observed that linked closures can
retain what flat ones would release; Shao and Appel built a nested representation that
shares without breaking that property; Chez's answer is to keep flat closures and optimize
within them, on the bet that free-variable references are far more common than closure
creation. That is a clean statement of a design trade-off where each party measured
something different.

Finally, the well-known/not-well-known distinction is the practical version of what
[[escape-analysis]] is for. A procedure whose value never escapes its known call sites
does not need a code pointer at all, and everything above follows from that one fact —
which is a more useful framing than "escaping procedures need heap closures," because it
says what to do with the ones that do not.
