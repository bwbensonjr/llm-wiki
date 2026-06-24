---
type: summary
title: A Programmable Programming Language
created: 2026-06-24
source: https://dl.acm.org/doi/10.1145/3127323
raw: raw/2026-06-24-3127323.md
tags: [racket, language-oriented-programming, domain-specific-languages, lisp, programming-languages, type-systems]
---

# A Programmable Programming Language

## Summary

A 2018 *Communications of the ACM* article (the published version of the 2015
"Racket Manifesto") arguing for [[language-oriented-programming]] (LOP): a
paradigm in which developers solve each part of a problem in a
[[domain-specific-language]] suited to its domain, then compose those
multilingual components into one system. The authors — led by
[[matthias-felleisen|Matthias Felleisen]], with Robert Bruce Findler, Matthew
Flatt, Shriram Krishnamurthi, Eli Barzilay, Jay McCarthy, and Sam
Tobin-Hochstadt — present [[racket]] as a platform built over 20 years to make
LOP friction-free.

Racket, an heir of [[lisp]] and Scheme, eliminates the hard boundary between
*library* and *language*: new linguistic constructs are imported as seamlessly
as functions or classes (its `class` system and `for` loops are themselves
library imports). Each module declares its language on the first line — like a
shell script's `#!` — so defining a language is just writing a module that
provides, reinterprets, or subtracts constructs from a base language. The key
innovation is a **modular, hygienic syntax system** (improving on Scheme macros,
which improved on Lisp's tree-transformation), letting developers incrementally
redefine constructs — e.g. redefining `lambda` to check argument predicates, a
step toward `typed/racket`.

The article develops three threads. **(1) Creating languages** by linguistic
reuse, one construct at a time. **(2) Soundness** — Racket spans a spectrum from
unsound C-level FFI veneers up through runtime checks, higher-order contracts
(with a blame mechanism that points to the two faulty components at a boundary),
and static [[type-systems]] (`typed/video`, `typed/racket`, and the `turnstile`
eDSL for expressing type systems). Cooperating components must respect each
language's invariants; a contract wraps exported values in a proxy that guards
access at every boundary. **(3) Internalizing OS services** — sandboxes,
inspectors, and custodians turn extra-linguistic mechanisms into language
constructs, so programmers no longer "step outside the language"; the `shill`
secure-scripting language relies on these. A worked running example is the
`video` eDSL for editing recordings of conference talks.

The authors are candid about limits: conventional (non-Lisp) syntax breaks
incrementality; type checkers must be built wholesale rather than attached
rule-by-rule to constructs; security still needs a research breakthrough; and
IDE tooling (debuggers, profilers) must be customized per language, an open
problem. A real-world validation: Sony's Naughty Dog game studio built a
Racket-based architecture with languages for describing scenes, transitions, and
scores, composed and compiled into dynamically linked libraries for a C-based
game engine.

## Why this matters

An early version of Racket (then MzScheme) was originally based on `libscheme`,
the Scheme implementation I wrote — so this paper traces the lineage of a
language-oriented-programming research project that grew out of my own work.
