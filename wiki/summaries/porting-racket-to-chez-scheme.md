---
type: summary
status: reviewed
title: Porting Racket to Chez Scheme
created: 2026-06-29
source: https://users.cs.utah.edu/~mflatt/tmp/rkt-on-chez.pdf
raw: raw/2026-06-29-rkt-on-chez.md
tags: [racket, scheme, chez-scheme, lisp, programming-languages, language-implementation]
---

# Porting Racket to Chez Scheme

## Summary

An experience report on **Racket CS** — porting [[racket|Racket]] to run on top
of [[chez-scheme|Chez Scheme]] rather than its original C-based runtime. The
motivation is maintainability: Racket began in 1995 as a fusion of two
off-the-shelf C/C++ libraries — a [[scheme|Scheme]] interpreter
([[libscheme-scheme-as-a-c-library|Benson 1994]]) and a cross-platform GUI
toolkit — and although the distribution is now ~1.2M lines of Racket, it still
rests on ~200k lines of hard-to-maintain C. Chez Scheme, open-sourced in
mid-2016, is a far better-informed substrate for a functional language: proper
tail calls, first-class continuations bounded only by the heap, and the full
numeric tower — things the major mainstream VMs (JVM, etc.) handle poorly.

**How it works.** Racket's macro expander (already rewritten in Racket in 2016,
and shared unchanged here) elaborates modules into *linklets* — a λ-calculus
core whose imports and exports are explicit, potentially mutable variables,
which enables cross-module optimization. A new **schemify** layer translates
each linklet into a Chez Scheme `lambda`, which Chez's compiler then handles.
Racket relies on ~1500 primitives; most come for free from the shared
[[lisp|Lisp]]/Scheme heritage, with the rest supplied by Racket- and
Scheme-implemented compatibility layers plus a C **rktio** layer that abstracts
over operating-system facilities.

**Language mismatches.** The least predictable part of the effort was
reconciling ~30 differences between Racket and Chez Scheme, resolved four ways:
in schemify, in a compatibility library, by changes merged upstream into Chez,
or by Racket-specific patches to Chez. Examples: forcing left-to-right argument
evaluation (via nested `let`s); a well-performing **continuation marks**
primitive added to Chez (rather than a slow library version); preventing the
optimizer from collapsing non-tail calls that marks depend on; **applicable
structures** (`prop:procedure`) via a schemify rewrite of unknown calls;
procedure **arity reflection**; immutable pairs, vectors, and strings via a
mutability tag bit; chaperones and impersonators; **ephemerons** and **ordered
finalization** for the garbage collector; a type-reconstruction compiler pass;
and FFI work (C `struct` arguments, foreign-thread activation, compare-and-set).

**Performance & status.** The changes to Chez Scheme have negligible effect on
its own benchmarks. Racket CS roughly matches Racket on Scheme benchmarks but
lags on others; production programs run between slightly faster and ~50% slower,
with the biggest costs in compile time, code size, and load time (machine code
vs. the old lazily-parsed bytecode). Racket CS passes **>99.8% of the 813,650
core tests** (33 genuine failures), DrRacket runs, and it builds itself from
source. The maintainability payoff is concrete — rewriting the expander in
Racket grew its contributor pool from 2 people over 16 years to 6 over 2 years —
and the authors expect Racket CS to become the main Racket implementation, while
encouraging other functional-language implementers to consider Chez Scheme as a
target.

*Experience report by [[matthew-flatt|Matthew Flatt]] and colleagues (ICFP
2019); the source PDF is the anonymized review version.*

## Why this matters

This paper is the connective tissue between my own
[[libscheme-scheme-as-a-c-library|libscheme]] work and modern Racket: it traces
Racket's origin all the way back to libscheme (Benson 1994), so it closes the
loop between the source I just filed and the language Racket became.
