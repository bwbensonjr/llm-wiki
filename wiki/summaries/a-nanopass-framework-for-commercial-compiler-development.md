---
type: summary
status: provisional
title: A Nanopass Framework for Commercial Compiler Development
created: 2026-08-05
source: https://doi.org/10.1145/2544174.2500618
raw: raw/2026-08-05-2544174-2500618.md
tags: [programming-languages, language-implementation, scheme, lisp, chez-scheme, domain-specific-languages]
---

# A Nanopass Framework for Commercial Compiler Development

## Summary

Andrew Keep and [[r-kent-dybvig|R. Kent Dybvig]]'s ICFP 2013 paper reporting what
happened when [[chez-scheme|Chez Scheme]]'s back end was rewritten in the
[[nanopass|nanopass]] style. The question it answers is the one that had kept nanopass
a research idea: does decomposing a compiler into many tiny passes cost too much to
use in production?

**The framework** is a [[domain-specific-language|DSL]] for writing compilers, with
two central forms: `define-language`, which formally specifies an intermediate-language
grammar, and `define-pass`, which specifies a pass over those languages. Defining the
grammars formally is what pays: the framework fills in boilerplate, so a pass writes
only the clauses where it actually does something, and the rest of the tree is
traversed and rebuilt automatically.

It builds on the prototype framework of Sarkar et al., which had demonstrated
viability but was only ever used for the first half of a student compiler. Making it
carry a real compiler required smoothing rough edges on two fronts. *Usability:*
language definitions are no longer restricted to top level; passes may be defined with
no input or output language, so a pass can consume or produce a non-language term;
error messages carry source locations; and language definitions check more, catching
repeated meta-variables, removed productions that never existed, and duplicate field
names. *Performance:* pattern matching now dispatches on an integer tag rather than by
record dispatch, clause order is respected so likely matches can be placed first, and
less code is generated overall.

**The rewrite.** The original Chez compiler is ten large multipurpose passes and is,
in the authors' words, almost absurdly fast — it compiles its own source in roughly
three seconds. The new compiler keeps the same front end (a `syntax-case` expander
with a module system and R6RS libraries, per [[hygienic-macros]]) and replaces the
five back-end passes with **approximately 50 passes over about 35 nanopass
languages**, each doing primarily one job.

The other major change is a **graph-coloring register allocator**, which forced code
to be expanded into near-assembly form much earlier so that all temporaries are
visible. It packs spilled variables more tightly, uses registers better, produces more
compact code, and applies move biasing to avoid frame-to-frame moves — at a real
compile-time cost. The rewrite also improved
[[closure-conversion|closure optimization]], added implicit cross-library
optimization, and handled multiple-value returns better. Not everything survived: block
allocation of closures, where several closures created together share one allocation,
is not implemented in the new compiler.

**Results.** Generated code got faster — average run-time improvements of 26.6% and
22.3% on x86 (optimize levels 2 and 3) and 22.0% and 15.0% on x86-64. The authors
credit the graph-coloring allocator as the biggest and most consistent contributor.
They also report the outliers honestly: `similix` and `softscheme` invoke the compiler
*during* the benchmark run, so they got slower (up to 1.54× normalized) and dragged the
average down.

Compile time was the risk, and the target was to stay within a factor of two. Worst
case — 64-bit at optimize level 2 — came in at **1.75×** the original. The conclusion
is stated modestly: a nanopass compiler can perform on par with a traditionally
structured one, despite a more expensive register allocator and 50 passes replacing
five.

Compatibility rested on Chez's existing suite of unit, functional, and regression
tests, plus bootstrapping — the first test being that the compiler compiles itself and
the output matches. Examples in the paper are drawn from a student compiler rather
than Chez itself, since the Chez source was not open at the time.

## Why this matters

This closes a loop the wiki opened and explicitly deferred.
[[an-incremental-approach-to-compiler-construction|Ghuloum's tutorial]]
arrived with a curator note calling it the origin of "the nanopass idea"; the
ingest flagged that as wrong, and the first `curate` run confirmed the correction and
recorded that nanopass proper is Sarkar, Waddell, and Dybvig — while deferring the
[[nanopass]] hub. This paper is a primary source for nanopass proper, so
the hub is minted on evidence rather than inference, and the distinction the corpus
drew from the outside can now be checked from the inside:
[[an-incremental-approach-to-compiler-construction|Ghuloum's]] incrementality is 24
progressively larger *source languages*, each yielding a working compiler, while
nanopass decomposes *one* compiler into many tiny passes over many intermediate
languages. Same Indiana lineage, different ideas.

It is also the natural sequel to
[[the-development-of-chez-scheme|The Development of Chez Scheme]], ingested alongside
it. That paper ends at Version 7 in 2005 with ten multipurpose passes and Dybvig's
stated method of picking low-hanging fruit; this one is the same system seven years
later being taken apart and rebuilt on a different organizing principle. Reading them
together is unusual: a design argument and its own later revision by the same person.

The engineering claim worth keeping is the one about cost. Arguments for decomposition —
nanopass, Ghuloum's incremental subsets,
[[a-tractable-native-code-scheme-system|Scheme 48's]] separate byte-code optimizer — all
face the objection that clean structure is bought with performance. This paper measures
that trade on a commercial compiler, and the answer is concrete rather than rhetorical:
10× the passes, faster generated code, 1.75× worst-case compile time.
