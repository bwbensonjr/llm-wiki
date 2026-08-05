---
type: concept
status: provisional
title: Nanopass
created: 2026-08-05
tags: [programming-languages, language-implementation, scheme, domain-specific-languages]
---

# Nanopass

A way of structuring a compiler as a large number of very small passes, each doing
essentially one job, over many formally-defined intermediate languages — supported by
a DSL that generates the traversal boilerplate so a pass writes only the clauses where
something actually happens.

## Notes

The organizing bet is that pass count is the wrong thing to economize. A conventional
compiler bundles many tasks into each of a few large passes because every pass costs a
full tree traversal and a pile of structural recursion to hand-write. If the
intermediate languages are formally specified, the framework can generate that
traversal, and the cost of an additional pass drops far enough that one-task passes
become affordable.

The framework provides two central forms: `define-language`, specifying an
intermediate-language grammar, and `define-pass`, specifying a transformation between
them. Formal grammars also buy checking — the framework can verify that a pass's
output actually conforms to its declared output language.

**Not to be confused with incremental compiler construction.**
[[an-incremental-approach-to-compiler-construction|Ghuloum's tutorial]] builds 24
progressively larger *source-language subsets*, each yielding a complete working
compiler; nanopass decomposes *one* compiler into many small passes over many
intermediate languages. Both react against the monolithic-pass tradition and both come
out of the same Indiana lineage, which is likely why they get conflated, but they
answer different questions. This wiki initially recorded the distinction from the
outside, before any nanopass source was ingested.

**Lineage.** The prototype framework is Sarkar, Waddell, and Dybvig; it proved the idea
workable but was only ever used for half of a student compiler. Keep and
[[r-kent-dybvig|Dybvig]] then rebuilt it for production use and rewrote
[[chez-scheme|Chez Scheme]]'s back end with it —
[[a-nanopass-framework-for-commercial-compiler-development|the paper]] reporting that
work shows the approach surviving contact with a commercial
compiler. Roughly 50 passes over 35 intermediate languages replaced five large ones,
generated code got 15–27% faster, and worst-case compile time rose to 1.75×.

The idea sits alongside other decomposition arguments in this wiki —
[[a-tractable-native-code-scheme-system|Scheme 48's]] separate byte-code optimizer,
Ghuloum's staged subsets — and the Chez rewrite measured and published what the
decomposition cost.

The argument itself is older than the name. Appel and Jim made it in 1988 for
[[standard-ml|SML/NJ]]'s back end
([[continuation-passing-closure-passing-style|Continuation-Passing, Closure-Passing Style]]),
aimed squarely at [[orbit-an-optimizing-compiler-for-scheme|ORBIT]]: where ORBIT
had "one black box covering phases 6 through 9," they had "four smaller black boxes" with
semantically well-defined interfaces, so an individual analysis could be isolated. What
the Chez work adds is not the principle but the scale and the price tag.

## Sources

- [[a-nanopass-framework-for-commercial-compiler-development|A Nanopass Framework for Commercial Compiler Development]]
- [[continuation-passing-closure-passing-style|Continuation-Passing, Closure-Passing Style]]
- [[optimizing-closures-in-o-0-time|Optimizing Closures in O(0) Time]]
