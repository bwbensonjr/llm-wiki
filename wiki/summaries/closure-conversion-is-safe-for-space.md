---
type: summary
status: provisional
title: Closure Conversion Is Safe for Space
created: 2026-08-05
source: https://www.cs.princeton.edu/~appel/papers/safe-closure.pdf
raw: raw/2026-08-05-safe-closure.md
tags: [programming-languages, language-implementation, formal-methods, program-verification]
---

# Closure Conversion Is Safe for Space

## Summary

[[zoe-paraskevopoulou|Zoe Paraskevopoulou]] and [[andrew-appel|Andrew W. Appel]]'s ICFP
2019 paper (PACMPL 3, article 83) giving a mechanized proof that flat-environment
[[closure-conversion|closure conversion]] for CPS lambda calculus is correct *and*
[[safe-for-space|safe for space and time]] — the first formal proof of space safety for a
closure-conversion transformation. It is part of the **CertiCoq** pipeline from Coq
(Gallina) through CompCert Clight to assembly, and the results are mechanized in Coq, with
the proof composing with the correctness proofs of CertiCoq's other phases.

**The problem it takes on** is that verified compilers usually guarantee only *extensional*
behavior — the result of the computation — while programmers also expect *intensional*
properties like resource consumption to survive compilation. The authors put the stakes
plainly: static cost-analysis frameworks let programmers reason formally about a program's
time and memory, but a compiler that fails to preserve resource consumption "renders
source-level cost analysis useless." Few transformations in the literature are certified
with respect to resources, and most of those cover running time only.

**The motivating failure is linked closures.** When a shared environment holds variables
with different future lifetimes — some pointing at large structures — the collector cannot
reclaim any of it until the whole closure-pair becomes unreachable, which can inflate
memory by an amount *not bounded by any constant factor*. Flat closures are safe for space
but not optimal for creation time; more efficient safe-for-space algorithms exist (Shao and
Appel 1994, 2000), but nobody had formally established space safety for any of them. The
paper notes that unsafe sharing is not merely historical: the **JavaScript V8 engine's
environment-sharing strategy, based on linked environments, is not safe for space.**

**Why formal space reasoning is hard.** Counting allocated cells is insufficient — one must
reason about how many cells are *simultaneously live* at each point and show the transformed
program preserves that. Minamide (1999) did this for the CPS transformation by simulation,
but closure conversion perturbs the shape and lifetime of heap data far more. This paper
also goes further than preserving *idealized* space: it connects the source cost model to a
target model closer to a real implementation by accounting for the whole heap rather than
its reachable part, and by modeling calls to the garbage collector explicitly.

**The method** is a binary, step-indexed **logical relation**, with the technical novelty
that it imposes pre- and postconditions on the related programs, so resource bounds are
established simultaneously with functional correctness. Garbage collection is what makes
this delicate: it breaks Kripke monotonicity, since heaps do not merely grow but also shrink
and get *renamed* under a copying collector, so the relation quantifies over all future
heaps under a suitable notion of "future." The authors also explain why pre-/postcondition
monotonicity — what licenses weakening, strengthening, and frame rules in Hoare logic —
fails directly here, and how to restore it. The framework is described as
"garbage-collection compatible" for exactly this reason.

**What is proved.** For terminating source programs: semantics preservation plus space and
time safety. For diverging ones: divergence preservation plus space safety — capturing that
a program may run indefinitely in bounded memory, a case traditional logical relations
cannot handle. The supporting apparatus includes profiling semantics for time and space
before and after conversion, a formal garbage-collection model, and a heap-isomorphism
relation to cope with collector renaming. The paper also documents a **failed first attempt**
at the configuration relation before giving the definition that works.

## Why this matters

This is the formal settlement of a question the corpus has been circling from the
engineering side for thirty years.
[[continuation-passing-closure-passing-style|Appel and Jim]] observed in 1988 that linked
closures can retain data flat ones would release;
[[optimizing-closures-in-o-0-time|Keep, Hearn, and Dybvig]] build Chez's whole optimization
suite on the constraint of *remaining* safe for space while never doing harm. Both treat
the property as a design rule to respect. This paper proves the rule holds for flat
conversion, and does so in a cost model that includes the collector rather than idealizing
it away — which is what makes the result usable as a guarantee rather than an intuition.

It also sharpens what "safe for space" is a claim *about*. The definition here is
asymptotic — no increase beyond a constant factor per program — so it is compatible with
Chez's finding that flat closures cost more to create and less to access. The two are
answering different questions, and the V8 example shows the property is still worth
proving: a widely deployed engine shares environments in a way that is not space-safe, so
this is not a settled matter of folklore.

Set against [[lightweight-closure-conversion|Steckler and Wand]], it completes a pair.
Both papers prove a closure transformation correct; the earlier one establishes that a
constraint solution *justifies* omitting a captured variable, while this one establishes
that the transformation does not change what the program *costs*. Extensional correctness
and intensional preservation are separate obligations, and each paper takes one — which is
a cleaner way to see the difference than treating both as "verification."

Finally, it connects the compiler thread here to [[formal-methods]] in a concrete way. The
seL4-scale expense of verification is the usual framing; this is a case where the artifact
being verified is a *compiler optimization*, the property is *resource consumption*, and
the payoff is that source-level cost analysis remains meaningful after compilation.
